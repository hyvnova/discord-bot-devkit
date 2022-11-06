# NoVa - Discord Bot Dev Kit 

#### Is a set of funtions and classes to simplify the creation of discord bots

## Installing DBDK

```bash
pip install dbdk
```
-  You can install **DBDK** manually using [PyPI](https://pypi.org/project/dbdk/)

## Importing DBDK

```py
from dbdk import * 
```

## Creating A `Root`

```py
@bot.command(name="sample")
async def sample_command(ctx: commands.context.Context):

    root: Root = await create_root(ctx)
```
- Roots are the start and managers of everything in **DBDK**.
In most cases you will only need **1 root** per command.

## `View` Introduction

- As shown in the example above, we assuming this is inside a command function definition.
```py
root: Root = await create_root(ctx)

# by default `root` has a `view` property
root.view

# You can add items to the view using `add_items` method
await root.view.add_items(
    Button(on_click_callback, "This is the label"),

    SelectMenu(
        on_select_callback, options = [
            SelectOption
        ]
    )
)
```
- **add_items** method update the root, so changes will be displayed when called

- Check [Pycord API reference: discord.ui.View](https://docs.pycord.dev/en/stable/api.html?highlight=view#discord.ui.View) for more details.


#### Adding a `Button` to the `view`

```py
# Create a on click callback function; this function is called when the button is clicked
async def on_click(clicked_button: Button, interaction: discord.Interaction):

    # respond the interacion
    await interaction.response.send_message("You Clicked the button!")

await root.view.add_items(
    Button(
        on_click,
        label = "Click Me!",
        emoji = '🙂'
    )
)

    # That's all, you'll see changes reflected in the root message
```
- Check [Pycord API reference: discord.Button](https://docs.pycord.dev/en/stable/api.html?highlight=view#discord.ui.Button) for more details.

# Embeds

```py
await root.embeds.add_items(
    Embed(
        title = "My Embed",
        description = "My embed description :D",
        color = discord.Color.green()
    )
)
```
- Check [Pycord API reference: discord.Embed](https://docs.pycord.dev/en/stable/api.html?highlight=view#discord.Embed) for more details.
