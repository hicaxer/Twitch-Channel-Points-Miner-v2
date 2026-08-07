import os
import sys

# Добавляем путь к проекту в систему импортов Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Попытка импорта сущностей из разных вариантов структуры репозитория
try:
    from TwitchChannelPointsMiner import TwitchChannelPointsMiner
    from TwitchChannelPointsMiner.classes.Entities import Streamer
except ImportError:
    try:
        from TwitchChannelPointsMiner.TwitchChannelPointsMiner import TwitchChannelPointsMiner
        from TwitchChannelPointsMiner.Streamer import Streamer
    except ImportError:
        from TwitchChannelPointsMiner import TwitchChannelPointsMiner, Streamer

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализируем майнер
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Авторизация по OAuth-токену
if hasattr(miner, "twitch") and miner.twitch is not None:
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
