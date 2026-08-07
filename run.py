import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.classes.Settings import Priority
from TwitchChannelPointsMiner.classes.Entities import Streamer

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

# Указываем ТОЛЬКО тех стримеров, которых нужно фармить (1 или 2 канала):
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka"), # Замени на второго стримера или удали эту строчку, если нужен только од
]

# Запуск фарма (followers=False отключает фарм остальных подписок)
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
