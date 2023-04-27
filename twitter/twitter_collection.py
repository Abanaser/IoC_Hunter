import snscrape.modules.twitter as sntwitter
import engine.database_connector as db_connector
import hashlib
import re
import json
import yaml

with open("./engine/regex.yaml", "r") as file:
    REGEXS = yaml.load(file, Loader=yaml.FullLoader)


def parse_tweet(data):
    for regex in REGEXS["regexes"]:
        if re.search(regex["pattern"], data["content"]):
            db_connector.write_to_db(data, "twitter")


def scrape_twitter(keyword):
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword}").get_items()):
        if i > 1:
            break
        data = {
            "user_name": tweet.user.username,
            "content": tweet.rawContent,
            "url": tweet.url,
            "source": "Twitter",
        }

        document_string = json.dumps(data, sort_keys=True)
        document_hash = hashlib.sha256(document_string.encode()).hexdigest()
        data["_id"] = document_hash
        parse_tweet(data)


def run():
    with open("./twitter/twitter_keywords", "r") as file:
        for keyword in file:
            scrape_twitter(keyword)


if __name__ == "__main__":
    run()
