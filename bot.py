import  sys, logging
import math
from binance.exceptions import BinanceAPIException
from binance.client import Client
import datetime, time
from datetime import timezone

logger=logging.basicConfig(
    filename='binance_order.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class BasicBot:
    def __init__(self ,api_key, api_secret):
        self.client = Client(api_key, api_secret , testnet=True)
        #Spot URL for testnet
        #self.client.API_URL = 'https://testnet.binance.vision/api'
        #Futures URL for testnet
        self.client.FUTURES_URL     = 'https://testnet.binancefuture.com'
   
        
    def market_order(self ,symbol , side , qty):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=qty
            )
            logging.info(f"Order successful: {order}")
            
            return order
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)
    
    def limit_order(self ,symbol, side, qty , price ):
        if price <= 0:
            logging.error("Price must be greater than 0 for LIMIT orders")
            sys.exit(1)
        try:
            resp = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=qty,
                price=price,
                timeInForce='GTC'
            )
            logging.info(" LIMIT: %s", resp)
            return resp
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)

    def get_order(self, symbol, order_id):
        try:
            resp = self.client.get_order(
                symbol=symbol,
                orderId=order_id
            )
            logging.info("GET ORDER: %s", resp)
            return resp
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)
    def stop_order(self, symbol, side, qty, stop_price):
        try:
            resp = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_MARKET',
                quantity=qty,
                stopPrice=stop_price,
            
                timeInForce='GTC',
                reduceOnly=False
            )
            logging.info(" STOP ORDER: %s", resp)
            return resp
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)
    
    def twap_execute(self, symbol, side, total_qty, start_time, end_time, slices):
        try:
            step_size = 0.001
            
            time1 = datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00")).replace(tzinfo=None)
            time2 = datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00")).replace(tzinfo=None)
            interval = (time2 - time1) / slices
            slice_qty = math.floor((total_qty / slices) * (1/step_size)) * step_size
            orders = []
            for i in range(slices):
                target = time1 + interval*i
                while datetime.datetime.now() < target:
                    time.sleep(1)
                resp = self.market_order(symbol, side, slice_qty)
                orders.append(resp)
            logging.info(" TWAP EXECUTE: %s", orders)
            return orders
                
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)
    
    def grid_strategy(self, symbol, side, total_qty, low, high, levels):
        step = (high - low) / (levels - 1)
        qty_per_order = total_qty / levels
        orders = []
        try:
            for i in range(levels):
                price = low + i*step
                result = self.limit_order(symbol, side, qty_per_order, price)
                orders.append(result)
            logging.info(" GRID STRATEGY: %s", orders)
            return orders
        except BinanceAPIException as e:
            logging.error(f"Binance API Exception: {e.message}")
            sys.exit(1)
    