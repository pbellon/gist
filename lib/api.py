import twitter
import json
import requests
import argparse
import ipdb
import sys

from .decorators import with_commands, command, command_arg
from . import env

gist_id = command_arg('gist', nargs=1, type=str,
    help='ID of the gist to delete (e.g: aa5a315d61ae9438b18d)'
)

@with_commands(description="Use gist api with a CLI.")
class GistApi:
    API_URL = "https://api.github.com"
    access_token = env.ACCESS_TOKEN

    def scope_params(self):
        return { 'scope': 'gist' }

    def auth_header(self):
        return { 'Authorization': "token %s" % self.access_token }

    @command(
        name='show', help='Show details of a gist',
        args=(gist_id,)
    )
    def show(self, gist):
        url = "{base}/gists/{id}".format(base=self.API_URL, id=gist[0])
        req = requests.get(url, params=self.scope_params(),
            headers=self.auth_header())
        return req.json()

    @command(
        name='delete', help='Delete a gist',
        args=(gist_id,)
    )
    def delete(self, gist):
        id = gist[0]
        url = "{base}/gists/{id}".format(base=self.API_URL, id=id)
        req = requests.delete(url, params=self.scope_params(),
            headers=self.auth_header())
            
        deleted = req.status_code == 204
        return { "result": (
                "Deleted gist %s" if deleted else (
                "An error occured with gist %s")
            ) % id
        }

    @command(
        name='list',
        help='List your gist'
    )
    def list(self):
        url = '%s/gists' % self.API_URL
        req = requests.get(url,
            params=self.scope_params(),
            headers=self.auth_header())

        data = req.json()
        return list(
            map(lambda gist: {
                "url": gist['html_url'],
                "id": gist['id'],
                "files": len(gist['files'].keys())
            }, data)
        )

    @command(
        name='create',
        help='Creates a gist, data took from stdin or a file',
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

        print("Content has %s chars" % len(content))
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
        data = req.json()
        result = {
            'url': data['html_url'],
            'api_url': data['url'],
            'id': data['id'],
            gist_name: data['files'][gist_name]['raw_url']
        }
        return result

def init(): return GistApi()
