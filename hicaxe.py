import os
import sys

# Добавляем путь к папке с исходниками, чтобы Python видел все внутренние файлы
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Прямой импорт основного класса
try:
    from TwitchChannelPointsMiner import TwitchChannelPointsMiner
    from TwitchChannelPointsMiner.classes.Entities import Streamer
except ModuleNotFoundError:
    # Вариант для структуры, где файлы лежат в корне или подпапке
    from TwitchChannelPointsMiner.TwitchChannelPointsMiner import TwitchChannelPointsMiner
    from TwitchChannelPointsMiner.Streamer import Streamer

# Инициализируем майнер
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Подставляем OAuth-токен в объект авторизации Twitch
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
