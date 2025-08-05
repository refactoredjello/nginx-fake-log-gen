# Default output settings
OUT_PATH = "output"
OUT_FILE_NAME = "fake.log"

# Generation settings
LOG_LINES = 10_000
MOCK_COUNT = 100
MAX_BYTES = 1048576 # MB

# Log format template
LOG_FORMAT = '{remote_addr} - {remote_user} [{local_time}] "{request}" {status} {bytes_sent} "{referer}" "{user_agent}"'

