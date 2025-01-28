import os
import telebot
from utils.trading_utils import initiate_trade, initiate_withdrawal
from utils.blockchain_utils import generate_ethereum_address, generate_solana_address

# Load the Telegram API key
API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /generate_eth, /generate_sol, /trade, or /withdraw to interact with the bot.")

@bot.message_handler(commands=["generate_eth"])
def generate_eth_address(message):
    eth_address = generate_ethereum_address()
    bot.reply_to(message, f"Ethereum Address: {eth_address['address']}\nPrivate Key: {eth_address['private_key']}")

@bot.message_handler(commands=["generate_sol"])
def generate_sol_address(message):
    sol_address = generate_solana_address()
    bot.reply_to(message, f"Solana Address: {sol_address['address']}\nPrivate Key: {sol_address['private_key']}")

@bot.message_handler(commands=["trade"])
def trade(message):
    bot.reply_to(message, "Send token name and amount in format: token_name amount (e.g., ETH 10)")

    @bot.message_handler(func=lambda msg: True)
    def handle_trade(msg):
        try:
            token, amount = msg.text.split()
            response = initiate_trade(token, float(amount))
            bot.reply_to(msg, response)
        except Exception as e:
            bot.reply_to(msg, f"Error processing trade: {e}")

@bot.message_handler(commands=["withdraw"])
def withdraw(message):
    bot.reply_to(message, "Send address and amount in format: address amount")

    @bot.message_handler(func=lambda msg: True)
    def handle_withdraw(msg):
        try:
            address, amount = msg.text.split()
            response = initiate_withdrawal(address, float(amount))
            bot.reply_to(msg, response)
        except Exception as e:
            bot.reply_to(msg, f"Error processing withdrawal: {e}")

if __name__ == "__main__":
    bot.polling()
