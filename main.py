#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized, TimedOut
from time import sleep
import os
from time import time
from src.entry import entry, syncSheetData  # , user_log
from src.gsheets_main import upload_to_sheets
import sys
import traceback

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    logging.error("Bot credentials not found in environment")

# How long the container exist
LIFESPAN = 7200


def main():
    """Run the bot."""
    syncSheetData()
    try:
        update_id = int(os.environ["UPDATE_ID"])
    except:
        update_id = 0

    start_time = int(time())

    bot = telegram.Bot(BOT_TOKEN)

    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=10):
                update_id = update.update_id + 1
                logging.info(f"Update ID:{update_id}")
                entry(bot, update)
        except NetworkError as e:
            print("Network Error")
            print(e)
            traceback.print_exc()
            logging.error(update)
            sleep(1)
        except Unauthorized:
            print("Unauthorized")
            logging.error(update)
            # The user has removed or blocked the bot.
            # update_id += 1
        except TimedOut:
            logging.error("Timeout")
            traceback.print_exc()
            sleep(5)
        except Exception as e:
            logging.error("Generic Error")
            logging.error(e)
            logging.info("uploading pending stuff")
            # upload_to_sheets(user_log)
            traceback.print_exc()
            sleep(5)
            sys.exit("End program with error")
        if int(time()) - start_time > LIFESPAN:
            logging.info("uploading pending stuff")
            # upload_to_sheets(user_log)
            logging.info("Enough for the day! Passing on to next Meeseek")
            with open("/tmp/update_id", "w") as the_file:
                the_file.write(str(update_id))
            break


if __name__ == "__main__":
    main()
