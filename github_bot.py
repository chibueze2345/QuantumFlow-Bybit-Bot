"""
QuantumFlow Elite Bybit Bot - Main Bot File
Last Updated: 2025-03-29 19:00:46 UTC
Author: chibueze2345
Version: 2.1.0
"""

import os
import sys
import json
import signal
import logging
import time
from datetime import datetime, timezone
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
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
        self.VERSION = '2.1.0'
        self.CREATOR = 'chibueze2345'
        self.LAST_UPDATED = '2025-03-29 19:00:46'
        
        # Initialize bot configuration
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not self.telegram_token or not self.telegram_chat_id:
            raise ValueError("Telegram credentials not found in environment variables!")
        
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
        
        self.running = False
        self.app = None

    async def initialize(self):
        """Initialize the bot application"""
        try:
            self.app = Application.builder().token(self.telegram_token).build()
            await self.app.initialize()
            await self.register_commands()
            logger.info("Bot initialized successfully")
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise

    async def register_commands(self):
        """Register all command handlers"""
        if not self.app:
            raise RuntimeError("Application not initialized")
        
        # Define command handlers
        async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        async def cmd_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
            balance = self.state.get('balance', 0.0)
            message = (
                "💰 *Balance Information*\n\n"
                f"Current Balance: ${balance:,.2f}\n"
                f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            await update.message.reply_text(message, parse_mode='Markdown')

        async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        async def cmd_positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
            help_message = (
                "🤖 *QuantumFlow Elite Bot Help*\n\n"
                "*Available Commands:*\n"
                "/start - Start the bot\n"
                "/balance - Check your balance\n"
                "/status - View current status\n"
                "/positions - View open positions\n"
                "/version - Show version info\n"
                "/help - Show this help message\n\n"
                f"For support, contact: @{self.CREATOR}"
            )
            await update.message.reply_text(help_message, parse_mode='Markdown')

        async def cmd_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
            message = (
                "🤖 *QuantumFlow Elite Bot Version Info*\n\n"
                f"Version: {self.VERSION}\n"
                f"Creator: @{self.CREATOR}\n"
                f"Last Updated: {self.LAST_UPDATED} UTC\n"
                f"Current Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            await update.message.reply_text(message, parse_mode='Markdown')

        # Register commands
        commands = [
            ('start', cmd_start),
            ('balance', cmd_balance),
            ('status', cmd_status),
            ('positions', cmd_positions),
            ('help', cmd_help),
            ('version', cmd_version)
        ]
        
        for command, handler in commands:
            self.app.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered command: /{command}")

    async def run(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            self.running = True
            
            # Initialize the application
            await self.initialize()
            
            # Start the application
            await self.app.start()
            
            # Send startup message
            await self.app.bot.send_message(
                chat_id=self.telegram_chat_id,
                text=f"🚀 QuantumFlow Elite Bot v{self.VERSION} is now online!\n"
                     f"Last Updated: {self.LAST_UPDATED} UTC",
                parse_mode='Markdown'
            )
            
            # Run the bot
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Bot error: {str(e)}")
            raise
        finally:
            self.running = False
            if self.app:
                await self.app.stop()
            logger.info("Bot stopped successfully")

async def main():
    """Main entry point"""
    bot = None
    try:
        bot = QuantumFlowBot()
        
        # Setup signal handlers
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}")
            if bot.running:
                logger.info("Initiating graceful shutdown...")
                bot.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Run the bot
        await bot.run()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        if bot and bot.running and bot.app:
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