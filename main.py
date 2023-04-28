import twitter.twitter_collection as twitter_collection
import mastodon_impl.mastodon_collection as mastodon_collection
from engine.api import app
from engine.database_connector import connect_to_db
import uvicorn
import threading


def start_api():
    print("Starting API")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def start_twitter():
    print("Starting Twitter Collection")
    twitter_collection.run()


def start_mastodon():
    print("Starting Mastodon Collection")
    mastodon_collection.run()


def main():
    # Connecting to DB
    if not connect_to_db():
        print("Error connecting to DB")
        return
    # Start the web server in a separate thread
    api_thread = threading.Thread(target=start_api)
    api_thread.start()

    # Start the twitter collection in a separate thread
    twitter_thread = threading.Thread(target=start_twitter)
    twitter_thread.start()

    # Start the mastodon collection in a separate thread
    mastodon_thread = threading.Thread(target=start_mastodon)
    mastodon_thread.start()


if __name__ == "__main__":
    main()
