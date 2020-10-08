import yarl
from environs import Env

env = Env()
env.read_env()

URL_TTL_S = env.int("URL_TTL_S")
MIN_URL_LENGTH = env.int("MIN_URL_LENGTH")
MAIN_SERVICE_URL = env.str("SERVICE_URL")
SERVICE_PORT = env.int("SERVICE_PORT")

REDIS_DSN = yarl.URL("redis://" + env.str("REDIS_HOST")).with_port(
    env.int("REDIS_PORT")
)

__all__ = ["URL_TTL_S", "MIN_URL_LENGTH", "MAIN_SERVICE_URL", "REDIS_DSN"]
