from dotenv.main import load_dotenv
import os

load_dotenv()

# Discord config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_PREFIX = "w!"

# Creates an integer ID list from a comma-separated string of IDs
GUILD_IDS = [
    int(gid)
    for gid in os.getenv("GUILD_IDS", "").split(",")
    if gid.isdigit()
] or None

# Clock channel
CLOCK_CHANNEL_ID = int(os.getenv("CLOCK_CHANNEL_ID"))

# Scoreboard channel
SCOREBOARD_CHANNEL_ID = int(os.getenv("SCOREBOARD_CHANNEL_ID"))

# Logging channel
LOGGING_CHANNEL_ID = int(os.getenv("LOGGING_CHANNEL_ID"))
