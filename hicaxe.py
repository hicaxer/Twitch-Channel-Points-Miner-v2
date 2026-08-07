import os
import sys

# Добавляем текущую директорию в пути поиска модулей Python
sys.path.insert(0, os.path.abspath("."))

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Импортируем классы напрямую из репозитория
try:
    from TwitchChannelPointsMiner import TwitchChannelPointsMiner
    from TwitchChannelPointsMiner.classes.Entities import Streamer
except ImportError:
    try:
        from TwitchChannelPointsMiner.TwitchChannelPointsMiner import TwitchChannelPointsMiner
        from TwitchChannelPointsMiner.Streamer import Streamer
    except ImportError:
        # Запасной вариант импорта для редких форков
        from src.TwitchChannelPointsMiner import TwitchChannelPointsMiner
        from src.Streamer import Streamer

# Инициализация майнера
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Авторизация по токену
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
