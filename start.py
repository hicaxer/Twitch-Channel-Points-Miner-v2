import os
import sys
import importlib

# Функция для автоматического поиска и импорта класса из любой подпапки
def get_class(class_name):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and not file.startswith("setup"):
                rel_path = os.path.relpath(os.path.join(root, file))
                module_path = rel_path.replace(os.sep, ".").rsplit(".py", 1)[0]
                try:
                    mod = importlib.import_module(module_path)
                    if hasattr(mod, class_name):
                        return getattr(mod, class_name)
                except Exception:
                    pass
    return None

# Динамически находим нужные классы
TwitchChannelPointsMiner = get_class("TwitchChannelPointsMiner")
Streamer = get_class("Streamer")

if not TwitchChannelPointsMiner:
    print("❌ Не удалось найти класс TwitchChannelPointsMiner")
    sys.exit(1)

if not Streamer:
    print("❌ Не удалось найти класс Streamer")
    sys.exit(1)

# Получение OAuth-токена
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
