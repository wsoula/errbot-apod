"""Astronomy Picture Of the Day"""
import urllib.request
import json
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import requests


class Apod(BotPlugin):
    """Astronomy Picture Of the Day"""

    @botcmd
    def apod(self, msg, args):
        """Astronomy Picture Of the Day"""
        url = 'http://apod.heroku.com/api'
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        image_url = response['url']
        image_bytes = requests.get(image_url).content
        file = open('tmp.gif', 'wb')
        file.write(image_bytes)
        file.close()
        self.send_stream_request(msg.frm, open('tmp.gif', 'rb'), name='image.gif', stream_type='image/gif')
