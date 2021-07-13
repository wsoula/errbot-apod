"""Astronomy Picture Of the Day"""
import urllib.request
import json
import secrets
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd
import requests
from datetime import date


class Apod(BotPlugin):
    """Astronomy Picture Of the Day"""

    @arg_botcmd('-r', dest='random', type=bool, default=False)
    def apod(self, msg, random=False):
        """Astronomy Picture Of the Day"""
        current_date = date.today()
        if random:
            year = str(secrets.choice(range(2000, current_date.year)))
            month = str(secrets.choice(range(1, 13)))
            day = str(secrets.choice(range(1, 29)))
        else:
            year = current_date.year
            month = current_date.month
            day = current_date.day
        # apodapi.herokuapp.com/api/?date=2001-07-12
        url = 'http://apodapi.herokuapp.com/api/?date='+year+'-'+month+'-'+day
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        image_url = response['url']
        image_bytes = requests.get(image_url).content
        file = open('tmp.gif', 'wb')
        file.write(image_bytes)
        file.close()
        self.send_stream_request(msg.frm, open('tmp.gif', 'rb'), name='image.gif', stream_type='image/gif')
        self.send(response['description'])
