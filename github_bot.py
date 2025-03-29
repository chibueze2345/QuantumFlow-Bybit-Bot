import os
import sys
import json
import logging
import time
from datetime import datetime, timezone
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from config import get_current_config
from storage import BotStorage

# ... (keep existing logging setup) ...

class QuantumFlowBot:
    def __init__(self):
        # ... (keep existing initialization) ...
        self.running = False
    
    # ... (keep existing command methods) ...

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
            
            # Run the bot
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Bot error: {str(e)}")
            raise
        finally:
            self.running = False
            if self.app.running:
                await self.app.stop()
            logger.info("Bot stopped successfully")

async def main():
    bot = None
    try:
        bot = QuantumFlowBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        if bot and bot.running:
            await bot.app.stop()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")