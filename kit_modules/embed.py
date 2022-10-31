import discord, datetime
from typing import *
from discord import Colour, EmbedField
from .utils import ExceptionList
from .types import _Root

class EmbedTemplate(discord.Embed):
    def __init__(
        self,
        *,
        color: int | Colour = Colour.blue(),
        title: str = None,
        type: str = "rich",
        url: str = None,
        description: str = ...,
        timestamp: datetime.datetime = None,
        fields: List[EmbedField] | None = None
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

    def __call__(
        self,
        *,
        color: int | Colour = None,
        title: str = None,
        url: str = None,
        description: str = None,
        timestamp: datetime.datetime = None,
        fields: List[EmbedField] | None = None
    ) -> discord.Embed:

        return discord.Embed(
            color=(color or self.color),
            title=(title or self.title),
            type=self.type,
            url=(url or self.url),
            description=(description or self.description),
            timestamp=(timestamp or self.timestamp),
            fields=(fields or self.fields),
        )

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
        description: str  = "Preparing Embed...",
        timestamp: datetime.datetime = None,
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
        `color: int | Colour`,
        `title: str | None`,
        `type: str = "rich"`,
        `url: str | None`,
        `description: str | None`,
        `timestamp: datetime.datetime`,
        `fields: List[EmbedField] | None`
        """

        # remove starting description
        if not self.__loaded:
            # remove starting description
            if not properties.get("description"):
                properties["description"] = ""

            self.__loaded = True

        for name, value in properties.items():
            setattr(self, name, value)

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