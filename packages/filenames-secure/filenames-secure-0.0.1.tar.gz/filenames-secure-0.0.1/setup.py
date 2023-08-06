import abbrs

package_name = abbrs.current_path()
description = 'Obscure filenames of mp4 files - away from being embarrassed by accidently opening family videos at work!'

abbrs.pypi_setup(description, f'''**{description}**

## Usage

Simply `$ {package_name}` to obscure and restore.

## How it Works

Filenames will be CRC-32'd, with restore record kept in an JSON file in the same folder.

## Collisions

If there are hash collisions, a different secure filename will be selected, then the collision check goes again, until there are no collisions - so there should be no risks of getting data lost - however, there are no warranties.

## Functional / Stability

If filename A is encoded into B this time, it will be encoded into B again next time, and forever - if there are no collisions that force a change.

## Does CRC-32 often collide?

No. It rarely happens. If it occurs, I suggest going out, buying a lottery.

## Code

The code is simple:

```python
{abbrs.read_file('{}/__init__.py'.format(package_name))}
```''')