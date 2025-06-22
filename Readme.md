# Simplified Binance Futures Trading Bot

A command-line bot built with Python to trade on the **Binance USDT-M Futures Testnet**. The bot supports market, limit, stop ,TWAP and Grid order strategies. It uses the official `python-binance` package and allows configurable trading via CLI.

---

## ✅ Features

* Place **Market** and **Limit** orders (Buy/Sell)
* Support for **OCO** and **TWAP** strategies
* Binance **Futures Testnet** integration
* Command-line interface with argument parsing
* Full logging of requests, responses, and errors
* Configurable through CLI flags or `.env`

---

## 📦 Requirements

* Python 3.8+
* pip
* Binance Testnet account
* Docker (if you want to automate the above process)

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/your-username/simplified-trading-bot.git
cd simplified-trading-bot
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Setup `.env`

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret

```

---

## ⚙️ CLI Usage

Run the bot with the following commands:

### Market Order

```bash
python run_bot.py market --symbol BTCUSDT --qty 0.01 --side BUY
```

### Limit Order

```bash
python run_bot.py limit --symbol BTCUSDT --qty 0.01 --price 65000 --side SELL
```
### Stop the Current Order

```bash
python run_bot.py stop --symbol BTCUSDT --qty 0.01 --stop-price 65000 
```

### TWAP Order

```bash
python run_bot.py twap --symbol BTCUSDT --qty 0.10 --side BUY --start-time 2025-06-22T10:00:00Z --end-time 2025-06-22T12:00:00Z --slices 12
```
---
### Grid Strategy

```bash
python run_bot.py grid --symbol BTCUSDT --qty 0.10  --lower-price  --upper-price --levels
```
---

## 📄 Logging

All logs are stored in `binance_order.log`:

* Order success/failure
* API errors and responses

---


## 📬 Contact

Created by Ayaan Amjad(https://github.com/Ayaan-tech) — feel free to open issues or pull requests!
