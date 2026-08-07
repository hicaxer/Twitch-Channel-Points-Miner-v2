import os
import sys
import builtins
import importlib

# Перехватываем вызовы input(), чтобы избежать EOFError в GitHub Actions
def non_interactive_input(prompt=""):
    print(f"[Auto-Input Blocking] Перехвачен запрос ввода: {prompt}")
    raise KeyboardInterrupt("Консольный ввод недоступен в GitHub Actions (проверьте валидность OAuth-токена).")

builtins.input = non_interactive_input

# Функция для динамического поиска и импорта классов
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

# Импортируем ключевые классы
TwitchChannelPointsMiner = get_class("TwitchChannelPointsMiner")
Streamer = get_class("Streamer")

if not TwitchChannelPointsMiner or not Streamer:
    print("❌ Не удалось найти необходимые классы!")
    sys.exit(1)

# Получаем токены из секретов GitHub Actions
token1 = os.environ.get("TWITCH_TOKEN_1", "")
token2 = os.environ.get("TWITCH_TOKEN_2", "")

# Выбираем доступный токен
auth_token = token1 or token2

if not auth_token:
    print("❌ Ошибка: Ни один OAuth-токен (TWITCH_TOKEN_1 или TWITCH_TOKEN_2) не передан!")
    sys.exit(1)

# Форматируем токен при необходимости
if not auth_token.startswith("oauth:") and len(auth_token) == 30:
    auth_token = f"oauth:{auth_token}"

# Инициализация майнера
try:
    miner = TwitchChannelPointsMiner(
        username="Bot",
        claim_drops_startup=True,
        oauth_token=auth_token
    )
except TypeError:
    miner = TwitchChannelPointsMiner(
        username="Bot",
        claim_drops_startup=True
    )
    if hasattr(miner, "oauth_token"):
        miner.oauth_token = auth_token

# Список стримеров
streamers = [
    Streamer("foxsi_pubg"),
    Streamer("tsunavohka")
]

# Запуск майнинга
miner.mine(
    streamers,
    followers=False
)
