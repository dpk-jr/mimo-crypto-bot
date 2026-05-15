"""
Crypto Research Module
Fetches real-time data from CoinGecko and other sources
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_KEY = os.getenv("COINGECKO_API_KEY", "")

HEADERS = {"accept": "application/json"}
if COINGECKO_KEY:
    HEADERS["x-cg-demo-api-key"] = COINGECKO_KEY


class CryptoResearcher:
    """Fetches crypto data from public APIs."""

    def get_token_data(self, query: str) -> dict | None:
        """
        Get token market data from CoinGecko.
        
        Args:
            query: Token name or symbol (e.g., "bitcoin", "ETH")
        
        Returns:
            dict with price, market_cap, volume, etc. or None
        """
        try:
            # Search for the token
            search_url = f"{COINGECKO_BASE}/search"
            resp = requests.get(search_url, params={"query": query}, headers=HEADERS, timeout=10)
            
            if resp.status_code != 200:
                return None
            
            coins = resp.json().get("coins", [])
            if not coins:
                return None

            # Get the top match
            coin = coins[0]
            coin_id = coin["id"]

            # Get detailed market data
            detail_url = f"{COINGECKO_BASE}/coins/{coin_id}"
            detail_resp = requests.get(
                detail_url,
                params={
                    "localization": "false",
                    "tickers": "false",
                    "community_data": "false",
                    "developer_data": "false",
                },
                headers=HEADERS,
                timeout=10,
            )

            if detail_resp.status_code != 200:
                return {
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol", "").upper(),
                    "market_cap_rank": coin.get("market_cap_rank"),
                }

            data = detail_resp.json()
            market = data.get("market_data", {})

            return {
                "name": data.get("name"),
                "symbol": data.get("symbol", "").upper(),
                "market_cap_rank": data.get("market_cap_rank"),
                "price_usd": market.get("current_price", {}).get("usd"),
                "price_change_24h": market.get("price_change_percentage_24h"),
                "price_change_7d": market.get("price_change_percentage_7d"),
                "price_change_30d": market.get("price_change_percentage_30d"),
                "market_cap": market.get("market_cap", {}).get("usd"),
                "total_volume": market.get("total_volume", {}).get("usd"),
                "ath": market.get("ath", {}).get("usd"),
                "ath_change": market.get("ath_change_percentage", {}).get("usd"),
                "atl": market.get("atl", {}).get("usd"),
                "circulating_supply": market.get("circulating_supply"),
                "total_supply": market.get("total_supply"),
                "max_supply": market.get("max_supply"),
                "fdv": market.get("fully_diluted_valuation", {}).get("usd"),
                "categories": data.get("categories", []),
                "description": data.get("description", {}).get("en", "")[:500],
                "website": data.get("links", {}).get("homepage", [None])[0],
                "twitter": data.get("links", {}).get("twitter_screen_name"),
                "telegram": data.get("links", {}).get("telegram_channel_identifier"),
                "github": data.get("links", {}).get("repos_url", {}).get("github", [None])[0] if data.get("links", {}).get("repos_url", {}).get("github") else None,
            }

        except Exception as e:
            return None

    def get_project_info(self, query: str) -> dict | None:
        """
        Get additional project info.
        Combines CoinGecko data with search results.
        """
        data = self.get_token_data(query)
        if not data:
            return None

        return {
            "name": data.get("name"),
            "symbol": data.get("symbol"),
            "categories": data.get("categories"),
            "description": data.get("description"),
            "website": data.get("website"),
            "twitter": data.get("twitter"),
            "github": data.get("github"),
        }

    def get_trending(self) -> dict | None:
        """Get trending tokens from CoinGecko."""
        try:
            resp = requests.get(
                f"{COINGECKO_BASE}/search/trending",
                headers=HEADERS,
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            data = resp.json()
            trending = []
            for coin in data.get("coins", [])[:10]:
                item = coin.get("item", {})
                trending.append({
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "market_cap_rank": item.get("market_cap_rank"),
                    "price_btc": item.get("price_btc"),
                    "score": item.get("score"),
                })

            return {"trending_coins": trending}

        except Exception:
            return None

    def get_global_data(self) -> dict | None:
        """Get global crypto market data."""
        try:
            resp = requests.get(
                f"{COINGECKO_BASE}/global",
                headers=HEADERS,
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            data = resp.json().get("data", {})
            return {
                "total_market_cap": data.get("total_market_cap", {}).get("usd"),
                "total_volume": data.get("total_volume", {}).get("usd"),
                "btc_dominance": data.get("market_cap_percentage", {}).get("btc"),
                "eth_dominance": data.get("market_cap_percentage", {}).get("eth"),
                "active_cryptos": data.get("active_cryptocurrencies"),
                "markets": data.get("markets"),
            }

        except Exception:
            return None
