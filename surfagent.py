# Copyright (C) 2024 Tristan de Cacqueray
# SPDX-License-Identifier: Apache-2.0

# This process follow firefox to record youtube page titles in markdown to create playlists

import time, traceback
from urllib.parse import urlparse, parse_qs

from marionette_driver.marionette import Marionette

def save_infos(infos):
    with open("playlist.md", "a") as of:
        of.write(f"| DATE | AUTHOR | {infos['title']} <!-- YT:{infos['vid']} --> |\n")
        print(f"Updated playlist.md with {infos}")

def process_yt(client, url):
    title = client.title
    vid = parse_qs(urlparse(url).query)["v"][0]
    return dict(title=title, vid=vid)

def process(client, url):
    print(f"[+] Processing {url}")
    if url.startswith("https://www.youtube.com/watch"):
        return process_yt(client, url)

# Wait 10 seconds before recording a page
FOCUS_TIME = 10.0

def main_loop(client):
    focused = str(client.title)
    urls = set()
    last = ("", 0)
    while True:
        time.sleep(1.0)

        # The client doesn't follow tab changed, but we can observe the title in the context chrome:
        with client.using_context(client.CONTEXT_CHROME):
            if str(client.title) != focused:
                print(f"[+] Tab changed, reconnecting to get the url... {client.title}")
                focused = str(client.title)
                client.cleanup()
                client.start_session()

        # Then we check if the current URL changed
        url = client.get_url()
        if url in urls:
            continue

        # This is a new URL
        now = time.time()
        if last[0] == url:
            if now - last[1] >= FOCUS_TIME:
                # And it is playing for more than FOCUS_TIME
                try:
                    if infos := process(client, url):
                        save_infos(infos)
                    urls.add(url)
                except Exception as e:
                    print(traceback.format_exc())
                    print("[+] Oops", e)
        else:
            # It's a fresh new url, let's wait a bit
            last = (url, now)

def mk_client():
    client = Marionette('127.0.0.1', port=2828)
    client.start_session()
    print("[+] Connected!")
    return client

if __name__ == "__main__":
    main_loop(mk_client())
