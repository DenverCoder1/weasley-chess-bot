from dotenv.main import load_dotenv
import os

load_dotenv()

# Discord config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_PREFIX = "w!"

# Guild
GUILD_ID = int(os.getenv("GUILD_ID"))

# Clock channel
CLOCK_CHANNEL_ID = int(os.getenv("CLOCK_CHANNEL_ID"))

# Scoreboard channel
SCOREBOARD_CHANNEL_ID = int(os.getenv("SCOREBOARD_CHANNEL_ID"))

# Logging channel
LOGGING_CHANNEL_ID = int(os.getenv("LOGGING_CHANNEL_ID"))

# JSON Match API endpoint
JSON_API_ENDPOINT = os.getenv("JSON_API_ENDPOINT")
