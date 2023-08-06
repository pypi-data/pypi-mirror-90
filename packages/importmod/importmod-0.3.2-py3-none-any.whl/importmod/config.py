import configparser
import os

from portmod.globals import env

NEXUS_KEY = None

if os.path.exists(env.CONFIG_DIR):
    config = configparser.ConfigParser()
    config.read(os.path.join(env.CONFIG_DIR, "importmod.cfg"))
    if config["importmod"]:
        NEXUS_KEY = config["importmod"].get("NEXUS_KEY")
