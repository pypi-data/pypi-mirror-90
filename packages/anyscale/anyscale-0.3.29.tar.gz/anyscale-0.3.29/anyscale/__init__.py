import os
from sys import path

anyscale_dir = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.join(anyscale_dir, "client"))
path.append(os.path.join(anyscale_dir, "sdk"))
anyscale_ray_dir = os.path.join(anyscale_dir, "anyscale_ray")
path.insert(0, anyscale_ray_dir)

__version__ = "0.3.29"

ANYSCALE_ENV = os.environ.copy()
ANYSCALE_ENV["PYTHONPATH"] = anyscale_ray_dir + ":" + ANYSCALE_ENV.get("PYTHONPATH", "")
