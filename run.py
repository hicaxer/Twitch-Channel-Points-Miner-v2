import os
import sys
from TwitchChannelPointsMiner import TwitchChannelPointsMiner

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер напрямую
miner = TwitchChannelPointsMiner(
    oauth_token=auth_token,
    claim_drops_startup=True
)

# Запуск фарма по списку логинов
miner.mine(
    [
        "foxsi_pubg",
        "tsunavohka"
    ],
    followers=False,
    git_upgrade=False
)
