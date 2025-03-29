import os
import sys
import json
import signal
import logging
import time
from datetime import datetime, timezone
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from config import get_current_config
from storage import BotStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class QuantumFlowBot:
    def __init__(self):
        # Bot metadata
        self.VERSION = '2.1.0'
        self.CREATOR = 'chibueze2345'
        self.LAST_UPDATED = '2025-03-29 18:13:19'
        
        # Initialize bot configuration
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not self.telegram_token or not self.telegram_chat_id:
            raise ValueError("Telegram credentials not found in environment variables!")
        
        # Initialize Telegram application
        self.app = Application.builder().token(self.telegram_token).build()
        
        # Initialize storage
        self.storage = BotStorage()
        
        # Initialize state
        self.state = {
            'balance': 0.0,
            'positions': {},
            'daily_trades': 0,
            'pnl': 0.0,
            'last_update': self.LAST_UPDATED
        }
        
        # Add running flag
        self.running = False
        
        # Register command handlers
        self.register_commands()

    def register_commands(self):
        """Register all command handlers"""
        commands = [
            ('start', self.cmd_start, 'Start the bot'),
            ('balance', self.cmd_balance, 'Check balance'),
            ('status', self.cmd_status, 'Check status'),
            ('positions', self.cmd_positions, 'View positions'),
            ('help', self.cmd_help, 'Show help'),
            ('version', self.cmd_version, 'Show version info')
        ]
        
        for command, handler, description in commands:
            self.app.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered command: /{command}")

    async def cmd_version(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /version command"""
        message = (
            "🤖 *QuantumFlow Elite Bot Version Info*\n\n"
            f"Version: {self.VERSION}\n"
            f"Creator: @{self.CREATOR}\n"
            f"Last Updated: {self.LAST_UPDATED} UTC\n"
            f"Current Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = (
            "🤖 *Welcome to QuantumFlow Elite Bot*\n\n"
            f"Version: {self.VERSION}\n"
            f"Last Updated: {self.LAST_UPDATED} UTC\n\n"
            "Available commands:\n"
            "/balance - Check your balance\n"
            "/status - View current status\n"
            "/positions - View open positions\n"
            "/version - Show version info\n"
            "/help - Show this help message\n\n"
            "Bot Status: Active ✅"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def cmd_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command"""
        balance = self.state.get('balance', 0.0)
        message = (
            "💰 *Balance Information*\n\n"
            f"Current Balance: ${balance:,.2f}\n"
            f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        status = {
            'time': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            'balance': self.state.get('balance', 0.0),
            'positions': len(self.state.get('positions', {})),
            'daily_trades': self.state.get('daily_trades', 0),
            'pnl': self.state.get('pnl', 0.0)
        }
        
        message = (
            "📊 *Current Status*\n\n"
            f"🕒 Time: {status['time']} UTC\n"
            f"💰 Balance: ${status['balance']:,.2f}\n"
            f"📈 Open Positions: {status['positions']}\n"
            f"🎯 Today's Trades: {status['daily_trades']}\n"
            f"📗 P/L: ${status['pnl']:,.2f}"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def cmd_positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /positions command"""
        positions = self.state.get('positions', {})
        
        if not positions:
            await update.message.reply_text("📈 No open positions currently.")
            return
            
        message = "📊 *Open Positions*\n\n"
        for symbol, pos in positions.items():
            message += (
                f"*{symbol}*\n"
                f"Side: {pos.get('side', 'N/A')}\n"
                f"Size: {pos.get('size', 0)}\n"
                f"Entry: ${pos.get('entry_price', 0):,.2f}\n\n"
            )
        
        await update.message.reply_text(message, parse_mode='Markdown')

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            "🤖 *QuantumFlow Elite Bot Help*\n\n"
            "*Available Commands:*\n"
            "/start - Start the bot\n"
            "/balance - Check your balance\n"
            "/status - View current status\n"
            "/positions - View open positions\n"
            "/version - Show version info\n"
            "/help - Show this help message\n\n"
            "For support, contact: @chibueze2345"
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')

    async def run(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            self.running = True
            await self.app.initialize()
            await self.app.start()
            
            # Send startup message
            await self.app.bot.send_message(
                chat_id=self.telegram_chat_id,
                text=f"🚀 QuantumFlow Elite Bot v{self.VERSION} is now online!\n"
                     f"Last Updated: {self.LAST_UPDATED} UTC",
                parse_mode='Markdown'
            )
            
            # Run the bot
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
            
        except Exception as e:
            logger.error(f"Bot error: {str(e)}")
            raise
        finally:
            self.running = False
            if hasattr(self, 'app') and self.app.running:
                await self.app.stop()
            logger.info("Bot stopped successfully")

def setup_signal_handlers(bot):
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}")
        if bot.running:
            logger.info("Initiating graceful shutdown...")
            bot.running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    bot = None
    try:
        bot = QuantumFlowBot()
        setup_signal_handlers(bot)
        await bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        if bot and bot.running and hasattr(bot, 'app'):
            try:
                await bot.app.stop()
            except Exception as stop_error:
                logger.error(f"Error during shutdown: {stop_error}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")