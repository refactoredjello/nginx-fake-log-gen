# Generate fake nginx logs with random values for the standard nginx log output variables
# remote_addr, remote_user, [local_time], http_method /path http_version, http_status, body_bytes_sent, http_referer, http_user_agent
# 192.168.1.1 - user1 [27/07/2025:10:30:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "http://example.com/referer" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
from collections.abc import Callable
from symtable import Function

from faker import Faker
import time
import os

OUT_PATH = "output"
OUT_FILE_NAME = "fake.log"
HTTP_VERSION = "HTTP/1.1"
LOG_LINES = 10_000
MOCK_COUNT = 100

fake = Faker()

def gen_mock(func: Callable, postfix=None):
    res = []
    for _ in range(MOCK_COUNT):
        val = func()
        if postfix:
            val += postfix()
        res.append(val)
    return res

class LogMocks:
    def __init__(self):
        Faker.seed(time.time())

        self._original_getattribute = super().__getattribute__
        self.remote_addr = gen_mock(fake.ipv4)
        self.user_name = gen_mock(fake.user_name)
        self.uri_path = gen_mock(fake.uri_path, lambda : fake.uri_extension() if fake.random_digit_or_empty() else '')
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

def gen_remote_addr(log_mocks: LogMocks):
    return log_mocks.remote_addr

def gen_remote_user(log_mocks: LogMocks):
    return log_mocks.user_name

def gen_local_time():
    return f"{fake.date()}:{fake.time()} +0000"

def gen_request(log_mocks: LogMocks):
    return f"{fake.http_method()} /{log_mocks.uri_path} {HTTP_VERSION}"

def gen_http_status():
    return fake.http_status_code()

def gen_bytes_sent():
    return fake.random_int(min=1, max=2048)

def gen_referer(log_mocks: LogMocks):
    return log_mocks.referer

def gen_user_agent(log_mocks: LogMocks):
    return log_mocks.user_agent

def compose_line(mocks: LogMocks):
    return f'{gen_remote_addr(mocks)} - {gen_remote_user(mocks)} [{gen_local_time()}] "{gen_request(mocks)}" {gen_http_status()} {gen_bytes_sent()} "{gen_referer(mocks)}" "{gen_user_agent(mocks)}"'

def generate_data():
    log_mocks = LogMocks()
    log = ''
    for i in range(LOG_LINES):
        log += compose_line(log_mocks) + "\n"

    return log

def write_data(data: str):
    with open(f'{OUT_PATH}/{OUT_FILE_NAME}', 'w') as f:
        f.write(data)


if __name__ == '__main__':
    output = generate_data()
    print(f"writing data to {OUT_PATH}/{OUT_FILE_NAME} of size {len(output)}")
    os.makedirs(OUT_PATH, exist_ok=True)
    write_data(output)
