import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import requests
from eth_account import Account
from itertools import cycle
from web3 import Web3
import urllib3

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
Account.enable_unaudited_hdwallet_features()

init(autoreset=True)

class DachainBot:
    def __init__(self):
        self.private_keys = self.load_file('accounts.txt')
        self.proxies_list = self.load_file('proxy.txt')
        self.rpc_url = "https://rpctest.dachain.tech"
        self.chain_id = 21894
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.smart_contract = self.w3.to_checksum_address("0x3691A78bE270dB1f3b1a86177A8f23F89A8Cef24")
        self.stake_method_id = "0x3a4b66f1"
        self.burn_method_id = "0x4a5d094b"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    
    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}DACHAIN BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=1, max_sec=5):
        delay = random.randint(min_sec, max_sec)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def fetch_with_retry(self, session, method, url, headers, payload=None, retries=3):
        for attempt in range(retries):
            try:
                if method == "GET":
                    response = session.get(url, headers=headers, timeout=30, verify=False)
                else:
                    response = session.post(url, headers=headers, json=payload, timeout=30, verify=False)
                return response
            except requests.exceptions.Timeout:
                self.log(f"Request timed out (Attempt {attempt+1}/{retries}). Retrying...", "WARNING")
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                self.log(f"Network error: {e}", "WARNING")
                time.sleep(2)
        return None

    def run(self):
        self.print_banner()
        
        choice = self.show_menu()

        try:
            send_input = input(f"{Fore.GREEN}How many send transactions per account? (0 to skip): {Style.RESET_ALL}")
            send_count = int(float(send_input))
        except ValueError:
            send_count = 0
            
        try:
            stake_input = input(f"{Fore.GREEN}How much DAC to STAKE per account? (0 to skip): {Style.RESET_ALL}")
            amount_to_stake_eth = float(stake_input)
            if amount_to_stake_eth < 0: amount_to_stake_eth = 0.0
        except ValueError:
            amount_to_stake_eth = 0.0

        try:
            burn_input = input(f"{Fore.GREEN}How much DAC to BURN for QE per account? (0 to skip): {Style.RESET_ALL}")
            amount_to_burn_eth = float(burn_input)
            if amount_to_burn_eth < 0: amount_to_burn_eth = 0.0
        except ValueError:
            amount_to_burn_eth = 0.0

        if choice == '1':
            self.log("Running with proxy", "INFO")
            proxy_pool = cycle(self.proxies_list) if self.proxies_list else None
        else:
            self.log("Running without proxy", "INFO")
            proxy_pool = None
            
        if not self.private_keys:
            self.log("No private keys found in accounts.txt", "ERROR")
            return
            
        self.log(f"Loaded {len(self.private_keys)} accounts successfully", "INFO")
        
        if not self.w3.is_connected():
            self.log("Could not connect to DAC Testnet RPC", "WARNING")

        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle_count = 1
        while True:
            self.log(f"Cycle #{cycle_count} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(self.private_keys)
            
            for index, pk in enumerate(self.private_keys, start=1):
                try:
                    account = Account.from_key(pk)
                    wallet_address = account.address
                    
                    self.log(f"Account #{index}/{total_accounts}", "INFO")
                    
                    proxy_dict = None
                    if proxy_pool:
                        current_proxy = next(proxy_pool)
                        proxy_dict = {"http": current_proxy, "https": current_proxy}
                        self.log(f"Proxy: {current_proxy}", "INFO")
                    else:
                        self.log("Proxy: No Proxy", "INFO")

                    self.log(f"Wallet: {wallet_address}", "INFO")

                    session = requests.Session()
                    if proxy_dict:
                        session.proxies.update(proxy_dict)

                    self.log("Fetching CSRF Token & Logging in...", "INFO")
                    
                    base_headers = {
                        "accept": "application/json",
                        "accept-language": "en-US,en;q=0.9",
                        "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"Windows"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "user-agent": self.user_agent
                    }
                    
                    csrf_headers = base_headers.copy()
                    csrf_headers["referer"] = "https://inception.dachain.io/"
                    
                    csrf_token = None
                    
                    try:
                        resp_csrf = session.get("https://inception.dachain.io/csrf/", headers=csrf_headers, timeout=15, verify=False)
                        if resp_csrf.status_code == 200:
                            csrf_token = session.cookies.get('csrftoken')
                    except Exception as e:
                        self.log(f"Error fetching CSRF: {e}", "WARNING")
                    
                    if csrf_token:
                        login_headers = base_headers.copy()
                        login_headers["content-type"] = "application/json"
                        login_headers["origin"] = "https://inception.dachain.io"
                        login_headers["referer"] = "https://inception.dachain.io/"
                        login_headers["x-csrftoken"] = csrf_token
                        
                        login_payload = {"wallet_address": wallet_address.lower()}
                        
                        try:
                            response = session.post("https://inception.dachain.io/api/auth/wallet/", headers=login_headers, json=login_payload, timeout=20, verify=False)
                            
                            if response.status_code == 200:
                                try:
                                    resp_json = response.json()
                                    if resp_json.get("success"):
                                        self.log("Login successful!", "SUCCESS")
                                        
                                        self.log("Processing Faucet Claim...", "INFO")
                                        self.random_delay(2, 4)
                                        
                                        faucet_headers = login_headers.copy()
                                        faucet_headers["referer"] = "https://inception.dachain.io/faucet"
                                        
                                        try:
                                            faucet_resp = session.post("https://inception.dachain.io/api/inception/faucet/", headers=faucet_headers, timeout=20, verify=False)
                                            if faucet_resp.status_code in [200, 201]:
                                                if faucet_resp.json().get("success"):
                                                    self.log("Faucet Claim Success! Reward dispensed.", "SUCCESS")
                                                    time.sleep(5)
                                                else:
                                                    self.log("Faucet claim skipped or limit reached.", "WARNING")
                                            else:
                                                self.log("Faucet failed or already claimed.", "WARNING")
                                        except Exception as e:
                                            self.log(f"Faucet error: {e}", "WARNING")

                                        if (send_count > 0 or amount_to_stake_eth > 0 or amount_to_burn_eth > 0) and self.w3.is_connected():
                                            self.log("Executing On-Chain Transactions...", "INFO")
                                            try:
                                                amount_to_send_eth = 0.0001
                                                amount_to_send_wei = self.w3.to_wei(amount_to_send_eth, 'ether')
                                                
                                                amount_to_stake_wei = self.w3.to_wei(amount_to_stake_eth, 'ether') if amount_to_stake_eth > 0 else 0
                                                amount_to_burn_wei = self.w3.to_wei(amount_to_burn_eth, 'ether') if amount_to_burn_eth > 0 else 0
                                                
                                                balance_wei = self.w3.eth.get_balance(wallet_address)
                                                total_needed_wei = (amount_to_send_wei * send_count) + amount_to_stake_wei + amount_to_burn_wei
                                                
                                                if balance_wei <= total_needed_wei:
                                                    self.log(f"Low Balance! Current: {self.w3.from_wei(balance_wei, 'ether')} DAC", "WARNING")
                                                
                                                nonce = self.w3.eth.get_transaction_count(wallet_address)
                                                gas_price = self.w3.eth.gas_price
                                                
                                                if send_count > 0:
                                                    for i in range(send_count):
                                                        random_address = Account.create().address
                                                        tx_send = {
                                                            'nonce': nonce, 'to': random_address, 'value': amount_to_send_wei,
                                                            'gas': 21000, 'gasPrice': gas_price, 'chainId': self.chain_id
                                                        }
                                                        signed_tx = self.w3.eth.account.sign_transaction(tx_send, pk)
                                                        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                                                        tx_hash_hex = self.w3.to_hex(tx_hash)
                                                        self.log(f"SEND [{i+1}/{send_count}] Successfully transferred {amount_to_send_eth} DAC", "SUCCESS")
                                                        self.log(f"Tx Hash: https://exptest.dachain.tech/tx/{tx_hash_hex}", "INFO")
                                                        nonce += 1
                                                        time.sleep(1)

                                                if amount_to_stake_eth > 0:
                                                    tx_stake = {
                                                        'nonce': nonce, 'to': self.smart_contract, 'value': amount_to_stake_wei,
                                                        'gas': 150000, 'gasPrice': gas_price, 'chainId': self.chain_id, 'data': self.stake_method_id
                                                    }
                                                    signed_tx = self.w3.eth.account.sign_transaction(tx_stake, pk)
                                                    tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                                                    tx_hash_hex = self.w3.to_hex(tx_hash)
                                                    self.log(f"STAKE | Successfully staked {amount_to_stake_eth} DAC", "SUCCESS")
                                                    self.log(f"Tx Hash: https://exptest.dachain.tech/tx/{tx_hash_hex}", "INFO")
                                                    nonce += 1
                                                    time.sleep(1)

                                                if amount_to_burn_eth > 0:
                                                    tx_burn = {
                                                        'nonce': nonce, 'to': self.smart_contract, 'value': amount_to_burn_wei,
                                                        'gas': 100000, 'gasPrice': gas_price, 'chainId': self.chain_id, 'data': self.burn_method_id
                                                    }
                                                    signed_tx = self.w3.eth.account.sign_transaction(tx_burn, pk)
                                                    tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                                                    tx_hash_hex = self.w3.to_hex(tx_hash)
                                                    self.log(f"BURN | Successfully burned {amount_to_burn_eth} DAC for QE", "SUCCESS")
                                                    self.log(f"Tx Hash: https://exptest.dachain.tech/tx/{tx_hash_hex}", "INFO")
                                                    nonce += 1
                                                    time.sleep(1)

                                            except Exception as e:
                                                self.log(f"Web3 Error: {e}", "ERROR")

                                        self.log("Fetching Profile...", "INFO")
                                        profile_headers = base_headers.copy()
                                        profile_headers["referer"] = "https://inception.dachain.io/activity"
                                        
                                        profile_resp = self.fetch_with_retry(session, "GET", "https://inception.dachain.io/api/inception/profile/", profile_headers)
                                        if profile_resp and profile_resp.status_code == 200:
                                            try:
                                                p_data = profile_resp.json()
                                                u_name = p_data.get("username", "Unknown")
                                                u_rank = p_data.get("user_rank", "N/A")
                                                u_qe = p_data.get("qe_balance", 0)
                                                u_dacc = p_data.get("dacc_balance", "0")
                                                u_tx = p_data.get("tx_count", 0)
                                                
                                                self.log(f"Username : {u_name}", "SUCCESS")
                                                self.log(f"Rank     : {u_rank}", "SUCCESS")
                                                self.log(f"QE       : {u_qe}", "SUCCESS")
                                                self.log(f"DACC     : {u_dacc}", "SUCCESS")
                                                self.log(f"Tx Count : {u_tx}", "SUCCESS")
                                            except Exception:
                                                self.log("Failed to parse profile JSON.", "WARNING")
                                        else:
                                            self.log("Failed to fetch profile.", "WARNING")
                                            
                                    else:
                                        self.log("Login failed: Success response is false.", "ERROR")
                                except Exception:
                                    self.log("Login failed (Invalid JSON received).", "ERROR")
                            else:
                                self.log(f"Login request failed with status {response.status_code}.", "ERROR")
                        except Exception as e:
                            self.log(f"Login request timed out or failed: {e}", "ERROR")
                    else:
                        self.log("Failed to get CSRF Token. Proceeding to On-Chain tasks.", "ERROR")

                    success_count += 1
                    
                except Exception as e:
                    self.log(f"Process Error: {e}", "ERROR")

                if index < total_accounts:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle_count} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle_count += 1
            self.countdown(28800)

if __name__ == "__main__":
    bot = DachainBot()
    bot.run()
