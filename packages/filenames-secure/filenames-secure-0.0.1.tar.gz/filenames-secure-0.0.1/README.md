# filenames-secure

Obscure filenames of mp4 files - away from being embarrassed by accidently opening family videos at work!

Install with: `pip install filenames-secure`

**Obscure filenames of mp4 files - away from being embarrassed by accidently opening family videos at work!**

## Usage

Simply `$ filenames-secure` to obscure and restore.

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
import abbrs

RC_FILENAME = 'filenames-secure.json'

def make_dat(ls):
	def is_mp4(x):
		s = x.split('.')
		return len(s) >= 2 and (s[-1] == 'mp4' or s[-2] == 'mp4')

	def check_collision(d):
		for i, v in enumerate(d):
			for j in range(i + 1, len(d)):
				if d[i][0] == d[j][0]:
					return j
	
	dat = [ [ abbrs.cool_hash(i), i ] for i in filter(is_mp4, ls) ]
	
	while True:
		i = check_collision(dat)
		if i:
			print(f'Repairing collision: {dat[i][0]} -> {dat[i][1]}')
			dat[i][0] = abbrs.cool_hash(dat[i][0])
		else:
			break
	
	return dat

if __name__ == '__main__':
	import os
	if os.path.exists(RC_FILENAME):
		dat = abbrs.load_json(RC_FILENAME)
		
		for hash, filename in dat:
			os.rename(hash, filename)
	else:
		dat = make_dat(os.listdir())
		abbrs.json_dump(RC_FILENAME, dat)
		
		for hash, filename in dat:
			print(f'{hash} = {filename}')
			os.rename(filename, hash)
```