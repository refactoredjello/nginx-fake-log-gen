import os
from faker import Faker

from .config import OUT_PATH, OUT_FILE_NAME, LOG_LINES, LOG_FORMAT
from .log_data_builder import LogDataBuilder



HTTP_VERSION = "HTTP/1.1"


def gen_remote_addr(log_mocks: LogDataBuilder):
    return log_mocks.remote_addr


def gen_remote_user(log_mocks: LogDataBuilder):
    return log_mocks.user_name


def gen_local_time(log_mocks: LogDataBuilder):
    return f"{log_mocks.random_date()}:{log_mocks.random_time()} +0000"


def gen_request(log_mocks: LogDataBuilder):
    return f"{log_mocks.random_http_method()} /{log_mocks.uri_path} {HTTP_VERSION}"


def gen_http_status(log_mocks: LogDataBuilder):
    return log_mocks.random_status_code()


def gen_bytes_sent(log_mocks: LogDataBuilder):
    return log_mocks.random_bytes_sent()


def gen_referer(log_mocks: LogDataBuilder):
    return log_mocks.referer


def gen_user_agent(log_mocks: LogDataBuilder):
    return log_mocks.user_agent


def compose_line(mocks: LogDataBuilder):
    """Compose a single log line from mock data."""
    return LOG_FORMAT.format(
        remote_addr=gen_remote_addr(mocks),
        remote_user=gen_remote_user(mocks),
        local_time=gen_local_time(mocks),
        request=gen_request(mocks),
        status=gen_http_status(mocks),
        bytes_sent=gen_bytes_sent(mocks),
        referer=gen_referer(mocks),
        user_agent=gen_user_agent(mocks)
    )


def generate_logs(num_lines: int = LOG_LINES) -> str:
    log_mocks = LogDataBuilder()
    log_lines = []

    for _ in range(num_lines):
        log_lines.append(compose_line(log_mocks))

    return "\n".join(log_lines) + "\n"


def write_logs(data: str, output_path: str = OUT_PATH, output_file: str = OUT_FILE_NAME):
    os.makedirs(output_path, exist_ok=True)
    full_path = f'{output_path}/{output_file}'

    with open(full_path, 'w') as f:
        f.write(data)

    return full_path
