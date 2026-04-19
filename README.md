# DACHAIN BOT

> 🌐 **Register here first:** [https://inception.dachain.io/?ref=DAC00162](https://inception.dachain.io/?ref=DAC00162)

An automated bot for **DAChain Testnet** that handles daily tasks including faucet claims, on-chain transactions (send, stake, burn), and profile tracking — all in one tool.

---

## ✨ Features

- ✅ Auto Login with Wallet Address
- ✅ Auto Faucet Claim
- ✅ Auto Send Transactions to Random Addresses
- ✅ Auto Stake DAC
- ✅ Auto Burn DAC for QE
- ✅ Profile & Balance Tracker
- ✅ Proxy Support (Optional)
- ✅ Multi-Account Support
- ✅ Auto Cycle (every 8 hours)

---

## 📋 Requirements

- Python 3.8+
- pip packages (see `requirements.txt`)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/febriyan9346/DACHAIN-BOT.git
cd DACHAIN-BOT

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. `accounts.txt`
Add your EVM private keys, one per line:
```
0xYOUR_PRIVATE_KEY_1
0xYOUR_PRIVATE_KEY_2
```

### 2. `proxy.txt` *(optional)*
Add your proxies, one per line:
```
http://user:pass@ip:port
http://ip:port
```

---

## ▶️ Usage

```bash
python bot.py
```

You will be prompted to:
1. Choose proxy mode (with / without proxy)
2. Set number of **Send** transactions per account
3. Set amount of DAC to **Stake** per account
4. Set amount of DAC to **Burn** for QE per account

---

## 📊 What the Bot Does Each Cycle

| Step | Action |
|------|--------|
| 1 | Fetch CSRF Token |
| 2 | Login with Wallet Address |
| 3 | Claim Faucet |
| 4 | Send DAC to random addresses |
| 5 | Stake DAC to smart contract |
| 6 | Burn DAC for QE points |
| 7 | Fetch & display profile info |
| 8 | Wait 8 hours, repeat |

---

## ⚠️ Disclaimer

This bot is for **educational and testnet purposes only**. Use at your own risk. Never use real funds or mainnet private keys.

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

<p align="center">Made with ❤️ by <b>FEBRIYAN</b></p>
