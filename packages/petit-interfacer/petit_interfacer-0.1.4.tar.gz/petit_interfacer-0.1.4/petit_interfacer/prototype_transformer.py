from dataclasses import dataclass
import functools
import inspect
from typing import (Any, Callable, Dict, Final, List, Optional, Set, TypeVar,
                    Union, get_args, get_origin, get_type_hints)

from .exceptions import MissingHints
from .utils import (ClassProxyTest, clean_union_type, is_blindbind,
                    is_proxy_class, is_real_optional, validate_blindbind)
import asyncio
NoneType = type(None)
T = TypeVar('T')
U = TypeVar('U')

base_code: Final[str] = "lambda {all_params}: func({reduced_params})"

async_string = """
async def test({all_params}):
    return await func({reduced_params})
output = test
"""


def get_parameters_hint(func: Callable) -> Dict[str, Any]:
    parameters = get_type_hints(func)
    if 'return' in parameters:
        del parameters['return']
    return parameters


def adapt_for(all_args: List[str], args: Dict[str, str], is_async: bool) -> Callable[[Callable], Callable]:
    def decorator(func: Callable):
        # TODO: bind remaining params if `func` has more default params than all_args
        new_func = None
        if asyncio.iscoroutinefunction(func):
            if not is_async:
                raise TypeError(
                    'Expected sync function and got async function')
            context = {'output': None, 'func': func}
            string = async_string.format(
                all_params=','.join(all_args),
                reduced_params=','.join(
                    f'{new_name}={old_name}' for old_name, new_name in args.items())
            )
            exec(string, context)
            new_func = context['output']
        else:
            if is_async:
                raise TypeError(
                    'Expected async function and got sync function')
            string = base_code.format(
                all_params=','.join(all_args),
                reduced_params=','.join(
                    f'{new_name}={old_name}' for old_name, new_name in args.items())
            )
            new_func: Callable = eval(
                string,
                {'func': func},
            )
        return functools.wraps(func)(new_func)
    return decorator


# TODO: not enough type hint
def make_transfomer(all_args: List[str]) -> Callable[[Callable], Callable]:
    return functools.partial(adapt_for, all_args)


# TODO: type hint seems false
def transformer_from_prototype(func: Callable[[T], U]):
    return make_transfomer(inspect.signature(func).parameters.keys())


def interface_binder_for(proto: T) -> Callable[[Callable], T]:
    """Will try to bind two interfaces together by using type hinting:

    You can use special annotations for this, such as RealOptional and BlindBind

    ### RealOptional

    The decorator won't force the bind the parameter if it is missing in the decorated function

    ### BlindBind

    If an annotation is missing, then the decorator will bind the unknown parameter on the BlindBind parameter

    As such you can only have one BindBind parameter per function prototype
    """
    parameters = get_parameters_hint(proto)
    required_names: Set[str] = {
        name for name, value in parameters.items() if not is_real_optional(value)
    }
    names = [name for name in parameters.keys()]
    classes = [cls for cls in parameters.values()]
    is_async = asyncio.iscoroutinefunction(proto)
    # check if only one BlindBind
    blind_param = validate_blindbind(names, classes)
    transformer = transformer_from_prototype(proto)

    def f(func: Callable):
        res: Dict[str, str] = {}
        sig = get_parameters_hint(func)

        # in case of None, sig doesn't have any data
        for n, v in inspect.signature(func).parameters.items():
            if n not in sig:
                sig[n] = None
        handled_params = 0
        for param_name, annotation in sig.items():
            if inspect.isclass(annotation):
                for i, cls in enumerate(classes):
                    if get_origin(cls) is Union:
                        cls = list(get_args(cls))
                        clean_union_type(cls)
                    # kinda ugly, but this is compile time
                    a = cls
                    if not isinstance(cls, list):
                        a = [cls]
                    for c in a:
                        if is_proxy_class(c):
                            # c: ClassProxyTest
                            if c.is_correct_type(annotation):
                                res[names[i]] = param_name
                                handled_params += 1
                                break
                        elif issubclass(annotation, c):
                            res[names[i]] = param_name
                            handled_params += 1
                            break
                #     else:
                #         break
                # else:
                #     raise Exception(
                #         f'Invalid type hint in {func.__name__}, {annotation}')

            elif annotation is None:
                res[blind_param] = param_name
        keys = set(res.keys())

        if len(sig) == handled_params + 1:
            for key in sig.keys():
                if key not in keys:
                    res[blind_param] = key

        # validate required names
        for name in required_names:
            if name not in res:
                raise MissingHints(
                    f"Wasn't able to bind all parameters based on annotations for function: {func.__name__}"
                    f"| failed to bind {name}"
                )

        return transformer(res, is_async)(func)
    return f
