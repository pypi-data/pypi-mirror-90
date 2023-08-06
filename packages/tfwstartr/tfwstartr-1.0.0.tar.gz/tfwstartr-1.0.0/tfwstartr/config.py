import os

__DEFAULT_WORKDIR = "/tmp/startr"

STARTER_WORKDIR = os.environ.get("TFW_STARTER_WORKING_DIRECTORY", __DEFAULT_WORKDIR)
DATA_FOLDER = f"{__package__}.data"
