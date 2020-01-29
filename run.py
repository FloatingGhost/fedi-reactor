import os
import sys
import requests
from mastodon import Mastodon
from pyaml import yaml
from urllib.parse import urljoin

with open("config.yaml", "r") as f:
    config = yaml.load(f)

BASE_URL = config["instance"]

user_creds = ".usersecret"
app_secret = ".app_secret"

if not os.path.exists(user_creds):
    Mastodon.create_app("reactor", api_base_url=BASE_URL, to_file=app_secret)

    mastodon = Mastodon(client_id=app_secret, api_base_url=BASE_URL)
    mastodon.log_in(config["user"], config["password"], to_file=user_creds)

mastodon = Mastodon(access_token=user_creds, api_base_url=BASE_URL)

token = mastodon.access_token

id = sys.argv[1]
word = sys.argv[2]

base = 127462
letters = "abcdefghijklmnopqrstuvwxyz"
mapping = {}

for i in range(26):
    mapping[letters[i]] = base + i

out = []
for letter in word.lower():
    if letter in mapping:
        while letter in out:
            letter += '\u200b'
        out.append(chr(mapping[letter]))
    else:
        out.append(letter)
for letter in out:
    print("Reacting with", letter)
    r = requests.post(
        urljoin(BASE_URL, "/api/v1/pleroma/statuses/{}/react_with_emoji".format(id)),
        json={"emoji": letter},
        headers={"Authorization": "Bearer {}".format(token)},
    )
    print(r.json())
