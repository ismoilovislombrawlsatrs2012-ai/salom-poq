from aiogram.types import Message, CallbackQuery
from keyboards import inline_murkup
import aiohttp
import urllib.parse

WEATHER_API_KEY = "257d046bc3fb0a27d808df3e2feb7361"


async def start_command_answer(message: Message):
    await message.answer(
        "Assalomu aleykum! Botga xush kelibsiz.\n"
        "Biror shaharni yozing yoki pastdagi tugmalardan birini tanlang — shaharning ob-havosini va namoz vaqtlarini ko'rsataman!",
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
