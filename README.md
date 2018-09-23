# gist.py
## Requirements
```
Python >= 3.5
pip
```

## Installation
```sh
git clone https://github.com/pbellon/gist.git
cd gist
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
usage: gist.py [-h] {create,delete,list,show} ...

Use gist api with a CLI.

positional arguments:
  {create,delete,list,show}
    create              Creates a gist, data took from stdin or a file
    delete              Delete a gist
    list                List your gist
    show                Show details of a gist

optional arguments:
  -h, --help            show this help message and exit
```

### Create a gist:
```sh
# 1. from stdin
echo 'TEST' | py gist.py create --gist_name=test.text --description='test'
# Outputs:
{
    "url": "https://gist.github.com/a32a87f8d3a2498089143781340838b4",
    "api_url": "https://api.github.com/gists/a32a87f8d3a2498089143781340838b4",
    "id": "a32a87f8d3a2498089143781340838b4",
    "test.text": "https://gist.githubusercontent.com/pbellon/a32a87f8d3a2498089143781340838b4/raw/92cde0114177f8c6f3b09f473473b40a8abdadb2/test.text"
}
# 2. from file
echo 'TEST' > test.txt
py gist.py create --file=test.txt --description='test'
# Outputs:
{
    "url": "https://gist.github.com/9319922eac307fd91daba47225820fb5",
    "api_url": "https://api.github.com/gists/9319922eac307fd91daba47225820fb5",
    "id": "9319922eac307fd91daba47225820fb5",
    "test.txt": "https://gist.githubusercontent.com/pbellon/9319922eac307fd91daba47225820fb5/raw/92cde0114177f8c6f3b09f473473b40a8abdadb2/test.txt"
}
```

### Other commands:
```sh
# Show a gist details
$> py gist.py show <gist id>
# Delete a gist
$> py gist.py show <gist id>
# List gists
$ py gist.py list
```


[apps]: https://apps.twitter.com/
