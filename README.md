# 📈 Binance P2P Rate Bot

> A Discord bot that fetches **live USDT/PKR P2P rates** from Binance — right inside your server.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Binance P2P](https://img.shields.io/badge/Data-Binance%20P2P-F0B90B?logo=binance&logoColor=white)](https://p2p.binance.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 💡 What It Does

No more switching tabs to check crypto rates. Type one command in Discord and instantly get:

- 🟢 **Top Buy offers** — who's selling USDT cheapest
- 🔴 **Top Sell offers** — who's buying USDT at the highest rate
- 📊 **Average prices + spread** — so you know the market at a glance
- ✅ **Verified merchant badges** — only trusted Binance merchants shown
- 🔗 **Quick links** to [Crypto Awaz](https://cryptoawaz.com) and the [FAQ](https://cryptocurrencypakistan.org)

All wrapped in a clean Discord embed. Updated every time you call it.

---

## 🚀 Commands

| Command | Description |
|---------|-------------|
| `!rates` | Fetch live USDT/PKR P2P rates from Binance |
| `!fee` | Calculate P2P transaction fee — live via [CryptoAwaz DVA Bot](https://github.com/Dr-Hack/CryptoAwaz-DVA-BOT) |

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/Dr-Hack/binance-p2p-rate.git
cd binance-p2p-rate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your token

Copy the example env file and fill in your Discord bot token:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholder:

```env
DISCORD_TOKEN=your_actual_bot_token_here
```

> **Where do I get a token?**  
> Go to the [Discord Developer Portal](https://discord.com/developers/applications) → Your App → Bot → Reset Token.

### 4. Run the bot

```bash
python bot.py
```

You should see:
```
✅ Logged in as YourBot#1234
```

---

## 🛡️ How It Works

```
User types !rates
        ↓
Bot calls Binance P2P API (merchant ads only, PKR/USDT)
        ↓
Filters out promotional/privileged listings
        ↓
Calculates avg buy price, avg sell price, spread
        ↓
Sends a formatted Discord embed with top 5 offers each side
```

The bot queries the Binance P2P endpoint directly — no third-party data, no delay, always fresh.

---

## 📦 Requirements

- Python 3.8+
- A Discord bot token ([guide](https://discord.com/developers/applications))
- Bot invited to your server with `Send Messages` + `Embed Links` permissions

```
discord.py
requests
python-dotenv
```

---

## 🔒 Security

- The bot token is loaded from a `.env` file — **never hardcoded**
- `.env` is listed in `.gitignore` and will never be committed
- Use `.env.example` as a safe template when sharing or deploying

---

## 🌐 Built For

This bot is built for the Pakistani crypto community.  
Check out **[Crypto Awaz](https://cryptoawaz.com)** for market news and **[CryptoCurrency Pakistan](https://cryptocurrencypakistan.org)** for guides and FAQs.

---

## 📄 License

MIT — free to use, modify, and deploy.
