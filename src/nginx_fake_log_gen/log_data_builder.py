from collections.abc import Callable
import time

from faker import Faker

from .config import MOCK_COUNT, MAX_BYTES


def gen_mock(func: Callable, postfix: Callable = None):
    res = []
    for _ in range(MOCK_COUNT):
        val = func()
        if postfix:
            val += postfix()
        res.append(val)
    return res


class LogDataBuilder:
    """Contains and generate reusable log parts to simulate real logs"""

    def __init__(self, max_bytes=MAX_BYTES):
        Faker.seed(time.time())
        self._fake = Faker()
        self.max_bytes = max_bytes

        self._remote_addr = gen_mock(self._fake.ipv4)
        self._user_name = gen_mock(self._fake.user_name)
        self._uri_path = gen_mock(self._fake.uri_path, lambda: self._fake.random_element([self._fake.uri_extension(), '']))
        self._referer = gen_mock(self._fake.url)
        self._user_agent = gen_mock(self._fake.user_agent)

    def random_status_code(self):
        return self._fake.http_status_code()

    def random_date(self):
        return self._fake.date(pattern="%d/%b/%Y")

    def random_time(self):
        return self._fake.time()

    def random_bytes_sent(self):
        return self._fake.random_int(min=1, max=self.max_bytes)

    def random_http_method(self):
        return self._fake.http_method()

    @property
    def remote_addr(self):
        return self.get_random_element(self._remote_addr)

    @property
    def user_name(self):
        return self.get_random_element(self._user_name)

    @property
    def uri_path(self):
        return self.get_random_element(self._uri_path)

    @property
    def referer(self):
        return self.get_random_element(self._referer)

    @property
    def user_agent(self):
        return self.get_random_element(self._user_agent)

    def get_random_element(self, prop: iter):
        return self._fake.random_element(prop)
