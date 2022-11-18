from typing import Callable, Awaitable
import discord

default_not_allowed_response = "Esta interacion pertenece a {author};"

def interaction_control_check(
    conditional: Callable[[discord.Member, discord.Interaction, discord.Component], bool],
    owner: discord.Member,
    response: str | discord.Embed = default_not_allowed_response
):
    """
    - Conditional: if the conditional is `True`, interaction will be responden with `response`
    
    - Note: `response` will be formated using 4 kwargs:
        - `author` : `owner.name: str`
        - `owner` : `discord.Member`
        - `interaction` : `discord.Interaction`
        - `component` : `discord.Component`
    """
    def inner(func: Callable[[discord.Component, discord.Interaction], Awaitable[None]]) -> Awaitable[None]:

        async def wrapper(component: discord.Component, interaction: discord.Interaction) -> Awaitable[None]:

            if not conditional(owner, interaction, component):

                if isinstance(response, discord.Embed):
                    await interaction.response.send_message(embed=response, ephemeral=True, delete_after=10)
                else:
                    await interaction.response.send_message(
                        response.format(author=owner.name, owner=owner, interaction=interaction, component=component), 
                        ephemeral=True, delete_after=10
                    )

            else:
                await func(component, interaction)

            return None

        return wrapper

    return inner


def only_owner(owner: discord.Member, response: str | discord.Embed = default_not_allowed_response):
    """
    Only allows the owner respond the interaction, other users who trigger the interaction will get `response` as response.

    - Note: `response` will be formated using 4 kwargs:
        - `author` : `owner.name: str`
        - `owner` : `discord.Member`
        - `interaction` : `discord.Interaction`
        - `component` : `discord.Component`

    """
    return interaction_control_check(lambda owner, interaction, _: owner.id == interaction.user.id, owner, response)

def only_higher_roles(owner: discord.Member, response: str | discord.Embed = default_not_allowed_response):
    """
    Only allows the higher roles (than owner role) respond the interaction, other users who trigger the interaction will get `response` as response.

    - Note: `response` will be formated using 4 kwargs:
        - `author` : `owner.name: str`
        - `owner` : `discord.Member`
        - `interaction` : `discord.Interaction`
        - `component` : `discord.Component`

    """
    return interaction_control_check(lambda owner, interaction, _: interaction.user.top_role <= owner.top_role, owner, response)


def only_if(
    owner: discord.Member,
    condition: Callable[[discord.Member, discord.Interaction, discord.Component], bool], 
    response: str | discord.Embed = default_not_allowed_response
):
    """
    Only allows the user who triggered the interaction use it if `condition` is `True`

    - Note: `response` will be formated using 4 kwargs:
        - `author` : `owner.name: str`
        - `owner` : `discord.Member`
        - `interaction` : `discord.Interaction`
        - `component` : `discord.Component`
    """

    return interaction_control_check(condition, owner, response)
