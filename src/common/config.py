import yaml

with open("config.yaml", "r") as f:
    GLOBAL_CONFIG = yaml.safe_load(f)

print("GLOBAL_CONFIG:", GLOBAL_CONFIG)

RECV_AVATAR_ENABLED = GLOBAL_CONFIG["recv"]["avatar"]
RECV_IMAGE_ENABLED = GLOBAL_CONFIG["recv"]["image"]

FOCUS_GROUP = (
    GLOBAL_CONFIG["focus"]["group"]["mode"] != "blacklist",
    GLOBAL_CONFIG["focus"]["group"]["list"],
)
FOCUS_USER = (
    GLOBAL_CONFIG["focus"]["user"]["mode"] != "blacklist",
    GLOBAL_CONFIG["focus"]["user"]["list"],
)

DEBUG_MODE = GLOBAL_CONFIG["debug"]
