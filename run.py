import os
import sys

# Прямой импорт классов из файлов библиотеки
from TwitchChannelPointsMiner.Twitch import Twitch
from TwitchChannelPointsMiner.Streamer import Streamer
from TwitchChannelPointsMiner.TwitchChannelPointsMiner import TwitchChannelPointsMiner

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Авторизуемся через объект Twitch
twitch_instance = Twitch(auth_token=auth_token)

# Инициализируем главный класс майнера
miner = TwitchChannelPointsMiner(
    twitch=twitch_instance,
    claim_drops_startup=True
)

# Запуск фарма для двух стримеров
miner.mine(
    [
        Streamer("foxsi_pubg"),
        Streamer("tsunavohka")
    ],
    followers=False,
    git_upgrade=False
)
