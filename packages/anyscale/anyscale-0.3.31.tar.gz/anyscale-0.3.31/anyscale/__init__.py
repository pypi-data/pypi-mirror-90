import os
from sys import path

anyscale_dir = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.join(anyscale_dir, "client"))
path.append(os.path.join(anyscale_dir, "sdk"))
ANYSCALE_RAY_DIR = os.path.join(anyscale_dir, "anyscale_ray")

__version__ = "0.3.31"

ANYSCALE_ENV = os.environ.copy()
ANYSCALE_ENV["PYTHONPATH"] = ANYSCALE_RAY_DIR + ":" + ANYSCALE_ENV.get("PYTHONPATH", "")
