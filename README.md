# 🚀 Binance Futures Testnet Trading Bot (Python)

## 📌 Overview

This project is a simplified trading bot built in Python that interacts with Binance Futures Testnet (USDT-M).
It allows users to place MARKET and LIMIT orders via CLI with proper validation, logging, and error handling.

---

## ⚙️ Features

* Place **MARKET** and **LIMIT** orders
* Supports both **BUY** and **SELL**
* CLI-based input (argparse)
* Input validation
* Structured code (modular design)
* Logging of API requests, responses, and errors
* Error handling for:

  * Invalid inputs
  * API errors
  * Network issues

---

## 🏗️ Project Structure

trading_bot/
│── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│── cli.py
│── requirements.txt
│── README.md

---

## 🔧 Setup Instructions

### 1. Clone the repository

git clone https://github.com/Rahman-s/binance-trading-bot-python
cd binance-trading-bot-python

### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate     (Windows)

### 3. Install dependencies

pip install -r requirements.txt

---

## 🔑 Binance Testnet Setup

* Register on Binance Futures Testnet
* Generate API Key & Secret
* Replace in config file or environment variables

Base URL:
https://testnet.binancefuture.com

---

## ▶️ How to Run

### MARKET Order Example

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002

### LIMIT Order Example

python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 65000

---

## 📊 Sample Output

## Order Request Summary

Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.002

## Order Response Summary

Status: SUCCESS
Order ID: XXXXX
Executed Qty: 0.002
Avg Price: 70365

---

## 🧾 Logging

Logs are stored in:
logs/app.log

Includes:

* API requests
* API responses
* Errors

---

## ⚠️ Assumptions

* Only USDT-M futures supported
* User provides valid API keys
* Price required only for LIMIT orders

---

## 🚀 Future Improvements (Optional)

* Stop-Limit orders
* Better CLI UX
* Risk management module

---
