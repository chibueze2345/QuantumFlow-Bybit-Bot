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

# Your existing logging setup remains the same
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
    # All your existing methods remain the same until the run method
    # Only changing the run method and main function to fix the event loop issue
    
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
                text="🚀 Bot is now online and ready!",
                parse_mode='Markdown'
            )
            
            # Run the bot with close_loop=False to prevent the error
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
            
        except Exception as e:
            logger.error(f"Bot error: {str(e)}")
            raise
        finally:
            self.running = False
            if self.app.running:
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
        if bot and bot.running:
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