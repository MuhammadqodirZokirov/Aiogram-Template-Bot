from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN: str = env.str("BOT_TOKEN")  # Bot token
ADMINS: list[int] = env.list("ADMINS", subcast=int, default=[])  # adminlar ro'yxati
IP: str = env.str("IP", default="localhost")  # Xosting ip manzili
