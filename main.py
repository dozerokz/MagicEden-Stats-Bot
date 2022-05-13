import discord
import requests
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import random

WEBHOOK_URL = "your_webhook_url"
BOT_TOKEN = "your_bot_token"

COLORS = ["E8AEA8", "FC3890", "07F5E0", "7C72F7"]
intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("Bot started")

@bot.command()
async def collection(ctx, arg):
    msg = await get_collection_stats(arg)
    if msg:
        await ctx.send(msg)

async def get_collection_stats(collection_name):
    try:
        r = requests.get("https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{}".format(collection_name))
        r = r.json()
        floor_price = round(r["results"]["floorPrice"]/1000000000, 3)
        total_value = round(r["results"]["volumeAll"]/1000000000, 3)
        volume_24h = round(r["results"]["volume24hr"]/1000000000, 3)
        listed = r["results"]["listedCount"]
        avg_price24h = round(r["results"]["avgPrice24hr"]/1000000000, 3)

        r = requests.get("https://api-mainnet.magiceden.io/collections/{}".format(collection_name))
        r = r.json()
        name = r["name"]
        image = r["image"]
        link = "https://magiceden.io/marketplace/{}".format(collection_name)

        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed = DiscordEmbed(title=name, color=random.choice(COLORS), url=link)
        embed.set_thumbnail(url=image)
        embed.set_timestamp()
        embed.add_embed_field(name='Floor Price', value=str(floor_price), inline=False)
        embed.add_embed_field(name='Total Volume', value=str(total_value), inline=False)
        embed.add_embed_field(name='24H Volume', value=str(volume_24h), inline=False)
        embed.add_embed_field(name='Listed', value=str(listed), inline=False)
        embed.add_embed_field(name='24H Average Price', value=str(avg_price24h), inline=False)

        webhook.add_embed(embed)
        webhook.execute()
    except:
        msg = "Can't get this collection stats! Make sure you used right name!"
        return msg


if __name__ == '__main__':
    bot.run(BOT_TOKEN)  # BOT TOKEN