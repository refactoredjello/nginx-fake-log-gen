from collections.abc import Callable
import time

from faker import Faker

from .config import MOCK_COUNT

fake = Faker()

def gen_mock(func: Callable, postfix: Callable=None):
    res = []
    for _ in range(MOCK_COUNT):
        val = func()
        if postfix:
            val += postfix()
        res.append(val)
    return res



class LogDataBuilder:
    """Contains and generate reusable log parts to simulate real logs"""

    def __init__(self):
        Faker.seed(time.time())
        
        self.remote_addr = gen_mock(fake.ipv4)
        self.user_name = gen_mock(fake.user_name)
        self.uri_path = gen_mock(fake.uri_path, lambda: fake.random_element([fake.uri_extension(), '']))
        self.referer = gen_mock(fake.url)
        self.user_agent = gen_mock(fake.user_agent)

    def __getattribute__(self, name):
        try:
            original_value = super().__getattribute__(name)
            if isinstance(original_value, list):
                return fake.random_element(original_value)

            return original_value

        except AttributeError:
            raise