from typing import Any, Dict

import string, random

def get_random_string(length) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

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


     