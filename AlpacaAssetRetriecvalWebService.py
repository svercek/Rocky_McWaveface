import logging
from typing import List, Tuple
from alpaca.trading.client import TradingClient
from alpaca.trading.models import Asset
from alpaca.common.exceptions import APIError, APIConnectionError
from alpaca.markets import Exchange

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def get_list_assets(
    trading_client: TradingClient, 
    exchange: Exchange
) -> Tuple[List[Asset], int]:
    """
    Retrieve a list of active US equity assets for a specific exchange.

    Args:
        trading_client (TradingClient): Authenticated Alpaca Trading Client
        exchange (Exchange): Specific market exchange to filter assets

    Returns:
        Tuple[List[Asset], int]: 
        - First element: List of matching assets
        - Second element: Status code (0 for success, other values for errors)
    """
    try:
        # Validate input parameters
        if not trading_client:
            logger.error("Invalid trading client: None provided")
            return [], 3
        
        # Retrieve assets with specific filtering
        assets = await trading_client.list_assets(
            asset_class='us_equity',
            status='active',
            exchange=exchange.value
        )
        
        # Log successful retrieval
        logger.info(f"Successfully retrieved {len(assets)} assets from {exchange.value}")
        
        return assets, 0
    
    except APIConnectionError as conn_err:
        # Handle network-related errors
        logger.error(f"Network connectivity error: {conn_err}")
        return [], 2
    
    except APIError as api_err:
        # Handle API-specific errors
        logger.error(f"API request failed: {api_err}")
        return [], 1
    
    except Exception as unexpected_err:
        # Catch any unexpected errors
        logger.error(f"Unexpected error during asset retrieval: {unexpected_err}")
        return [], 4

# Example usage demonstration
async def main():
    """
    Demonstration of asset retrieval function.
    """
    try:
        # Initialize trading client (replace with actual credentials)
        trading_client = TradingClient(
            key_id='YOUR_API_KEY', 
            secret_key='YOUR_SECRET_KEY', 
            paper=True
        )
        
        # Retrieve assets from NASDAQ
        assets, status_code = await get_list_assets(
            trading_client, 
            Exchange.NASDAQ
        )
        
        if status_code == 0:
            print(f"Retrieved {len(assets)} assets")
            for asset in assets[:5]:  # Print first 5 assets
                print(f"Symbol: {asset.symbol}, Name: {asset.name}")
        else:
            print(f"Failed to retrieve assets. Status code: {status_code}")
    
    except Exception as e:
        print(f"Error in main execution: {e}")

# Ensure proper async execution
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())