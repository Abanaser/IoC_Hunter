from mastodon_impl import Mastodon
import argparse


def authenticate(client_id, client_secret, access_token, instance_url):
    mastodon = Mastodon(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=instance_url,
    )
    return mastodon


def search_toots(keyword, mastodon, max_results):
    search_results = mastodon.search(q=keyword)
    toots = search_results["statuses"]
    return toots


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for toots on Mastodon based on keywords."
    )
    parser.add_argument(
        "--keyword", type=str, required=True, help="Keyword to search for"
    )
    parser.add_argument(
        "--instance_url",
        type=str,
        required=True,
        help='Mastodon instance URL (e.g., "https://mastodon.social")',
    )
    parser.add_argument(
        "--client_id", type=str, required=True, help="Your Mastodon app client ID"
    )
    parser.add_argument(
        "--client_secret",
        type=str,
        required=True,
        help="Your Mastodon app client secret",
    )
    parser.add_argument(
        "--access_token", type=str, required=True, help="Your Mastodon app access token"
    )
    parser.add_argument(
        "--max_results",
        type=int,
        default=40,
        help="Maximum number of toots to retrieve (default: 40)",
    )
    args = parser.parse_args()

    mastodon = authenticate(
        args.client_id, args.client_secret, args.access_token, args.instance_url
    )
    print(type(args.keyword))
    toots = search_toots(args.keyword, mastodon, args.max_results)

    for idx, toot in enumerate(toots):
        print(f"#{idx+1}: {toot['url']}\n{toot['content']}\n")
