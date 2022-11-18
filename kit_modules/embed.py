import discord, datetime
from typing import Awaitable, List, Dict, Any
from discord import Colour, EmbedField
from .states import ExceptionList, State, process_states
from .types import _Root
from dataclasses import dataclass


@dataclass
class EmbedAuthor:
    name: str
    url: str
    icon_url: str

@dataclass
class EmbedFooter:
    text: str
    icon_url: str
        

@dataclass
class EmbedAuthor:
    name: str
    url: str
    icon_url: str

@dataclass
class EmbedFooter:
    text: str
    icon_url: str
        

class Embed(discord.Embed):
    
    """
    Creates a Embed
    - Make sure you pass `root` if you creating the embed outside a `EmbedList`.`add_item` method
    """
    Exceptions = ExceptionList(
        NotExistingField = "You trying to add items to a field that doens't exists or is not declared in the Embed"
    )

    def __init__(
        self,
        title: str | None = None,
        color: int | Colour = discord.Color.blue(),
        type: str = "rich",
        url: str | None = None,
        description: str = "Preparing Embed...",
        footer : EmbedFooter = None,
        author : EmbedAuthor | discord.Member | None = None,
        image : str = None,
        thumbnail : str = None,
        timestamp: datetime.datetime | None = None,
        fields: List[EmbedField] | None = None,
        root: _Root | None = None
    ):
        
        super().__init__(
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp,
            fields=fields,
        )

        self.root: _Root = root
        self.custom_fields: Dict[str, List[Any]] = {}
        self.__loaded: bool = False
        
        if author: self.author = author
        if image: self.set_image(url=image)
        if thumbnail: self.set_thumbnail(url=thumbnail)
        if footer: self.footer = footer

    # setters
    @property
    def author(self):
        return self.author 
    
    @author.setter
    def author(self, author: discord.Member | EmbedAuthor):
        if isinstance(author, discord.Member):
            author = EmbedAuthor((author.nick or author.name), None, (author.guild_avatar or author.avatar).url)

        self.set_author(**{k:v for k,v in author.__dict__.items() if v and not k.startswith("_")})
        
    @property
    def footer(self):
        return self.footer
    
    @footer.setter
    def footer(self, footer: EmbedFooter):
        self.set_footer(**{k:v for k,v in footer.__dict__.items() if v and not k.startswith("_")})

    # methods
    async def update(self):
        """Updates embed at root embeds."""
        if self.root:
            await self.root.embeds.update()

    async def create_field(self, field_name: str, field_items: List[Any] = []) -> None:
        self.custom_fields[field_name] = field_items

        await self.update()

    async def add_to_field(self, field_name: str, field_items: List[Any]) -> None:

        field: list = self.fields.get(field_name)

        if not field:
            raise Embed.Exceptions.NotExistingField()

        field.extend(field_items)

        await self.update()

    async def edit(self, **properties) -> None:
        """
        #### Edits the properties of the embed then updates it

        #### Properties
        - `title` : `str` | `State`,
        - `color` : `int` | `State` | `Colour`,
        - `url`: `str` | `State`,
        - `description` : `str` | `State`,
        - `footer` : `EmbedFooter`,
        - `author` : `EmbedAuthor` | `discord.Member`,
        - `image` : `str` | `State`,
        - `thumbnail` : `str` | `State`,
        - `timestamp` : `datetime.datetime`,
        - `field_at` : `Tuple[int, EmbedField]`
        - `fields` : `List[EmbedField]`
        """

        # remove starting description
        if not self.__loaded:
            # remove starting description
            if not properties.get("description"):
                properties["description"] = ""

            self.__loaded = True

        for name, value in properties.items():
            if name == 'image':
                self.set_image(url=value)
                
            elif name == "thumbnail":
                self.set_thumbnail(url=value)
                
            elif name == "field_at":
                index, field = value
                self.set_field_at(index, name=field.name, value=field.value, inline=field.inline)
            
            else:
                #  try setting attribute setting directly
                try:
                    setattr(self, name, value)
                except AttributeError as e:
                    print("Exception was most-likely caused because you tried to set a property that doesn't exits or cannot be setted to Embed at edit method")
                    raise e
            

        await self.update()


class EmbedList(list):
    def __init__(self, root: _Root, *items):
        self.root: _Root = root
        super().__init__(items)

    def update_item(self, item: Embed) -> "EmbedList":
        self[self.index(item)] = item
        return self 
    
    async def update(self) -> Awaitable[None]:
        await self.root.edit(embeds=self)
        
    async def add_items(self, *embeds: Embed) -> Awaitable[None]:
        """
        Adds 1 or more items to the View, then updates it.
        """
        for embed in embeds:
            embed.root = self.root
            self.append(embed)
            
        await self.update()