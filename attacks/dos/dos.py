import argparse
import asyncio
import signal
import sys
import time

import aiohttp

def parse_args():
    p = argparse.ArgumentParser(description="Steady‑state crash tester")
    p.add_argument('--url',
                   default="https://elec0138-forum.0138019.xyz/",
                   help="Heavier endpoint to hit")
    p.add_argument('--users',    type=int,   default=3500,
                   help="Concurrent “sessions”")
    p.add_argument('--rps',      type=int,   default=3500,
                   help="Total requests per second to sustain")
    p.add_argument('--duration', type=int,   default=600,
                   help="Test duration (s)")
    return p.parse_args()

class TokenBucket:
    def __init__(self, rate):
        self._rate = rate
        self._tokens = rate
        self._last = time.monotonic()
    async def take(self):
        while True:
            now = time.monotonic()
            # refill
            self._tokens += (now - self._last) * self._rate
            self._last = now
            if self._tokens >= 1:
                self._tokens -= 1
                return
            await asyncio.sleep(0.001)

async def user_worker(session, id, url, bucket, counter):
    payload = {"username":"popeta","password":"mercedes","recaptchaToken":""}
    while True:
        await bucket.take()           # pace the total RPS
        try:
            async with session.post(url, json=payload) as resp:
                await resp.text()
                counter['reqs'] += 1
                counter['codes'][resp.status] = counter['codes'].get(resp.status,0)+1
        except Exception:
            counter['errors'] += 1

async def metrics_reporter(counter, interval, stop_event):
    prev = 0
    while not stop_event.is_set():
        await asyncio.sleep(interval)
        total = counter['reqs']
        delta = total - prev
        prev = total
        print(f"→ {delta/interval:.1f} req/s | 2xx={counter['codes'].get(200,0)} "
              f"4xx={counter['codes'].get(400,0)+counter['codes'].get(422,0)} "
              f"errors={counter['errors']}")

async def run_test(args):
    bucket = TokenBucket(args.rps)
    counter = {'reqs':0,'codes':{},'errors':0}
    stop = asyncio.Event()

    timeout = aiohttp.ClientTimeout(total=5)
    connector = aiohttp.TCPConnector(limit=args.users, ssl=False)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as sess:
        workers = [asyncio.create_task(user_worker(sess, i, args.url, bucket, counter))
                   for i in range(args.users)]
        metrics = asyncio.create_task(metrics_reporter(counter, 5, stop))

        try:
            await asyncio.sleep(args.duration)
        except asyncio.CancelledError:
            pass
        finally:
            stop.set()
            for w in workers: w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
            metrics.cancel()
            await asyncio.gather(metrics, return_exceptions=True)

def main():
    args = parse_args()
    try:
        asyncio.run(run_test(args))
    except KeyboardInterrupt:
        print("\n🛑 Interrupted — shutting down.")

if __name__ == "__main__":
    main()
