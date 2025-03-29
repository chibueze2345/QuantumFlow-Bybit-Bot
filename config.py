"""
QuantumFlow Elite Bybit Bot - Configuration
Last Updated: 2025-03-29 19:12:43 UTC
Author: chibueze2345
Version: 2.1.1
"""

import os
from datetime import datetime, timezone

# Environment Configuration
USE_TESTNET = os.getenv('USE_TESTNET', 'true').lower() == 'true'
ENV_TYPE = 'TESTNET' if USE_TESTNET else 'MAINNET'

# Bot Version
VERSION = '2.1.1'
CREATOR = 'chibueze2345'
LAST_UPDATED = '2025-03-29 19:12:43'

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

# Added missing TRADE_LIMIT_TIERS
TRADE_LIMIT_TIERS = {
    'tier1': {
        'max_position_size': 0.01,
        'max_daily_trades': 10,
        'min_balance': 0
    },
    'tier2': {
        'max_position_size': 0.05,
        'max_daily_trades': 20,
        'min_balance': 1000
    },
    'tier3': {
        'max_position_size': 0.1,
        'max_daily_trades': 30,
        'min_balance': 5000
    }
}

# Rest of your config remains the same...