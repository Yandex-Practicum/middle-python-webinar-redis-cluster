import yarl
from environs import Env

env = Env()
env.read_env()

URL_TTL_S = env.int("URL_TTL_S")
MIN_URL_LENGTH = env.int("MIN_URL_LENGTH")
MAIN_SERVICE_URL = env.str("SERVICE_URL")
SERVICE_PORT = env.int("SERVICE_PORT")

REDIS_DSNS = [str(yarl.URL(r_dsn)) for r_dsn in env.list("REDIS_DSNS")]

__all__ = ["URL_TTL_S", "MIN_URL_LENGTH", "MAIN_SERVICE_URL", "REDIS_DSNS"]
