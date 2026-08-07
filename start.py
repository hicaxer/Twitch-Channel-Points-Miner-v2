import os
import sys
import importlib

# Функция для автоматического поиска и импорта класса
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

TwitchChannelPointsMiner = get_class("TwitchChannelPointsMiner")
Streamer = get_class("Streamer")

if not TwitchChannelPointsMiner or not Streamer:
    print("❌ Не удалось найти необходимые классы!")
    sys.exit(1)

# Читаем оба токена из окружения
token1 = os.environ.get("TWITCH_TOKEN_1", "")
token2 = os.environ.get("TWITCH_TOKEN_2", "")

# Берем первый доступный токен (или token1 по умолчанию)
auth_token = token1 or token2

if not auth_token:
    print("❌ Ошибка: Ни один OAuth-токен (TWITCH_TOKEN_1 или TWITCH_TOKEN_2) не передан!")
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
