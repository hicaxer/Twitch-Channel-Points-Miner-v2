import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.classes.Twitch import Twitch
from TwitchChannelPointsMiner.classes.Entities import Streamer

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Авторизуемся через OAuth-токен напрямую в объекте Twitch
twitch = Twitch(oauth_token=auth_token)

# Инициализируем майнер с авторизованным объектом Twitch
miner = TwitchChannelPointsMiner(
    twitch=twitch,
    claim_drops_startup=True
)

# Список стримеров для фарма
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka"),
]

# Запуск фарма
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
