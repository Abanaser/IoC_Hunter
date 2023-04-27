from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os


def discord(data):
    load_dotenv()
    webhook = DiscordWebhook(
        url=os.getenv("DISCORD_WEBHOOK_URL"),
    )

    # Role, or specific user to ping
    # webhook.content = (
    #     "<@&1042573033447108628>"  # TODO Role ID e.g., <@&1003330526754639892>
    # )

    embed = DiscordEmbed(
        title=f"New IoC found!",
        description=f"Source: {data['source']}",
        color="03b2f8",
    )
    embed.set_timestamp()
    embed.set_author(name="⚡️ IoC Hunter ⚡️")

    embed.add_embed_field(
        name="Content",
        value=f"{data['content']}",
        inline=False,
    )

    embed.add_embed_field(
        name="URL",
        value=f"{data['url']}",
        inline=False,
    )

    webhook.add_embed(embed)

    webhook.execute()
