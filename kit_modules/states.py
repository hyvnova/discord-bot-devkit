#
# 
# THIS IS STILL A CONCEPT, DOESNT WORK YET
#
#


from typing import Any, Awaitable, Callable, Dict, List

class _StateValue:
    """
    StateValue provides all instances where a state is "mounted" to recieve the update value and be able to use the property as a value directly, without calling any methods
    
    Example:
    ```
    # Without StateValue
    instance.propery.get() 
    
    # With StateValue
    instance.property
    """
    def __init__(self, value: Any) -> None:
        self.value = value

    def __get__(self, instance, owner) -> Any:
        return self.value
    
class State:
    def __init__(self, value: Any):
        self.__mounted = False # check if call method was call
        self.value = value
        self.on_change_callbacks: List[Callable[[None], Awaitable[None]]] = []
        self.on_delete: List[Callable[[None], None]] = []
        
    def get(self):
        return self.value
    
    async def set(self, value) -> Awaitable[None]: 
        if not self.__mounted:
            raise TypeError("State was not mounted; needs to be called after declaring")
        
        self.value = value
        
        try:
            for callback in self.on_change_callbacks:
                await callback()
        except:
            raise TypeError("Missing update function")

    def __call__(self, instance, name):
        if not self.__mounted: self.__mounted = True
        
        self.on_change_callbacks.append(instance.update)
        
        cls = type(instance)
        
        self.on_delete.append(lambda: delattr(cls, name) )
        
        setattr(cls, name, property(
            lambda instance: self.get(),  # getter
            lambda instance, value: None  # setter
        ))
    
    def __del__(self) -> None:
        map(
            lambda callback: callback(),
            self.on_delete
        )
        del self
                
class States(dict):
    """This class should NOT be instaciated directly (unless you kno what you doing), use the `create_states` method instead"""
    def __init__(self, states : Dict[str, State]) -> None:
        super().__init__(states)
        
    async def set(self, key: str, value: Any) -> Awaitable[None]:        
        state : State = self[key]
        await state.set(value)
        
    async def set_many(self, states: Dict[str, Any], skip_if_null: bool = True) -> Awaitable[None]:
        for k,v in states.items():
            if not v and skip_if_null:
                continue
            
            await self.set(k,v)

def create_states(**kwargs) -> States:
    """
    ### Creates a States object
    #### Note: remember all items that use the states must have a update method
    """
    return States({k: State(v) for k,v in kwargs.items()})
               
def process_states(instance: object, _locals : Dict[str, Any]):
    for key, value in _locals.items():
        if not isinstance(value, State):
            continue
        
        value(instance, key)
        
        