"""
QuantumFlow Elite Bybit Bot - Main Bot File
Last Updated: 2025-03-29 19:12:43 UTC
Author: chibueze2345
Version: 2.1.1
"""

import os
import sys
import logging
import asyncio
from datetime import datetime, timezone
from telegram.ext import Application, CommandHandler
from config import get_current_config
from storage import BotStorage
from commands import (
    cmd_start,
    cmd_balance,
    cmd_status,
    cmd_positions,
    cmd_help
)

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
        self.VERSION = '2.1.1'
        self.CREATOR = 'chibueze2345'
        self.LAST_UPDATED = '2025-03-29 19:12:43'
        
        # Initialize bot configuration
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables!")
        
        # Initialize storage
        self.storage = BotStorage()
        
        # Initialize application
        self.app = None
        self.running = False
        
        # Load configuration
        self.config = get_current_config()
        
        # Initialize state
        self.state = {
            'balance': 0.0,
            'positions': {},
            'daily_trades': 0,
            'pnl': 0.0,
            'last_update': self.LAST_UPDATED
        }

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
        """Register command handlers"""
        if not self.app:
            raise RuntimeError("Application not initialized")
        
        # Register commands
        commands = [
            ('start', cmd_start),
            ('balance', cmd_balance),
            ('status', cmd_status),
            ('positions', cmd_positions),
            ('help', cmd_help)
        ]
        
        for command, handler in commands:
            self.app.add_handler(CommandHandler(command, handler))
            logger.info(f"Registered command: /{command}")

    async def start(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            self.running = True
            
            # Initialize the application
            await self.initialize()
            
            # Start the application
            await self.app.start()
            
            # Keep the bot running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error running bot: {str(e)}")
            raise
        finally:
            await self.shutdown()

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

def main():
    """Main entry point"""
    bot = QuantumFlowBot()
    
    # Set up asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
    finally:
        loop.run_until_complete(bot.shutdown())
        loop.close()

if __name__ == "__main__":
    main()