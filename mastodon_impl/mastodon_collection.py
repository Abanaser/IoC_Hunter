from mastodon import Mastodon
import engine.database_connector as db_connector
import hashlib
import re
import json
import yaml
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

with open("./engine/regex.yaml", "r") as file:
    REGEXS = yaml.load(file, Loader=yaml.FullLoader)


def authenticate(client_id, client_secret, access_token, instance_url):
    mastodon = Mastodon(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=instance_url,
    )
    return mastodon


def parse_toot(data):
    for regex in REGEXS["regexes"]:
        if re.search(regex["pattern"], data["content"]):
            db_connector.write_to_db(data, "mastodon")


def search_toots(keyword, mastodon):
    search_results = mastodon.search(q=keyword)
    toots = search_results["statuses"]
    return toots


def scrape_mastodon(keyword, mastodon):
    toots = search_toots(keyword, mastodon)
    for toot in toots:
        data = {
            "user_name": toot["account"]["username"],
            "content": toot["content"],
            "url": toot["url"],
            "source": "Mastodon",
        }

        soup = BeautifulSoup(data["content"], "html.parser")
        data["content"] = soup.get_text()

        document_string = json.dumps(data, sort_keys=True)
        document_hash = hashlib.sha256(document_string.encode()).hexdigest()
        data["_id"] = document_hash
        print(data)
        parse_toot(data)


def run(instance_url="https://infosec.exchange"):
    load_dotenv()

    client_id = os.environ["MASTODON_CLIENT_ID"]
    client_secret = os.environ["MASTODON_CLIENT_SECRET"]
    access_token = os.environ["MASTODON_ACCESS_TOKEN"]
    mastodon = authenticate(client_id, client_secret, access_token, instance_url)
    with open("./mastodon_impl/mastodon_keywords", "r") as file:
        for keyword in file:
            scrape_mastodon(keyword, mastodon)


if __name__ == "__main__":
    run()
