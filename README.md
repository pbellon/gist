# gist.py
## Requirements
```
Python >= 3.5
pip
```

## Installation
```sh
git clone https://github.com/pbellon/tw.git
cd tw
pip install -r requirement.txt
```

## Configuration
```sh
cd lib/
mv env.sample.py env.py
```
Then edit env.py to add the proper key & secrets. To obtain them visit [twitter apps][apps] and create an app if necessary.

## Usage
```
usage: gist.py [-h] {create,list} ...

Use gist api with a CLI.

positional arguments:
  {create,list}
    create       Creates a gist, data took from stdin or a file (see --file)
    list         List your gist

optional arguments:
  -h, --help     show this help message and exit
```

Exemple:
```sh
$> py gist.py --retweets > my_latest_retweets.json
```

[apps]: https://apps.twitter.com/
