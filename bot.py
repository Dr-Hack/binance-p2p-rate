import discord
from discord.ext import commands
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Binance payload and fetching logic
def get_payload(trade_type):
    return {
        "fiat": "PKR",
        "page": 1,
        "rows": 10,
        "tradeType": trade_type,
        "asset": "USDT",
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "filterType": "all",
        "publisherType": "merchant",
        "classifies": ["mass", "profession", "fiat_trade"],
        "tradedWith": False,
        "followed": False
    }

def fetch_ads(trade_type):
    response = requests.post(
        'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
        json=get_payload(trade_type),
        timeout=10
    )
    if response.status_code != 200:
        raise Exception(f"Binance API failed: {response.status_code} - {response.text}")
    return [ad for ad in response.json().get("data", []) if ad.get("privilegeType") != 4]

def build_embed(buy_ads, sell_ads):
    def format_ads(ads, label):
        if not ads:
            return f"No {label.lower()} offers"
        result = ""
        for ad in ads[:5]:
            price = ad['adv']['price']
            name = ad['advertiser']['nickName']
            verified = "✅" if ad['advertiser'].get("userGrade") == 1 else ""
            result += f"**{name}** {verified} - 💰 `{price} PKR`\n"
        return result

    now = datetime.now().strftime("%d %b %Y • %I:%M %p")
    buy_prices = [float(ad['adv']['price']) for ad in buy_ads[:3]] if buy_ads else []
    sell_prices = [float(ad['adv']['price']) for ad in sell_ads[:3]] if sell_ads else []

    avg_buy = sum(buy_prices) / len(buy_prices) if buy_prices else 0
    avg_sell = sum(sell_prices) / len(sell_prices) if sell_prices else 0
    spread = avg_sell - avg_buy if avg_buy and avg_sell else 0

    embed = discord.Embed(
        title="Binance P2P USDT/PKR",
        description=f"📊 Updated: {now}",
        color=0x2ecc71
    )
    embed.set_thumbnail(url="https://cryptologos.cc/logos/tether-usdt-logo.png")
    embed.add_field(name="📈 Market Summary",
                    value=f"🟢 Avg Buy: `{avg_buy:.2f} PKR`\n🔴 Avg Sell: `{avg_sell:.2f} PKR`\n📊 Spread: `{spread:.2f} PKR`",
                    inline=False)
    embed.add_field(name="🟢 Top Buy Offers", value=format_ads(buy_ads, "BUY"), inline=True)
    embed.add_field(name="🔴 Top Sell Offers", value=format_ads(sell_ads, "SELL"), inline=True)
    embed.add_field(
        name="​",
        value="🌐 [Crypto Awaz](https://cryptoawaz.com) • 📖 [FAQ](https://cryptocurrencypakistan.org)\n⏱️ Type `/fee` to calculate fee",
        inline=False
    )
    embed.timestamp = datetime.now(timezone.utc)
    return embed

# 👇 Command users will call: !rates
@bot.command(name='rates')
async def rates_command(ctx):
    try:
        buy_ads = fetch_ads("BUY")
        sell_ads = fetch_ads("SELL")
        embed = build_embed(buy_ads, sell_ads)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error fetching rates:\n```{str(e)}```")

# 👋 On ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

bot.run(TOKEN)
