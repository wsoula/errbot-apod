"""Astronomy Picture Of the Day"""
import urllib.request
import json
import secrets
from datetime import date
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import requests


class Apod(BotPlugin):
    """Astronomy Picture Of the Day"""

    @botcmd
    def apod(self, msg, args):
        """Astronomy Picture Of the Day"""
        return self.apod_send(msg, random=False)

    @botcmd
    def apod_random(self, msg, args):
        """Random Astronomy Picture Of the Day"""
        return self.apod_send(msg, random=True)

    def apod_send(self, msg, random):
        """Astronomy Picture Of the Day"""
        current_date = date.today()
        if random:
            year = str(secrets.choice(range(2000, current_date.year)))
            month = str(secrets.choice(range(1, 13)))
            day = str(secrets.choice(range(1, 29)))
        else:
            year = str(current_date.year)
            month = str(current_date.month)
            day = str(current_date.day)
        # apodapi.herokuapp.com/api/?date=2001-07-12
        url = 'http://apodapi.herokuapp.com/api/?date='+year+'-'+month+'-'+day
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        if 'url' in response:
            image_url = response['url']
            image_bytes = requests.get(image_url).content
            file = open('tmp.gif', 'wb')
            file.write(image_bytes)
            file.close()
            self.send_stream_request(msg.frm, open('tmp.gif', 'rb'), name='image.gif', stream_type='image/gif')
            return response['description']
        return 'No image for:'+year+'-'+month+'-'+day
