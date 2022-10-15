from typing import Any, Callable, Dict, List, Union


def extract(obj: Union[Dict, object], keys: List[str] = None):
    if not keys:
        try:
            keys = obj.__dict__.keys()
            obj = obj.__dict__

        except:
            keys = obj.keys()

    return [obj[key] for key in keys]


def is_calleable(object: Any):
    return "__call__" in object.__dict__

class ExceptionList:
    """
    #### Creates a exception list object

    #### Parameters
    - exceptions : {name: message, ...}

    #### Example
    ```
    exceptions = ExceptionList({
        "MissingElement" : "You missing a element",
    })
    ...
    raise exceptions.MissingElement() 
    taise exceptions.MissingElement(f"You missing {missing_elemenet} element...")

    ```
    """
    def __init__(self, **exceptions: Dict[str, str]):

        for name, message in exceptions.items():

            exception_class = type(
                name, (Exception,), {}
            )

            if isinstance(message, str):
                self.__dict__[name] = lambda new_message=None: exception_class(new_message or message)

            else:
                raise ValueError(f"Value of exception message must be either str or calleable (function) not {type(message)}. at ExceptionList")


    def fire(self, exception_name: str, exception_message: Any = None):
        """Raises the indicated exception"""

        exception_class: Exception = self.__dict__.get(exception_name)

        if not exception_class:
            raise ValueError(f"{exception_name} is not a declared exception")

        raise exception_class(exception_message)
