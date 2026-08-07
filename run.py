import os
import sys

# Импорт основного класса майнера
from TwitchChannelPointsMiner import TwitchChannelPointsMiner

# Импорт сущностей из папки classes
from TwitchChannelPointsMiner.classes.Entities import Streamer

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер (указываем username для создания сессии)
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Передаем OAuth токен в объект авторизации
miner.twitch.auth_token = auth_token

# Список стримеров
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

# Запуск фарма
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
