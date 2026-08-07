import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner, Streamer

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер
miner = TwitchChannelPointsMiner(
    claim_drops_startup=True
)

# Авторизуемся через токен в объекте twitch
miner.twitch.auth_token = auth_token

# Запуск фарма для двух стримеров
miner.mine(
    [
        Streamer("foxsi_pubg"),
        Streamer("tsunavohka")
    ],
    followers=False,
    git_upgrade=False
)
