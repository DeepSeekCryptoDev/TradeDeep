import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.trading_utils import initiate_trade, initiate_withdrawal
from utils.blockchain_utils import generate_ethereum_address, generate_solana_address
from .rugcheck_scraper import fetch_token_data, analyze_token

# Load the Telegram API key
API_KEY = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(API_KEY)

# Keep track of user states
user_states = {}

def create_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Generate ETH Address", callback_data="generate_eth"),
        InlineKeyboardButton("Generate SOL Address", callback_data="generate_sol")
    )
    keyboard.row(
        InlineKeyboardButton("🔜 Trade", callback_data="none",),   # callback_data="trade"
        InlineKeyboardButton("🔜 Withdraw", callback_data="none"), # callback_data="withdraw"
        InlineKeyboardButton("Analyze", callback_data="analyze")
    )
    return keyboard

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    try:
        welcome_text = f"""<a href="https://i.ibb.co/DDbXnhJL/banner.png">&#8205;</a> TradeDeep is a powerful and modular bot designed for crypto enthusiasts. It provides token analysis, social activity tracking, and trading functionality via Telegram, all while leveraging the BonkBot API for seamless trades and withdrawals. Built with scalability and ease of use in mind, TradeDeep helps users stay ahead in the ever-evolving crypto space. TradeDeep was created exclusively using DeepSeek.

<u><b>Usage</b></u>:

<b>Generate ETH Address</b>: Generate an Ethereum address.
<b>Generate SOL Address</b>: Generate a Solana address.
<b>Trade</b>: Coming soon.
<b>Withdraw</b>: Coming soon.
<b>Analyze</b>: Run token analysis on demand.        
        """
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='HTML',
            reply_markup=create_main_keyboard()
        )
    except Exception as e:
        bot.reply_to(
            message,
            f"Error displaying welcome message: {e}"
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "generate_eth":
            eth_address = generate_ethereum_address()
            bot.send_message(
                call.message.chat.id,
                f"Ethereum Address: {eth_address['address']}\nPrivate Key: {eth_address['private_key']}"
            )
        
        elif call.data == "generate_sol":
            sol_address = generate_solana_address()
            bot.send_message(
                call.message.chat.id,
                f"Solana Address: {sol_address['address']}\nPrivate Key: {sol_address['private_key']}"
            )
        
        elif call.data == "trade":
            user_states[call.message.chat.id] = "trade"
            bot.send_message(
                call.message.chat.id,
                "Send token name and amount in format: token_name amount (e.g., ETH 10)"
            )
        
        elif call.data == "withdraw":
            user_states[call.message.chat.id] = "withdraw"
            bot.send_message(
                call.message.chat.id,
                "Send address and amount in format: address amount"
            )
        
        elif call.data == "analyze":
            user_states[call.message.chat.id] = "analyze"
            bot.send_message(
                call.message.chat.id,
                "Please send the contract address to analyze:"
            )
        
        # Remove the "loading" state from the button
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        bot.send_message(
            call.message.chat.id,
            f"Error processing request: {e}"
        )
        user_states.pop(call.message.chat.id, None)

@bot.message_handler(func=lambda msg: True)
def handle_text(msg):
    try:
        chat_id = msg.chat.id
        current_state = user_states.get(chat_id)
        
        if current_state == "trade":
            try:
                token, amount = msg.text.split()
                response = initiate_trade(token, float(amount))
                bot.reply_to(msg, response)
                user_states.pop(chat_id, None)
            except ValueError:
                bot.reply_to(msg, "Invalid trade format. Please use: token_name amount")
            except Exception as e:
                bot.reply_to(msg, f"Error processing trade: {e}")
                user_states.pop(chat_id, None)
        
        elif current_state == "withdraw":
            try:
                address, amount = msg.text.split()
                response = initiate_withdrawal(address, float(amount))
                bot.reply_to(msg, response)
                user_states.pop(chat_id, None)
            except ValueError:
                bot.reply_to(msg, "Invalid withdrawal format. Please use: address amount")
            except Exception as e:
                bot.reply_to(msg, f"Error processing withdrawal: {e}")
                user_states.pop(chat_id, None)
        
        elif current_state == "analyze":
            try:
                contract_address = msg.text.strip()
                data = fetch_token_data(contract_address)
                if data:
                    token_analysis = analyze_token(data)
                    if token_analysis:
                        analysis_message = f"""
🔍 Token Analysis Report:

📝 Basic Information:
- Name: {token_analysis['token_name']}
- Symbol: {token_analysis['token_symbol']}
- Contract: {token_analysis['contract_address']}

🔒 Security Metrics:
- Safety Score: {token_analysis['safety_score']}

⚙️ Contract Features:
- Mintable: {'⚠️' if token_analysis['mintable'] else '✅'}
- Pausable: {'⚠️' if token_analysis['pausable'] else '✅'}
"""
                        bot.reply_to(msg, analysis_message)
                    else:
                        bot.reply_to(msg, "⚠️ Warning: This token did not pass our safety checks. Trading not recommended.")
                else:
                    bot.reply_to(msg, "❌ Error: Unable to fetch token data. Please try again.")
                user_states.pop(chat_id, None)
            except Exception as e:
                bot.reply_to(msg, f"Error analyzing token: {e}")
                user_states.pop(chat_id, None)
        
        else:
            bot.reply_to(
                msg,
                "Please use /start or /help to see available commands."
            )
    
    except Exception as e:
        bot.reply_to(
            msg,
            f"Error processing request: {e}"
        )
        user_states.pop(chat_id, None)

def setup_bot():
    try:
        # Check if API key is set
        if not API_KEY:
            raise ValueError("TELEGRAM_API_KEY environment variable is not set")
        
        print("Bot setup completed successfully")
        return True
    
    except Exception as e:
        print(f"Error during setup: {e}")
        return False

if __name__ == "__main__":
    if setup_bot():
        print("Starting TradeDeep bot...")
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Critical error: {e}")
    else:
        print("Bot setup failed, please check the errors above")
