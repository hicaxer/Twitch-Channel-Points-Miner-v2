import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер
miner = TwitchChannelPointsMiner(
    username="", 
    password="",
    claim_drops_startup=True
)

# Авторизация по OAuth-токену
miner.analytics.auth_token = auth_token

# Список стримеров указываем простыми строками
streamers = [
    "foxsi_pubg",
    "tsunavohka",
]

# Запуск фарма
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
