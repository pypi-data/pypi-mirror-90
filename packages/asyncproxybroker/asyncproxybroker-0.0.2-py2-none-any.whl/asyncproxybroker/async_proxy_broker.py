import asyncio
import random
import time
from asyncio import Queue, PriorityQueue, Lock
from collections import deque

import aiohttp
from proxybroker.utils import get_all_ip

from asyncproxybroker.providers import PROVIDERS

JUDGES = [
    'http://httpbin.org/get?show_env',
    'http://azenv.net/',
    'http://proxyjudge.us/azenv.php',
    'http://www.proxy-listen.de/azenv.php',
]

IP_HOSTS = [
    'https://wtfismyip.com/text',
    'http://api.ipify.org/',
    'http://ipinfo.io/ip',
    'http://ipv4.icanhazip.com/',
    'http://myexternalip.com/raw',
    'http://ipinfo.io/ip',
    'http://ifconfig.io/ip',
]


class AsyncProxyBroker:
    def __init__(self, check_url, allowed_anonymity_levels=None, qps_per_proxy=1,
                 max_consecutive_failures=5, providers=PROVIDERS, timeout=5):
        self._proxies = Queue()
        self._pending_providers = Queue()
        self._providers = providers

        self._verified_proxies = {}
        self._throttled_proxies = PriorityQueue()
        self._errors = {}

        self._check_url = check_url
        self._qps_per_proxy = qps_per_proxy
        self._max_consecutive_failures = max_consecutive_failures
        self._timeout = timeout

        self._ip = None
        self._ip_lock = Lock()

        if not allowed_anonymity_levels:
            self._allowed_anonymity_levels = ['Anonymous', 'Elite']
        else:
            self._allowed_anonymity_levels = allowed_anonymity_levels

    async def _get_real_ip(self):
        while not self._ip:
            async with self._ip_lock:
                if self._ip:
                    return self._ip

                try:
                    async with aiohttp.request(url=random.choice(IP_HOSTS), method='GET',
                                               timeout=aiohttp.ClientTimeout(total=self._timeout)) as response:
                        contents = await response.text()
                        ips = get_all_ip(contents)

                        if len(ips) == 1:
                            self._ip = ips.pop()
                            return self._ip
                except (UnicodeDecodeError,
                        asyncio.TimeoutError,
                        aiohttp.ClientOSError,
                        aiohttp.ClientResponseError,
                        aiohttp.ServerDisconnectedError):
                    pass

        return self._ip

    async def _get_anonymity_level(self, proxy_address):
        judge = random.choice(JUDGES)
        ip = await self._get_real_ip()

        try:
            async with aiohttp.request(url=judge, method='GET', proxy=proxy_address,
                                       timeout=aiohttp.ClientTimeout(total=self._timeout)) as response:
                contents = (await response.text()).lower()
                contained_ips = get_all_ip(contents)

                if ip in contained_ips:
                    return 'Transparent'
                elif 'via' in contents or 'proxy' in contents:
                    return 'Anonymous'
                else:
                    return 'Elite'
        except (UnicodeDecodeError,
                asyncio.TimeoutError,
                aiohttp.ClientOSError,
                aiohttp.ClientResponseError,
                aiohttp.ServerDisconnectedError):
            return 'None'

    def _populate_providers(self):
        for provider in self._providers:
            self._pending_providers.put_nowait(provider)

    async def _can_connect_to_test_url(self, proxy_address):
        try:
            async with aiohttp.request(url=self._check_url, method='GET', proxy=proxy_address,
                                       timeout=aiohttp.ClientTimeout(total=self._timeout)) as response:
                await response.text()
                return True
        except (UnicodeDecodeError,
                asyncio.TimeoutError,
                aiohttp.ClientOSError,
                aiohttp.ClientResponseError,
                aiohttp.ServerDisconnectedError):
            return False

    async def _populate_proxies(self):
        if self._pending_providers.empty():
            self._populate_providers()

        provider = self._pending_providers.get_nowait()
        proxies = await provider.get_proxies()

        for proxy in proxies:
            self._proxies.put_nowait(proxy)

        self._pending_providers.task_done()

    async def _try_verify_one_proxy(self):
        if self._proxies.empty():
            await self._populate_proxies()
            return

        (host, port, types) = self._proxies.get_nowait()
        proxy_address = 'http://%s:%s' % (host, port)

        if await self._get_anonymity_level(proxy_address) in self._allowed_anonymity_levels and \
                await self._can_connect_to_test_url(proxy_address):
            self._verified_proxies[proxy_address] = deque()
            self._errors[proxy_address] = 0

        self._proxies.task_done()

    @staticmethod
    def _flush_history(history):
        executions_removed = 0
        earliest_time = time.monotonic()

        while len(history) > 0:
            earliest_time = history.popleft()
            if time.monotonic() - earliest_time < 1:
                history.appendleft(earliest_time)
                break
            executions_removed += 1

        return executions_removed, earliest_time

    def _flush_throttled_proxies(self):
        while not self._throttled_proxies.empty():
            (_, proxy_url, history) = self._throttled_proxies.get_nowait()
            executions_removed, earliest_time = self._flush_history(history)

            if executions_removed == 0:
                self._throttled_proxies.put_nowait((earliest_time, proxy_url, history))
                self._throttled_proxies.task_done()
                return

            self._verified_proxies[proxy_url] = history
            self._throttled_proxies.task_done()

    def mark_successful(self, proxy_url):
        if proxy_url not in self._errors:
            return

        self._errors[proxy_url] = max(0, self._errors[proxy_url] - 1)

    def mark_failure(self, proxy_url):
        if proxy_url not in self._errors:
            return

        self._errors[proxy_url] += 1

    async def random_proxy(self):
        while True:
            self._flush_throttled_proxies()

            if not self._verified_proxies:
                await self._try_verify_one_proxy()

            while self._verified_proxies:
                proxy_url = random.choice(list(self._verified_proxies.keys()))

                if self._errors[proxy_url] >= self._max_consecutive_failures:
                    del self._errors[proxy_url]
                    del self._verified_proxies[proxy_url]
                    continue

                history = self._verified_proxies[proxy_url]

                _, earliest_time = self._flush_history(history)
                if len(history) < self._qps_per_proxy:
                    history.append(time.monotonic())
                    return proxy_url

                del self._verified_proxies[proxy_url]
                self._throttled_proxies.put_nowait((earliest_time, proxy_url, history))
