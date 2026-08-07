import os
import sys

# Проверяем разные варианты структуры импортов
try:
    from TwitchChannelPointsMiner import TwitchChannelPointsMiner
    from TwitchChannelPointsMiner.classes.Settings import Streamer
except ImportError:
    try:
        from TwitchChannelPointsMiner import TwitchChannelPointsMiner, Streamer
    except ImportError:
        from TwitchChannelPointsMiner.TwitchChannelPointsMiner import TwitchChannelPointsMiner
        from TwitchChannelPointsMiner.Streamer import Streamer

# Получаем OAuth-токен
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализация майнера
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Передаем токен авторизации
if hasattr(miner, "twitch") and miner.twitch is not None:
    miner.twitch.auth_token = auth_token

# Список стримеров
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

# Запуск
miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
