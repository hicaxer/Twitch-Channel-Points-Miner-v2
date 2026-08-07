import os
import sys
import builtins
import importlib

# Перехватываем вызов input, чтобы скрипт не вис в ожидании ввода
def non_interactive_input(prompt=""):
    print(f"\n⚠️ Скрипт попытался запросить консольный ввод: '{prompt}'")
    print("❌ Токен/куки авторизации Twitch недействительны или просрочены. Обновите TWITCH_TOKEN_1 / TWITCH_TOKEN_2 в Secrets.")
    sys.exit(1)

builtins.input = non_interactive_input

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

# Читаем токены из секретов
token1 = os.environ.get("TWITCH_TOKEN_1", "").strip()
token2 = os.environ.get("TWITCH_TOKEN_2", "").strip()

auth_token = token1 or token2

# Убираем префикс oauth:, если он случайно записан (в cookies нужен чистый 30-значный хэш)
if auth_token.startswith("oauth:"):
    auth_token = auth_token.replace("oauth:", "")

if not auth_token:
    print("❌ Ошибка: Ни один OAuth-токен не передан!")
    sys.exit(1)

# Инициализация майнера
miner = TwitchChannelPointsMiner(
    username="Bot",
    claim_drops_startup=True
)

# Принудительно внедряем auth-token в HTTP-сессию майнера
if hasattr(miner, "twitch"):
    if hasattr(miner.twitch, "session"):
        miner.twitch.session.cookies.set("auth-token", auth_token, domain=".twitch.tv")
    if hasattr(miner.twitch, "auth_token"):
        miner.twitch.auth_token = auth_token

# Список стримеров
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

# Запуск
miner.mine(
    streamers,
    followers=False
)
