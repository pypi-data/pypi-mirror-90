import os
import dotenv

# ENV-BASED CREDENTIALS
# load .env file
ENV_FILE = os.getenv("DATA_ENV_FILE", os.path.expanduser("~/.dada/.env"))
if not ENV_FILE or not os.path.exists(ENV_FILE):
    dotenv.load_dotenv()
else:
    dotenv.load_dotenv(ENV_FILE)

ENV = os.getenv("DADA_ENV", "dev")

if not ENV:
    raise RuntimeError("No DADA_ENV supplied.")

# load constants
from dada_settings.core import *
from dada_settings.cons import *

# override with environments
if ENV == "prod":
    from dada_settings.prod import *

if ENV == "dev":
    from dada_settings.dev import *

if ENV == "test":
    from dada_settings.test import *

if ENV == "docker":
    from dada_settings.docker import *
