from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core

from time import sleep
import signal
import threading

from typing import Tuple

import asyncio

import multiprocessing

from addon import CaptureAddon


def main():
    # create and start mitmdump in its own thread
    m, addon = create_proxy()
    proxy_thread = threading.Thread(
        target=loop_in_thread, args=(asyncio.get_event_loop(), m)
    )
    proxy_thread.start()

    # wait for proxy to start before running input loop
    sleep(2)
    run_input_loop(m, addon)


def run_input_loop(m: DumpMaster, addon: CaptureAddon):
    while True:
        print(
            "Select an option:\n"
            "1. Start new site session\n"
            "2. Finish capture and quit"
        )
        option = None
        while option not in [1, 2]:
            try:
                option = int(input("> "))
            except:
                pass
        if option == 1:
            label = input("Enter label for session:\n> ")
            addon.label = label
        elif option == 2:
            # TODO save results for JSON, parse into something readable
            m.shutdown()
            break


def create_proxy() -> Tuple[DumpMaster, CaptureAddon]:
    # set default proxy options
    opts = options.Options(listen_host="0.0.0.0", listen_port=8080)
    config = proxy.config.ProxyConfig(opts)
    # create addon
    addon = CaptureAddon()
    # create proxy
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(config)
    m.addons.add(addon)
    return m, addon


def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)
    m.run_loop(loop.run_forever)


if __name__ == "__main__":
    main()
