# Discord Bot Dev Kit 
### Is a set of funtions and classes to simplify the creation of discord bots

## Installing DBDK
```bash
pip install dbdk
```

## Importing DBDK
```py
from dbdk import * # Note: dbdk imports pycord
```


## Creating A `Root`
```py
@bot.command(name="sample")
async def sample_command(ctx: commandd.context.Context):
    
    root: Root = createRoot(ctx)
```
Roots are the start and managers of everything in dbdk.
In most cases you will only need **1 root** per command

## `View` Introduction
```py
    # as shown in the example above, we assuming this is inside a command function definition

    root: Root = createRoot(ctx)

    # by default `root` has a `view` property
    # Check Pycord API reference: discord.ui.View; for more detais

    root.view

    # You can add items to the view using `add_item` or  `add_items` methods

    await root.view.add_items(
        Button(on_click_callback, "This is the label"),

        SelectMenu(
            on_select_callback, options = [
                SelectOption
            ]
        )
    )

    # These methods updates the root, so changes will be displayed when they're called

```

### Adding a `Button` to the `view`
```py
    # Check Pycord API reference: discord.Button; for more detais

    # Create a on click callback function; this function is called when the button is clicked

    async def on_click(clicked_button: Button, interaction: discord.Interaction):

        # respond the interacion
        await interaction.response.send_message("You Clicked the button!")

        # Check Pycord API reference: discord.Interaction ; for more detais

    await root.view.add_item(
        on_click,
        label = "Click Me!",
        emoji = '🙂'
    )

    # That's all,you'll see changes reflected in the root message
