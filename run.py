import os
import sys
import importlib

# 1. Автоматический поиск и импорт TwitchChannelPointsMiner и Streamer
def get_class(class_name):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file).replace("./", "").replace("/", ".").replace(".py", "")
                try:
                    mod = importlib.import_module(path)
                    if hasattr(mod, class_name):
                        return getattr(mod, class_name)
                except Exception:
                    pass
    return None

TwitchChannelPointsMiner = get_class("TwitchChannelPointsMiner")
Streamer = get_class("Streamer")

if not TwitchChannelPointsMiner or not Streamer:
    print("❌ Не удалось автоматически найти классы майнера!")
    sys.exit(1)

# 2. Получение токена из секретов GitHub
auth_token = os.environ.get("TWITCH_TOKEN", "")

if not auth_token:
    print("❌ Ошибка: OAuth-токен не передан!")
    sys.exit(1)

# 3. Инициализация майнера
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Передаем токен авторизации
if hasattr(miner, "twitch") and miner.twitch is not None:
    miner.twitch.auth_token = auth_token

# 4. Формирование списка стримеров и запуск
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

miner.mine(
    streamers,
    followers=False,
    git_upgrade=False
)
