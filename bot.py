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

last_rates = {"buy": None, "sell": None}

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

def trend(current, previous):
    if previous is None:
        return ""
    diff = current - previous
    if diff > 0:
        return f"🔺 +{diff:.2f}"
    elif diff < 0:
        return f"🔻 {diff:.2f}"
    return "➡️"

def build_embed(buy_ads, sell_ads):
    def format_ads(ads, label):
        if not ads:
            return f"No {label.lower()} offers"
        result = ""
        for ad in ads[:5]:
            price = ad['adv']['price']
            name = ad['advertiser']['nickName']
            verified = "✅" if ad['advertiser'].get("userGrade") == 1 else ""
            result += f"**{name}** {verified}\n💰 `{price} PKR`\n\n"
        return result

    now = datetime.now().strftime("%d %b %Y • %I:%M %p")
    buy_prices = [float(ad['adv']['price']) for ad in buy_ads[:3]] if buy_ads else []
    sell_prices = [float(ad['adv']['price']) for ad in sell_ads[:3]] if sell_ads else []

    avg_buy = sum(buy_prices) / len(buy_prices) if buy_prices else 0
    avg_sell = sum(sell_prices) / len(sell_prices) if sell_prices else 0
    spread = avg_sell - avg_buy if avg_buy and avg_sell else 0

    buy_trend = trend(avg_buy, last_rates["buy"])
    sell_trend = trend(avg_sell, last_rates["sell"])

    color = 0xe74c3c if spread < 0 else 0x2ecc71

    embed = discord.Embed(
        title="Binance P2P USDT/PKR",
        description=f"📊 Updated: {now}",
        color=color
    )
    embed.set_thumbnail(url="https://cryptologos.cc/logos/tether-usdt-logo.png")
    embed.add_field(name="📈 Market Summary",
                    value=f"🟢 Avg Buy: `{avg_buy:.2f} PKR` {buy_trend}\n🔴 Avg Sell: `{avg_sell:.2f} PKR` {sell_trend}\n📊 Spread: `{spread:.2f} PKR`",
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

@bot.command(name='rates')
async def rates_command(ctx):
    try:
        buy_ads = fetch_ads("BUY")
        sell_ads = fetch_ads("SELL")
        embed = build_embed(buy_ads, sell_ads)
        await ctx.send(embed=embed)

        buy_prices = [float(ad['adv']['price']) for ad in buy_ads[:3]]
        sell_prices = [float(ad['adv']['price']) for ad in sell_ads[:3]]
        last_rates["buy"] = sum(buy_prices) / len(buy_prices) if buy_prices else None
        last_rates["sell"] = sum(sell_prices) / len(sell_prices) if sell_prices else None
    except Exception as e:
        await ctx.send(f"❌ Error fetching rates:\n```{str(e)}```")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

bot.run(TOKEN)
