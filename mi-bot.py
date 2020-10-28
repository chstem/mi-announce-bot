#!/usr/bin/env python3

import json
import requests
import os
import feedparser
import urllib

from time import mktime
from datetime import datetime as dt


# Read bot token from environment
TOKEN = os.environ['MIA_TG_TOKEN']
CHATID = os.environ['MIA_TG_CHATID']

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=MarkdownV2".format(text, chat_id)
    get_url(url)

def tg_send(text):
    send_message(text, CHATID)

from time import mktime
from datetime import datetime as dt

MINKORREKT_RSS='http://minkorrekt.de/feed/'

mi_feed = feedparser.parse(MINKORREKT_RSS)

newest_episode = mi_feed['items'][0]

episode_release = dt.fromtimestamp(mktime(newest_episode['published_parsed']))

if (dt.now() - episode_release).total_seconds()/8600 < 1:
    tg_send('*%s*\nEine neue Folge Methodisch inkorrekt ist erschienen\!\n[Jetzt anhören](%s)' % (newest_episode.title,newest_episode.link))

