import os
import sys
import importlib.util

# Функция для точечного импорта файла по относительному пути
def load_module(module_name, relative_path):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Импортируем напрямую из файлов проекта
try:
    # Загружаем базовые сущности
    entities_mod = load_module("Entities", "TwitchChannelPointsMiner/classes/Entities.py")
    Streamer = entities_mod.Streamer
    
    # Загружаем главный класс
    miner_mod = load_module("TwitchChannelPointsMiner", "TwitchChannelPointsMiner/TwitchChannelPointsMiner.py")
    TwitchChannelPointsMiner = miner_mod.TwitchChannelPointsMiner
except Exception as e:
    print(f"❌ Ошибка загрузки модулей: {e}")
    sys.exit(1)

# Берем токен из секретов GitHub Actions
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# Инициализация майнера
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Установка токена авторизации
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
