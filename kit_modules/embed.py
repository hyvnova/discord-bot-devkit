import discord, datetime
from typing import *
from discord import Colour, EmbedField
from .utils import ExceptionList
from .root import RootMessage

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
    Exceptions = ExceptionList(
        NotExistingField = "You trying to add items to a field that doens't exists or is not declared in the Embed"
    )

    def __init__(
        self,
        root_message: RootMessage,
        color: int | Colour = discord.Color.blue(),
        title: str | None = None,
        type: str = "rich",
        url: str | None = None,
        description: str  = "Preparing Embed...",
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

        self.custom_fields: Dict[str, List[Any]] = {}

        self.root_message = root_message

        self.__loaded: bool = False


    async def update(self):
        if self.root_message:
            await self.root_message.edit(embed=self)

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

