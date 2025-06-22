# run_bot.py

import os
import sys
import json
import logging
from pydantic import ValidationError, TypeAdapter
import argparse

from input_validation import OrderInput
from bot import BasicBot

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def build_parser():
    parser = argparse.ArgumentParser(
        prog="run_bot.py",
        description="Binance Trading Bot CLI",
        epilog=(
            "Examples:\n"
            "  python run_bot.py market --symbol BTCUSDT --qty 0.001\n"
            "  python run_bot.py limit --symbol BTCUSDT --qty 0.001 --limit-price 28000\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="type", required=True,help="Order type")

    # common input args
    def add_common_args(p):
        p.add_argument("--symbol", "-s", required=True, help="Trading pair, e.g. BTCUSDT")
        p.add_argument("--side", choices=["BUY", "SELL"], default="BUY", help="Order side (default: BUY)")
        p.add_argument("--qty", "-q", type=float, required=True, help="Quantity to trade")

    # market order
    spm = subparsers.add_parser("market", help="Place a  MARKET order")
    add_common_args(spm)

    # limit order
    spl = subparsers.add_parser("limit", help="Place a  LIMIT order")
    add_common_args(spl)
    spl.add_argument("--limit-price", "-l", type=float, required=True, help="Price for your LIMIT order")
    #stop order
    sps = subparsers.add_parser("stop", help="Place a  STOP order")
    add_common_args(sps)
    sps.add_argument("--stop-price", "-sp", type=float, required=True,help="Stop price for your STOP order")
   

 
    #TWAP
    twap = subparsers.add_parser("twap", help="Execute a TWAP (Time Weighted Average Price) order")
    add_common_args(twap)
    twap.add_argument("--start-time", "-st", type=str, required=True, )
    twap.add_argument("--end-time", "-et", type=str, required=True)
    twap.add_argument("--slices", "-n", type=int, required=True)
    # GRID
    grid = subparsers.add_parser("grid", help="Execute a GRID trading strategy")
    add_common_args(grid)
    grid.add_argument("--lower-price", "-lp", type=float, required=True)
    grid.add_argument("--upper-price", "-up", type=float, required=True)
    grid.add_argument("--levels", "-g", type=int, required=True)


    return parser

def parse_and_validate():
    parser = build_parser()
    args = parser.parse_args()
    cli_args = vars(args)

    # Map limit-price to price for Pydantic model
    cli_args["type"] = cli_args["type"].upper()
    if "limit_price" in cli_args:
        cli_args["price"] = cli_args.pop("limit_price")
    if "stop_price" in cli_args:
        cli_args["stop_price"] = cli_args.pop("stop_price")

    # Insert SPOT market type directly
    cli_args["market"] = "FUTURES"

    try:
        # return OrderInput(**cli_args)
        return TypeAdapter(OrderInput).validate_python(cli_args)
    except ValidationError as e:
        print(" Invalid input:\n Please provide with correct set of inputs", e)
        sys.exit(1)

def main():
    inp = parse_and_validate()
    bot = BasicBot(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

    # Dispatch
    if inp.type == "MARKET":
        resp = bot.market_order(inp.symbol, inp.side, inp.qty)
        
    elif inp.type == "LIMIT":
        resp = bot.limit_order(inp.symbol, inp.side, inp.qty, inp.price)
        
    elif inp.type == "STOP":
        resp = bot.stop_order(inp.symbol, inp.side, inp.qty, inp.stop_price)

    elif inp.type == "TWAP":
        resp = bot.twap_execute(
            inp.symbol, inp.side, inp.qty,
            inp.start_time, inp.end_time, inp.slices
        )
    elif inp.type == "GRID":
        resp = bot.grid_strategy(
            inp.symbol, inp.side, inp.qty,
            inp.lower_price, inp.upper_price, inp.levels
        )
    else:
        print(" Unsupported order type for :", inp.type)
        sys.exit(1)

    print(json.dumps(resp, indent=2))

if __name__ == "__main__":
    main()
