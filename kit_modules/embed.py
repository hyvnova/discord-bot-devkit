import discord, datetime
from typing import *
from discord import Colour, EmbedField
from .utils import ExceptionList


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
    exceptions = ExceptionList(
        NotExistingField="You trying to add items to a field that doens't exists or is not declared in the Embed"
    )

    def __init__(
        self,
        original_message: discord.Message,
        color: int | Colour = discord.Color.blue(),
        title: str | None = None,
        type: str = "rich",
        url: str | None = None,
        description: str | None = None,
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

        self.original_message = original_message

    async def update(self):
        if self.original_message:
            await self.original_message.edit(embed=self)

    async def create_field(self, field_name: str, field_items: List[Any] = []):
        self.custom_fields[field_name] = field_items

        await self.update()

    async def add_to_field(self, field_name: str, field_items: List[Any]):

        field: list = self.fields.get(field_name)

        if not field:
            raise Embed.exceptions.NotExistingField()

        field.extend(field_items)

        await self.update()
