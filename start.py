import os
import sys
import importlib

# Динамический поиск классов
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

# Читаем токены из секретов GitHub
token1 = os.environ.get("TWITCH_TOKEN_1", "")
token2 = os.environ.get("TWITCH_TOKEN_2", "")

# Берем первый доступный токен
auth_token = token1 or token2

if not auth_token:
    print("❌ Ошибка: Ни один OAuth-токен (TWITCH_TOKEN_1 или TWITCH_TOKEN_2) не передан!")
    sys.exit(1)

# Если токен передан без приставки "oauth:", добавляем её при необходимости
if not auth_token.startswith("oauth:") and len(auth_token) == 30:
    auth_token = f"oauth:{auth_token}"

# Инициализация майнера (передаем oauth_token напрямую в параметры, если поддерживается, 
# либо инициализируем чистый клиент)
try:
    miner = TwitchChannelPointsMiner(
        username="Bot",
        claim_drops_startup=True,
        oauth_token=auth_token
    )
except TypeError:
    # Запасной вариант инициализации, если аргумент oauth_token не принимается в __init__
    miner = TwitchChannelPointsMiner(
        username="Bot",
        claim_drops_startup=True
    )
    if hasattr(miner, "oauth_token"):
        miner.oauth_token = auth_token

# Список стримеров для фарма
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
