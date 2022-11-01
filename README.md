# NoVa - Discord Bot Dev Kit 

### Is a set of funtions and classes to simplify the creation of discord bots

## Installing DBDK

```bash
pip install dbdk
```
-  You can install **DBDK** manually using [PyPI](https://pypi.org/project/dbdk/)

## Importing DBDK

```py
from dbdk import * 
```
*Note:* check **Imports and Defined members** to know what's being imported

## Creating A `Root`

```py
@bot.command(name="sample")
async def sample_command(ctx: commands.context.Context):

    root: Root = await createRoot(ctx)
```
- Roots are the start and managers of everything in **DBDK**.
In most cases you will only need **1 root** per command.

## `View` Introduction

- As shown in the example above, we assuming this is inside a command function definition.
```py
root: Root = createRoot(ctx)

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


### Adding a `Button` to the `view`

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


# Imports & Defined Members

- *This may vary a lot.*

0. ### **Any**                  =   `typing.Any`
1. ### **Await**                =   `typing.Await`
2. ### **Awaitable**            =   `typing.Awaitable`
3. ### **Bot**                  =   `discord.ext.commands.Bot`
4. ### **Button**               =   `discord.ui.Button`
5. ### **ButtonStyle**          =   `discord.ButtonSyle`
6. ### **Callable**             =   `typing.Calleable`
7. ### **Colour**               =   `discord.Colour`
8. ### **Component**            =   `discord.Component`
9. ### **Dict**                 =   `typing.Dict`
10. ### **Embed**               =   `discord.Embed`
11. ### **EmbedField**          =   `discord.EmbedField`
12. ### **EmbedList**           =   `dbdk.embed.EmbedList`
13. ### **EmbedTemplate**       =   `dbdk.embed.EmbedTemplate`
14. ### **Emoji**               =   `discord.Emoji`
15. ### **ExceptionList**       =   `dbdk.utils.ExceptionList`
16. ### **InputText**           =   `discord.ui.InputText`
17. ### **InputTextStyle**      =   `discord.InputTextStyle` *(Shortcut)*
18. ### **InputTextType**       =   `discord.InputTextStyle` *(Shortcut)*
19. ### **List**                =   `typing.List`
20. ### **Modal**               =   `dbdk.modal.Modal`
21. ### **OptionType**          =   ?
22. ### **Root**                =   `dbdk.root.Root`
23. ### **RootItems**           =   `dbdk.root.RootItems`
24. ### **SelectMenu**          =   `dbdk.components.SelectMenu`
25. ### **SelectOption**        =   `dbdk.components.SelectOption`
26. ### **States**              =   `dbdk.utils.States` *(Concept class)*
27. ### **Tuple**               =   `typing.Tuple`
28. ### **Union**               =   `typing.Union`
29. ### **View**                =   `dbdk.view.View`
38. ### **commands**            =   `discord.ext.commands`
39. ### **components**          =   `dbdk.components` *(Module)*
40. ### **create_root**         =   `dbdk.kit.create_root`
41. ### **datetime**            =   `datetime` *(Module)*
42. ### **default_on_select**   =   `dbdk.components.default_on_select`
43. ### **default_on_submit**   =   `dbdk.modal.default_on_submit`
44. ### **default_on_timeout**  =   `dbdk.view.default_on_timeout`
45. ### **discord**             =   `discord` *(Module)*
46. ### **embed**               =   `dbdk.embed` *(Module)*
47. ### **extract**             =   `dbdk.utils.extract`
48. ### **modal**               =   `dbdk.modal` *(Module)*
49. ### **namedtuple**          =   `collections.namedtuple`
50. ### **root**                =   `dbdk.root` *(Module)*
51. ### **types**               =   `dbdk.types` *(Module)*
52. ### **ui**                  =   `discord.ui` *(Shortcut)* 
53. ### **utils**               =   `dbdk.utils` *(Module)*
54. ### **view**                =   `dbdk.view` *(Module)*