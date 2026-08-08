import os
import sys
import pickle
import builtins
import getpass
import importlib
from requests.cookies import RequestsCookieJar

# 1. Глушим любые попытки консольного ввода (input и getpass)
def non_interactive_block(prompt=""):
    print(f"\n⚠️ Скрипт попытался запросить ввод пароля/данных: '{prompt}'")
    print("❌ Авторизация отклонена Twitch (токен недействителен, заблокирован IP или требуется 2FA).")
    sys.exit(1)

builtins.input = non_interactive_block
getpass.getpass = non_interactive_block

# 2. Динамический поиск классов
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

# 3. Получение токенов
token1 = os.environ.get("TWITCH_TOKEN_1", "").strip()
token2 = os.environ.get("TWITCH_TOKEN_2", "").strip()

auth_token = token1 or token2

if auth_token.startswith("oauth:"):
    auth_token = auth_token.replace("oauth:", "")

if not auth_token:
    print("❌ Ошибка: Переменные TWITCH_TOKEN_1 / TWITCH_TOKEN_2 пустые!")
    sys.exit(1)

# 4. Подготовка cookie-файлов
username = "Bot"
jar = RequestsCookieJar()
jar.set("auth-token", auth_token, domain=".twitch.tv", path="/")

os.makedirs("analytics", exist_ok=True)
os.makedirs(f"analytics/{username}", exist_ok=True)

cookie_paths = [
    "cookies.pkl",
    f"analytics/{username}/cookies.pkl",
    "analytics/cookies.pkl"
]

for path in cookie_paths:
    try:
        with open(path, "wb") as f:
            pickle.dump(jar, f)
    except Exception:
        pass

# 5. Инициализация майнера с отключенной аналитикой
miner = TwitchChannelPointsMiner(
    username=username,
    claim_drops_startup=True,
    enable_analytics=False  # Отключает проблемные запросы к spade.twitch.tv
)

if hasattr(miner, "twitch") and hasattr(miner.twitch, "session"):
    miner.twitch.session.cookies.update(jar)

# 6. Список стримеров
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

# 7. Запуск
miner.mine(
    streamers,
    followers=False
)
