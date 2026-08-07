import os
import sys
import pickle
import builtins
import importlib

# 1. Заглушка консольного ввода для GitHub Actions
def non_interactive_input(prompt=""):
    print(f"\n⚠️ Скрипт попытался запросить ввод: '{prompt}'")
    print("❌ Не удалось применить auth-token. Обновите значение TWITCH_TOKEN_1 в GitHub Secrets.")
    sys.exit(1)

builtins.input = non_interactive_input

# 2. Динамический импорт классов
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

# 3. Чтение и подготовка токена
token1 = os.environ.get("TWITCH_TOKEN_1", "").strip()
token2 = os.environ.get("TWITCH_TOKEN_2", "").strip()

auth_token = token1 or token2

if auth_token.startswith("oauth:"):
    auth_token = auth_token.replace("oauth:", "")

if not auth_token:
    print("❌ Ошибка: Токен TWITCH_TOKEN_1 / TWITCH_TOKEN_2 не передан!")
    sys.exit(1)

# 4. Создаем структуру cookies напрямую для обхода интерактивного входа
username = "Bot"
cookies_data = {
    "auth-token": auth_token
}

# Сохраняем куки во возможные локации, где майнер ищет профиль
os.makedirs("analytics", exist_ok=True)
os.makedirs(f"analytics/{username}", exist_ok=True)

cookie_paths = [
    "cookies.pkl",
    f"analytics/{username}/cookies.pkl",
    f"analytics/cookies.pkl"
]

for path in cookie_paths:
    try:
        with open(path, "wb") as f:
            pickle.dump(cookies_data, f)
    except Exception:
        pass

# 5. Инициализация майнера
miner = TwitchChannelPointsMiner(
    username=username,
    claim_drops_startup=True
)

# 6. Внедрение токена в сессию
if hasattr(miner, "twitch"):
    if hasattr(miner.twitch, "session"):
        miner.twitch.session.cookies.set("auth-token", auth_token, domain=".twitch.tv")

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
