import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.Settings import Priority
from TwitchChannelPointsMiner.Streamer import Streamer

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер
miner = TwitchChannelPointsMiner(
    username="", 
    password="",
    claim_drops_startup=True,
    priority=[
        Priority.STREAK,
        Priority.DROPS,
        Priority.SUBSCRIBED
    ]
)

# Авторизация по OAuth-токену
miner.analytics.auth_token = auth_token

# Список стримеров для фарма
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka"),
]

# Запуск фарма (followers=False отключает фарм остальных подписок)
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
