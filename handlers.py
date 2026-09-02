from aiogram.types import Message, CallbackQuery
from keyboards import inline_murkup
import aiohttp
import urllib.parse
import json
import os

# Owner and default settings
OWNER_ID = int(os.environ.get("OWNER_ID", "7877142193"))  # set via environment variable if desired
STATE_FILE = "bot_state.json"
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "257d046bc3fb0a27d808df3e2feb7361")

# Default initial state: owner is considered away (bot replies on their behalf)
_default_state = {
    "owner_id": OWNER_ID,
    "away": True,
    "phone": ""
}


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return _default_state.copy()
    return _default_state.copy()


def save_state(state: dict):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


_state = load_state()


async def start_command_answer(message: Message):
    await message.answer(
        "Assalomu aleykum! Botga xush kelibsiz.\n"
        "Biror shaharni yozing yoki pastdagi tugmalardan birini tanlang — shaharning ob-havosini va namoz vaqtlarini ko'rsataman!\n\n"
        "Agar men offline bo'lsam, men o'rningizga avtomatik javob beraman.\n"
        "Agar siz bot egasiga murojaat qilmoqchi bo'lsangiz, telefon: " + (_state.get("phone") or "(yozilmagan)"),
        reply_markup=inline_murkup
    )


async def _fetch_json(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as resp:
        try:
            data = await resp.json()
        except Exception:
            text = await resp.text()
            raise RuntimeError(f"Not JSON response: {text[:200]}")
        return resp.status, data


async def _build_and_send(city_name: str, send_func):
    # encode city name for URLs
    city_q = urllib.parse.quote(city_name)
    async with aiohttp.ClientSession() as session:
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_q}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
        )
        namaz_url = (
            f"http://api.aladhan.com/v1/timingsByCity?city={city_q}"
            f"&country=Uzbekistan&method=2"
        )

        w_status, weather_data = await _fetch_json(session, weather_url)
        n_status, namoz_vaqtlari = await _fetch_json(session, namaz_url)

        # OpenWeather returns 200 on success; cod may be a number or string
        if w_status != 200 or str(weather_data.get("cod", "")) == "404":
            raise ValueError("Shahar topilmadi yoki ob-havo API xatosi yuz berdi.")

        if n_status != 200 or namoz_vaqtlari.get("code") != 200:
            raise ValueError("Namoz vaqtlari API-sida xatolik yuz berdi.")

        havo_turi = weather_data['weather'][0].get('description', '').capitalize()
        havo_harorati = weather_data['main'].get("temp")
        tana_sezadigan_harora = weather_data['main'].get("feels_like")
        namlik = weather_data['main'].get('humidity')
        city_pretty = weather_data.get("name", city_name)

        malumotlar = (
            f"🌤 <b>Ob-havo ma'lumotlari</b>\n\n"
            f"📍 Shahar: <b>{city_pretty}</b>\n\n"
            f"🌡 Harorat: <b>{havo_harorati}°C</b>\n"
            f"🤒 Tana sezadigan harorat: <b>{tana_sezadigan_harora}°C</b>\n\n"
            f"☁️ Havo holati: <b>{havo_turi}</b>\n"
            f"💧 Namlik: <b>{namlik}%</b>\n\n"
            f"📊 Yaxshi kun tilaymiz!"
        )

        timings = namoz_vaqtlari.get("data", {}).get("timings", {})
        bomdod_namozi = timings.get("Fajr", "-")
        quyosh_chiqishi = timings.get("Sunrise", "-")
        peshin_namozi = timings.get("Dhuhr", "-")
        asr_namozi = timings.get("Asr", "-")
        shom_namozi = timings.get("Maghrib", "-")
        xufton_namozi = timings.get("Isha", "-")
        saharlik_tugashi = timings.get("Imsak", "-")

        text = (
            f"🕌 <b>Bugungi namoz vaqtlari</b>\n\n"
            f"🌙 Saharlik tugashi: <b>{saharlik_tugashi}</b>\n\n"
            f"🌅 Bomdod: <b>{bomdod_namozi}</b>\n"
            f"🌄 Quyosh chiqishi: <b>{quyosh_chiqishi}</b>\n\n"
            f"☀️ Peshin: <b>{peshin_namozi}</b>\n"
            f"🌤 Asr: <b>{asr_namozi}</b>\n\n"
            f"🌇 Shom: <b>{shom_namozi}</b>\n"
            f"🌙 Xufton: <b>{xufton_namozi}</b>\n\n"
            f"🤲 Alloh ibodatlaringizni qabul qilsin!"
        )

        await send_func(malumotlar, parse_mode="HTML")
        await send_func(text, parse_mode="HTML")


