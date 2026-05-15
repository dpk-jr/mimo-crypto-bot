"""
MiMo Crypto Agent — AI Crypto Research Telegram Bot
Powered by Xiaomi MiMo V2.5

Features:
- Natural language crypto research powered by MiMo
- Real-time token prices & market data
- Project analysis (fundamentals, tokenomics, team)
- Airdrop & testnet opportunity alerts
- Multi-chain support
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from mimo_client import MiMoClient
from crypto_research import CryptoResearcher

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Initialize clients
mimo = MiMoClient()
researcher = CryptoResearcher()


# ─── System Prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are MiMo Crypto Agent — an AI-powered crypto research assistant built on Xiaomi MiMo V2.5.

Your capabilities:
1. Research any crypto project (fundamentals, tokenomics, team, roadmap)
2. Provide real-time market analysis and price insights
3. Track airdrop and testnet opportunities
4. Explain DeFi concepts in simple terms
5. Analyze on-chain data and trends

Guidelines:
- Be concise but thorough in analysis
- Always mention risks — crypto is volatile
- Use emoji to make responses more readable
- Format data with clear structure (headers, bullets)
- When unsure, say so — don't make up data
- Respond in the user's language (English or Indonesian)

You have access to real-time crypto data tools. Use them when users ask about prices, projects, or market data."""


# ─── Command Handlers ────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    welcome = """
🤖 **MiMo Crypto Agent** — AI Crypto Research Assistant
Powered by Xiaomi MiMo V2.5

**Commands:**
/research `<token>` — Deep research on a crypto project
/price `<token>` — Get current price & market data
/airdrops — Latest airdrop opportunities
/trending — Trending tokens & narratives
/help — Show all commands

Or just **chat naturally** — ask me anything about crypto!

**Examples:**
• "What is EigenLayer?"
• "Compare Arbitrum vs Optimism"
• "Any new airdrops worth farming?"
• "Explain restaking in simple terms"
"""
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def research_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deep research on a crypto project."""
    if not context.args:
        await update.message.reply_text("Usage: /research <token name>\nExample: /research EigenLayer")
        return

    query = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 Researching **{query}**...")

    # Gather data
    market_data = researcher.get_token_data(query)
    project_info = researcher.get_project_info(query)

    # Ask MiMo for analysis
    prompt = f"""Provide a comprehensive research report on "{query}":

Market Data:
{json.dumps(market_data, indent=2) if market_data else "No real-time data available"}

Project Info:
{json.dumps(project_info, indent=2) if project_info else "No project info available"}

Include:
1. 📋 Project Overview (what it does, problem it solves)
2. 🏗️ Technology & Architecture
3. 👥 Team & Backers
5. 💰 Tokenomics (supply, distribution, utility)
6. 📊 Market Analysis (price trends, TVL, volume)
7. ⚡ Airdrop/Testnet Status (if applicable)
8. ⚠️ Risk Assessment
9. 🎯 Verdict & Score (1-10)

Format with markdown. Be thorough but concise."""

    response = await mimo.chat(prompt, system=SYSTEM_PROMPT)
    await msg.edit_text(response[:4096], parse_mode="Markdown")


async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current price & market data."""
    if not context.args:
        await update.message.reply_text("Usage: /price <token>\nExample: /price bitcoin")
        return

    query = " ".join(context.args)
    data = researcher.get_token_data(query)

    if not data:
        await update.message.reply_text(f"❌ Could not find data for '{query}'")
        return

    # Format price response with MiMo
    prompt = f"""Format this crypto market data as a clean, readable summary:

{json.dumps(data, indent=2)}

Include: price, 24h change, 7d change, market cap, volume, ATH.
Use emoji and markdown formatting. Be concise."""

    response = await mimo.chat(prompt, system=SYSTEM_PROMPT)
    await update.message.reply_text(response[:4096], parse_mode="Markdown")


async def airdrops_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show latest airdrop opportunities."""
    prompt = """List the top 5-8 current crypto airdrop/testnet opportunities worth farming right now.

For each, include:
- Project name & chain
- What to do (tasks)
- Estimated reward potential
- Deadline (if any)
- Difficulty level

Focus on high-quality, legitimate projects. Include both easy and advanced opportunities.
Format with markdown and emoji."""

    msg = await update.message.reply_text("🔍 Finding airdrop opportunities...")
    response = await mimo.chat(prompt, system=SYSTEM_PROMPT)
    await msg.edit_text(response[:4096], parse_mode="Markdown")


async def trending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show trending tokens and narratives."""
    trending_data = researcher.get_trending()

    prompt = f"""Based on this trending data and your knowledge, provide a market overview:

Trending Data:
{json.dumps(trending_data, indent=2) if trending_data else "No real-time data"}

Include:
1. 🔥 Top trending tokens & why
2. 📈 Market narratives gaining momentum
3. 📉 What's losing steam
4. 🎯 Key events this week
5. 💡 Alpha tips (with risk disclaimers)

Be concise and actionable."""

    msg = await update.message.reply_text("📊 Analyzing market trends...")
    response = await mimo.chat(prompt, system=SYSTEM_PROMPT)
    await msg.edit_text(response[:4096], parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help."""
    help_text = """
📚 **MiMo Crypto Agent — Commands**

**Research:**
/research `<token>` — Deep project analysis
/price `<token>` — Price & market data
/trending — Trending tokens & narratives
/airdrops — Airdrop opportunities

**Chat:**
Just type any question about crypto!

**Examples:**
• "Explain liquid staking"
• "What are the best L2s?"
• "Is it a good time to buy ETH?"
• "Compare Uniswap vs Curve"
• "How to bridge to Base?"

**Built with:** Xiaomi MiMo V2.5 🤖
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


# ─── Chat Handler ────────────────────────────────────────────────────────────

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language messages."""
    user_message = update.message.text
    user_id = update.effective_user.id

    # Get conversation history
    history = context.user_data.get("history", [])

    # Show typing
    await update.message.chat.send_action("typing")

    # Get response from MiMo
    response = await mimo.chat(
        user_message,
        system=SYSTEM_PROMPT,
        history=history[-10:],  # Keep last 10 messages
    )

    # Update history
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response})
    context.user_data["history"] = history[-20:]  # Keep max 20

    # Send response (split if too long)
    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            await update.message.reply_text(response[i:i+4096], parse_mode="Markdown")
    else:
        await update.message.reply_text(response, parse_mode="Markdown")


# ─── Error Handler ───────────────────────────────────────────────────────────

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Error: {context.error}", exc_info=context.error)
    if update and update.message:
        await update.message.reply_text("⚠️ Something went wrong. Please try again.")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not set in .env")
        return

    print("🤖 MiMo Crypto Agent starting...")

    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("research", research_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("airdrops", airdrops_command))
    app.add_handler(CommandHandler("trending", trending_command))
    app.add_handler(CommandHandler("help", help_command))

    # Chat
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    # Error
    app.add_error_handler(error_handler)

    print("✅ Bot is running! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
