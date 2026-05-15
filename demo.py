#!/usr/bin/env python3
"""
MiMo Crypto Agent — Live Demo
Shows bot architecture + real crypto data fetching
"""

import json
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crypto_research import CryptoResearcher

print("=" * 60)
print("🤖 MiMo Crypto Agent — Live Demo")
print("   Powered by Xiaomi MiMo V2.5")
print("=" * 60)
print()

# ─── Demo 1: Crypto Research ─────────────────────────────────────────────

researcher = CryptoResearcher()

print("📊 [1/3] Fetching real-time Bitcoin data...")
btc_data = researcher.get_token_data("bitcoin")
if btc_data:
    print(f"   ✅ Name: {btc_data.get('name')}")
    print(f"   💰 Price: ${btc_data.get('price_usd', 'N/A'):,.2f}")
    print(f"   📈 24h Change: {btc_data.get('price_change_24h', 'N/A'):.2f}%")
    print(f"   📊 Market Cap: ${btc_data.get('market_cap', 0):,.0f}")
    print(f"   🏆 Rank: #{btc_data.get('market_cap_rank', 'N/A')}")
else:
    print("   ⚠️ Could not fetch data")

print()

print("📊 [2/3] Fetching Ethereum data...")
eth_data = researcher.get_token_data("ethereum")
if eth_data:
    print(f"   ✅ Name: {eth_data.get('name')}")
    print(f"   💰 Price: ${eth_data.get('price_usd', 'N/A'):,.2f}")
    print(f"   📈 24h Change: {eth_data.get('price_change_24h', 'N/A'):.2f}%")
    print(f"   📊 Market Cap: ${eth_data.get('market_cap', 0):,.0f}")
else:
    print("   ⚠️ Could not fetch data")

print()

print("🔥 [3/3] Fetching trending tokens...")
trending = researcher.get_trending()
if trending:
    print("   Top 5 Trending:")
    for i, coin in enumerate(trending.get("trending_coins", [])[:5], 1):
        print(f"   {i}. {coin.get('name')} ({coin.get('symbol')}) — Rank #{coin.get('market_cap_rank', '?')}")
else:
    print("   ⚠️ Could not fetch trending")

print()
print("=" * 60)
print("🧠 MiMo V2.5 Integration")
print("=" * 60)
print()
print("   API Provider: Xiaomi MiMo")
print("   Model: MiMo-V2.5")
print("   Format: OpenAI-compatible")
print("   Features:")
print("   • Natural language crypto research")
print("   • Multi-turn conversation memory")
print("   • Real-time market data analysis")
print("   • Airdrop & testnet tracking")
print("   • 4-wallet identity management")
print()
print("=" * 60)
print("📁 Project Structure")
print("=" * 60)
print()
print("   mimo-crypto-bot/")
print("   ├── bot.py              — Telegram bot core")
print("   ├── mimo_client.py      — Xiaomi MiMo API client")
print("   ├── crypto_research.py  — CoinGecko data module")
print("   ├── requirements.txt    — Dependencies")
print("   ├── .env.example        — Config template")
print("   └── README.md           — Documentation")
print()
print("=" * 60)
print("✅ Demo complete! Bot ready for deployment.")
print("   GitHub: https://github.com/dpk-jr/mimo-crypto-bot")
print("=" * 60)
