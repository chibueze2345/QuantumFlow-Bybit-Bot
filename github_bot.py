"""
QuantumFlow Elite Bybit Bot - Main Bot File
Last Updated: 2025-03-29 19:07:51 UTC
Author: chibueze2345
Version: 2.1.1
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
        # Bot metadata
        self.VERSION = '2.1.1'
        self.CREATOR = 'chibueze2345'
        self.LAST_UPDATED = '2025-03-29 19:07:51'
        
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
        
        # Add running flag
        self.running = False
        
        # Initialize application to None
        self.app = None
        
        # Initialize event loop
        self.loop = None

    async def initialize(self):
        """Initialize the bot application"""
        try:
            self.app = Application.builder().token(self.telegram_token).build()
            await self.app.initialize()
            self.register_commands()
            logger.info("Bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            raise

    def register_commands(self):
        """Register all command handlers"""
        if not self.app:
            raise RuntimeError("Application not initialized")
            
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

    async def shutdown(self):
        """Gracefully shutdown the bot"""
        logger.info("Initiating bot shutdown...")
        self.running = False
        
        if self.app:
            try:
                await self.app.stop()
                await self.app.shutdown()
                logger.info("Bot stopped successfully")
            except Exception as e:
                logger.error(f"Error during shutdown: {str(e)}")
        
    async def run(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            self.running = True
            
            # Initialize the application
            await self.initialize()
            
            # Set up signal handlers
            for sig in (signal.SIGINT, signal.SIGTERM):
                self.loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(self.handle_signal(s)))
            
            # Start the application
            await self.app.start()
            
            # Run until stopped
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}")
            raise
        finally:
            await self.shutdown()

    async def handle_signal(self, signal):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signal.name}...")
        await self.shutdown()

    def start(self):
        """Entry point to start the bot"""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.run())
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            sys.exit(1)
        finally:
            try:
                if self.loop and not self.loop.is_closed():
                    self.loop.close()
            except Exception as e:
                logger.error(f"Error closing event loop: {str(e)}")

if __name__ == "__main__":
    bot = QuantumFlowBot()
    bot.start()