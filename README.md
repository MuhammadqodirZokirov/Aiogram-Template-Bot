# Aiogram-Template-Bot
Aiogram 3.x boti uchun tana (Python 3.10+)

Kerakli kutubxonalarni yuklab olish

```
pip install -r requirements.txt
```

`.env.example` dan nusxa olib `.env` fayl yarating va to'ldiring:

```
cp .env.example .env
```

Botni yurgizish:

```
python app.py
```

## Tuzilma

- `handlers/` — har bir modul o'z `Router`iga ega, `handlers.setup_routers()` ularni birlashtiradi
- `middlewares/` — `ThrottlingMiddleware` (antiflood)
- `utils/misc/throttling.py` — `rate_limit` dekoratori:

```python
@router.message(Command("test"))
@rate_limit(5, "test")
async def test(message: Message): ...
```
