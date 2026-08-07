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
    claim_drops_startup=True, # Авто-сбор Drops при старте
    priority=[
        Priority.STREAK,      # Приоритет стрикам просмотра
        Priority.DROPS,       # Приоритет дропсам
        Priority.SUBSCRIBED   # Приоритет каналам с сабкой
    ]
)

# Подставляем авторизацию по OAuth токену
miner.analytics.auth_token = auth_token

# Указываем отслеживаемые каналы
streamers = [
    Streamer("foxsi_pubg"),
]

# Запуск фарма
miner.mine(
    streamers,
    followers=True, # Автоматически подтягивать все каналы из твоих отслеживаемых на Twitch
    git_upgrade=False
)
