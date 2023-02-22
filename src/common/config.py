import yaml

with open("config.yaml", "r") as f:
    GLOBAL_CONFIG = yaml.safe_load(f)

print("GLOBAL_CONFIG:", GLOBAL_CONFIG)

RECV_AVATAR_ENABLED = GLOBAL_CONFIG["recv"]["avatar"]
RECV_IMAGE_ENABLED = GLOBAL_CONFIG["recv"]["image"]

FOCUS_GROUP = (
    True if GLOBAL_CONFIG["focus"]["group"]["mode"] == "blacklist" else False,
    GLOBAL_CONFIG["focus"]["group"]["list"],
)
FOCUS_USER = (
    True if GLOBAL_CONFIG["focus"]["user"]["mode"] == "blacklist" else False,
    GLOBAL_CONFIG["focus"]["user"]["list"],
)

DEBUG_MODE = GLOBAL_CONFIG["debug"]
