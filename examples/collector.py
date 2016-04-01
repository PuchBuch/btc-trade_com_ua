import os
os.sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from peewee import SqliteDatabase

from btctradeapi import config
config.DB = SqliteDatabase('collector.db')

from workers.collector import InfoCollector
from app.models import Deals, Deal, User, Buy, BuyItem, Sell, SellItem, CycleIterationStateSnapshot


def create_models():
    config.DB.create_tables(
        [Deal, Deals, User, BuyItem, Buy, SellItem, Sell, CycleIterationStateSnapshot],
        safe=True
    )


def main():
    import signal
    import time
    create_models()
    info_collector = InfoCollector('btc_uah')

    def sigterm_handler(_signo, _stack_frame):
        # Raises SystemExit(0):
        print "signal was arrived..."
        info_collector.alive = False
        info_collector.join()
        os.sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    info_collector.start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

