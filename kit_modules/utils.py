from typing import Any, Callable, Dict

def globalize(_globals: Callable[[], Dict[str, Any]],  **variables : Any) -> None:
    """
    Makes the given variables `global`, so they can acceded using the `global` keyword
    
    - `**variables` : `var_name` = `var_value`
    """
    _globals().update(**variables)
    

     