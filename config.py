"""
QuantumFlow Elite Bybit Bot - Configuration
Last Updated: 2025-03-29 18:13:19 UTC
Author: chibueze2345
Version: 2.1.0
"""

import os
from datetime import datetime, timezone

# Environment Configuration
USE_TESTNET = os.getenv('USE_TESTNET', 'true').lower() == 'true'
ENV_TYPE = 'TESTNET' if USE_TESTNET else 'MAINNET'

# Bot Version
VERSION = '2.1.0'
CREATOR = 'chibueze2345'
LAST_UPDATED = '2025-03-29 18:13:19'

# API Configuration
API_CONFIG = {
    'testnet': {
        'base_url': 'https://api-testnet.bybit.com',
        'ws_url': 'wss://stream-testnet.bybit.com'
    },
    'mainnet': {
        'base_url': 'https://api.bybit.com',
        'ws_url': 'wss://stream.bybit.com'
    }
}

# Trading Parameters
TRADING_CONFIG = {
    'testnet': {
        'risk_per_trade': 0.015,    # 1.5%
        'max_daily_loss': 0.05,     # 5%
        'max_drawdown': 0.10,       # 10%
        'base_lot': 0.001,          # Micro lot
        'growth_factor': 1.15,      # Conservative scaling
        'safety_margin': 0.95,      # 95% safety
        'max_trades_per_day': 10,   # Maximum trades per day
        'spread_multiplier': 1.5    # Higher spreads in testnet
    },
    'mainnet': {
        'risk_per_trade': 0.015,
        'max_daily_loss': 0.05,
        'max_drawdown': 0.10,
        'base_lot': 0.001,
        'growth_factor': 1.15,
        'safety_margin': 0.95,
        'max_trades_per_day': 20,
        'spread_multiplier': 1.0
    }
}

# Trading Pairs Configuration
PAIRS = {
    'EURUSD': {
        'active_hours': {'start': '06:00', 'end': '16:00'},
        'max_spread': 1.5,
        'risk_reward': 2.0,
        'min_volume': 100000
    },
    'GBPUSD': {
        'active_hours': {'start': '07:00', 'end': '15:00'},
        'max_spread': 1.8,
        'risk_reward': 2.0,
        'min_volume': 100000
    },
    'USDJPY': {
        'active_hours': {'start': '00:00', 'end': '07:00'},
        'max_spread': 1.6,
        'risk_reward': 2.0,
        'min_volume': 100000
    }
}

# Recovery System Configuration
RECOVERY_CONFIG = {
    'activate_after_losses': 3,
    'position_size_reduction': 0.5,
    'cooling_period_hours': 4,
    'max_recovery_attempts': 3
}

# Telegram Configuration
TELEGRAM_CONFIG = {
    'commands': {
        'start': 'Start the trading bot',
        'stop': 'Stop the trading bot',
        'status': 'Check current status',
        'balance': 'View account balance',
        'positions': 'View open positions',
        'trades': "View today's trades",
        'settings': 'View/modify settings',
        'risk': 'View/modify risk settings'
    },
    'notifications': {
        'trade_opened': True,
        'trade_closed': True,
        'profit_threshold': 5.0,
        'loss_threshold': -3.0,
        'balance_update': True,
        'daily_summary': True
    }
}

def get_current_config():
    env = 'testnet' if USE_TESTNET else 'mainnet'
    return {
        'environment': ENV_TYPE,
        'version': VERSION,
        'creator': CREATOR,
        'last_updated': LAST_UPDATED,
        'api': API_CONFIG[env],
        'trading': TRADING_CONFIG[env],
        'pairs': PAIRS,
        'trade_limits': TRADE_LIMIT_TIERS,
        'recovery': RECOVERY_CONFIG,
        'telegram': TELEGRAM_CONFIG
    }