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
usage: python gist.py [-h] [--retweets] [--timeline]

Small utility to retrieve tweets as JSON from twitter api.

optional arguments:
  -h, --help  show this help message and exit
  --retweets  Get user latest retweets
  --timeline  Get user timeline (limited)
```

Exemple:
```sh
$> py gist.py --retweets > my_latest_retweets.json
```

[apps]: https://apps.twitter.com/
