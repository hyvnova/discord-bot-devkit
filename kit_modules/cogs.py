import os
from pathlib import Path
from typing import List
from discord.ext.commands import Bot
 
from .types import FunctionType, CaptureType

class CogBundle:
    """
    #### Creates a CogBundle for easier cog loading and declaration
    """
    def __init__(self, cogs_folder: str | None, modules: List[str] | CaptureType):
        
        cogs_folder = Path(cogs_folder).name
        cogs_dir = cogs_folder + '.' if cogs_folder else ""
        
        if isinstance(modules, FunctionType):
            capture_type = modules
            
            self.extensions = [
                f"{cogs_dir}{file[:-3]}"
                for file in os.listdir(cogs_folder)
                if capture_type(file) and not file.startswith("_")
            ]
            
        else:
            self.extensions = [f"{cogs_dir}{mod}" for mod in modules]
            
    def __call__(self, bot: Bot):
        bot.load_extensions(*self.extensions)
        
        
        