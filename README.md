# 🤖 MiMo Crypto Agent

AI-powered Crypto Research Telegram Bot built on **Xiaomi MiMo V2.5**

## Features

- 🔍 **Deep Project Research** — Analyze any crypto project (fundamentals, tokenomics, team)
- 📊 **Real-time Market Data** — Live prices, market cap, volume via CoinGecko
- 🎯 **Airdrop Tracker** — Discover and track airdrop opportunities
- 📈 **Trending Analysis** — Market narratives and trending tokens
- 💬 **Natural Chat** — Ask anything about crypto in plain language
- 🧠 **Conversation Memory** — Context-aware multi-turn conversations

## Tech Stack

- **AI Model:** Xiaomi MiMo V2.5 (OpenAI-compatible API)
- **Bot Framework:** python-telegram-bot
- **Data Source:** CoinGecko API
- **Language:** Python 3.11+

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/mimo-crypto-bot.git
cd mimo-crypto-bot
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your keys:
# - MIMO_API_KEY: Get from https://platform.xiaomimimo.com
# - TELEGRAM_BOT_TOKEN: Get from @BotFather on Telegram
```

### 3. Run

```bash
python bot.py
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/research <token>` | Deep project analysis |
| `/price <token>` | Current price & market data |
| `/airdrops` | Latest airdrop opportunities |
| `/trending` | Trending tokens & narratives |
| `/help` | Show all commands |

Or just **chat naturally** — ask anything about crypto!

## Architecture

```
┌─────────────────────────────────────────────┐
│              Telegram Bot                    │
│         (python-telegram-bot)                │
├─────────────────────────────────────────────┤
│              Bot Core (bot.py)               │
│   Command handlers + Chat handler            │
├──────────────────┬──────────────────────────┤
│  MiMo Client     │   Crypto Researcher       │
│  (mimo_client.py)│   (crypto_research.py)    │
│                  │                            │
│  Xiaomi MiMo     │   CoinGecko API           │
│  V2.5 API        │   (market data)            │
└──────────────────┴──────────────────────────┘
```

## Project Structure

```
mimo-crypto-bot/
├── bot.py              # Main bot — handlers & entry point
├── mimo_client.py      # Xiaomi MiMo API client (OpenAI-compatible)
├── crypto_research.py  # CoinGecko data fetching
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## How It Works

1. **User sends message** → Telegram Bot receives it
2. **Bot processes** → Determines if it's a command or chat
3. **Data gathering** → Fetches real-time crypto data (if needed)
4. **MiMo inference** → Sends context + query to Xiaomi MiMo V2.5
5. **Response** → Formats and sends back to user

The bot maintains conversation history per user, enabling natural multi-turn conversations about crypto topics.

## Why MiMo?

- 🚀 Fast inference — low latency responses
- 💰 Cost-effective — competitive token pricing
- 🧠 Strong reasoning — excellent for analysis tasks
- 🔌 OpenAI-compatible — easy integration
- 🌏 Multilingual — supports English & Indonesian

## License

MIT

## Built With

- [Xiaomi MiMo V2.5](https://mimo.xiaomi.com/) — AI Model
- [python-telegram-bot](https://python-telegram-bot.org/) — Telegram Bot Framework
- [CoinGecko API](https://www.coingecko.com/en/api) — Crypto Market Data
- [OpenAI Python SDK](https://github.com/openai/openai-python) — API Client
