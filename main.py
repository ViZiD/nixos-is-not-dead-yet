#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: with ps; [ aiohttp ])" -p pyright ruff
# Copyright (C) 2024 Radik Islamov <vizid1337@gmail.com>
# SPDX-License-Identifier: MIT

import asyncio
import datetime
import logging
import os
import sys

import aiohttp

CHANNEL_ID = os.environ.get("TG_CHANNEL_ID")
API_TOKEN = os.environ.get("TG_BOT_TOKEN")
DEBUG_USER_ID = 744956396
API_URL = "https://api.telegram.org"

LOG = logging.getLogger("dead-bot")


async def send_message(
    session,
    msg,
    chat_id,
    disable_notification=False,
):
    data = {
        "text": msg,
        "chat_id": chat_id,
        "disable_notification": disable_notification,
    }
    response = await session.post(f"/bot{API_TOKEN}/sendMessage", data=data)
    response.raise_for_status()
    LOG.info(f"send message: {str(data)}")
    return await response.json()


async def wait_until(dt):
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_at(dt, coro):
    await wait_until(dt)
    return await coro


async def loop():
    LOG.info("Starting loop...")
    first_run = True
    async with aiohttp.ClientSession(base_url=API_URL) as session:
        while isinstance("", str):
            try:
                run_each_day = datetime.datetime.now() + datetime.timedelta(hours=8)
                run_at_date = datetime.datetime.now() if first_run else run_each_day
                response = await run_at(
                    run_at_date,
                    send_message(
                        session,
                        "Nixos ещё не умер",
                        CHANNEL_ID,
                    ),
                )
                first_run = False
                LOG.debug(response)
            except Exception as e:
                LOG.error(e)
                await send_message(session, str(e), DEBUG_USER_ID)


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    e_handler = logging.StreamHandler(sys.stdout)
    e_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    )
    root.addHandler(e_handler)
    asyncio.run(loop())
