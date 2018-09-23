import twitter
import json
import requests
import argparse
import ipdb
import sys

from .decorators import with_commands, command, command_arg
from . import env

@with_commands(description="Use gist api with a CLI.")
class GistApi:
    API_URL = "https://api.github.com"
    access_token = env.ACCESS_TOKEN

    def scope_params(self):
        return { 'scope': 'gist' }

    def auth_header(self):
        return { 'Authorization': "token %s" % self.access_token }

    @command(
        name='list',
        help='List your gist'
    )
    def list(self):
        url = '%s/gists' % self.API_URL
        req = requests.get(url,
            params=self.scope_params(),
            headers=self.auth_header())
        return req.json()

    @command(
        name='create',
        help='Creates a gist, data took from stdin or a file (see --file)',
        args=(
            command_arg('-f', '--file',
                help='Create gist from file, otherwise will use stdin',
                type=argparse.FileType('r'),
                default=sys.stdin),
            command_arg('-gn', '--gist_name',
                help='The name of the file to create. Will try to take --file\'s filename if not precised.',
            ),
            command_arg('-desc', '--description',
                help='Description of the gist to create',
            ),
            command_arg('--public',
                help='Creates a public gist',
                action='store_true',
            )
        ))
    def create(self, file, description, public=False,  gist_name=None):
        content = "".join(file.readlines())
        if gist_name is None:
            gist_name = file.name
        req = requests.post(url = "%s/gists" % self.API_URL,
            headers=self.auth_header(),
            params=self.scope_params(),
            data=json.dumps({
                "description": description,
                "public": public,
                "files": {
                    gist_name: {
                        "content": content
                    }
                }
            }))
        return req.json()

def init(): return GistApi()