async def Get_ob_havo_callback(callback: CallbackQuery):
    city_name = callback.data or ""
    await callback.answer()  # acknowledge callback
    try:
        async def _send(text, parse_mode=None):
            await callback.message.answer(text=text, parse_mode=parse_mode)

        await _build_and_send(city_name, _send)
    except ValueError as e:
        await callback.message.answer(str(e))
    except Exception:
        await callback.message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")


async def handle_city_message(message: Message):
    # Keep existing weather behavior if user sends a city name directly
    city_name = (message.text or "").strip()
    if not city_name or city_name.startswith("/"):
        return

    try:
        async def _send(text, parse_mode=None):
            await message.answer(text=text, parse_mode=parse_mode)

        await _build_and_send(city_name, _send)
    except ValueError as e:
        await message.answer(str(e))
    except Exception:
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")


# --- Away / auto-reply behavior ---
async def _send_away_reply_and_forward(message: Message):
    """
    When owner is away, reply to incoming messages and forward them to the owner.
    Works for private and group chats. For groups, the bot will reply in the group
    and also forward the message to the owner with context.
    """
    state = _state
    owner = state.get("owner_id") or OWNER_ID
    phone = state.get("phone") or "(telefon berilmagan)"

    away_text = (
        "Salom! Bot egasi hozir offline.\n"
        "Sizning xabaringiz qabul qilindi — tez orada javob berish uchun ular bilan bog'laning.\n\n"
        f"Murojat uchun telefon: {phone}\n\n"
        "Agar shoshilinch bo'lsa, telefon orqali murojaat qiling."
    )

    # Reply in the same chat (private or group)
    try:
        # If group, reply to message; in private chat, just send
        await message.reply(away_text)
    except Exception:
        try:
            await message.answer(away_text)
        except Exception:
            pass

    # Forward original message to owner and add context
    if owner:
        try:
            # forward the original message for owner to see
            await message.forward(chat_id=owner)
        except Exception:
            # if forwarding fails, send a textual summary
            try:
                chat = message.chat
                chat_info = f"Chat: {chat.title or chat.username or chat.id} (id={chat.id})"
                sender = message.from_user
                sender_info = f"From: {sender.full_name} (id={sender.id})"
                snippet = (message.text or "<non-text message>")[:800]
                await message.bot.send_message(
                    owner,
                    f"[{chat_info}] {sender_info}\n\n{snippet}"
                )
            except Exception:
                pass


async def incoming_message_autoreply(message: Message):
    """
    General handler for incoming messages. If owner is away and sender is not the owner,
    bot replies on owner's behalf and forwards the message to the owner.
    """
    # ignore messages sent by the bot itself
    if message.from_user and message.from_user.is_bot:
        return

    state = _state
    owner = state.get("owner_id") or OWNER_ID

    # If the message is from the owner, do nothing here (owner commands handled separately)
    if message.from_user and message.from_user.id == owner:
        return

    # If owner is away, auto-reply and forward
    if state.get("away"):
        await _send_away_reply_and_forward(message)


# Owner-only commands to control away mode and phone
async def away_command(message: Message):
    if not message.from_user or message.from_user.id != (_state.get("owner_id") or OWNER_ID):
        return
    _state["away"] = True
    save_state(_state)
    await message.answer("Siz hozir offline rejimidasiz — bot endi o'rningizga javob beradi.")


async def back_command(message: Message):
    if not message.from_user or message.from_user.id != (_state.get("owner_id") or OWNER_ID):
        return
    _state["away"] = False
    save_state(_state)
    await message.answer("Siz hozir online — bot avtomatik javobni o'chirdi.")


async def setphone_command(message: Message):
    """Usage: /setphone +998901234567"""
    if not message.from_user or message.from_user.id != (_state.get("owner_id") or OWNER_ID):
        return
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos telefon raqamni ko'rsating. Misol: /setphone +998901234567")
        return
    phone = args[1].strip()
    _state["phone"] = phone
    save_state(_state)
    await message.answer(f"Telefon raqam yangilandi: {phone}")


async def status_command(message: Message):
    if not message.from_user or message.from_user.id != (_state.get("owner_id") or OWNER_ID):
        return
    away = _state.get("away")
    phone = _state.get("phone")
    await message.answer(f"Away: {away}\nPhone: {phone}")
