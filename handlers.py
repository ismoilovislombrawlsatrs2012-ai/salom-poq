from aiogram.types import Message,CallbackQuery
from keyboards import inline_murkup
import requests
Weather_api_key = "257d046bc3fb0a27d808df3e2feb7361"

async def start_command_answer(message: Message):
    await message.answer(f"Assalomu aleykum! Botga xush kelibsiz.\nBiror shaharni tanlang shu shaharni ob havosini ko'rsataman!",reply_markup=inline_murkup)


async def Get_ob_havo(calback_data : CallbackQuery):

    city_name = calback_data.data
   

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={Weather_api_key}&units=metric").json()
    namoz_vaqtlari = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={city_name}&country=Uzbekistan&method=2").json()



    havo_turi = weather_data['weather'][0]['description']
    havo_harorati = weather_data['main']["temp"]
    tana_sezadigan_harora = weather_data["main"]["feels_like"]
    namlik = weather_data["main"]['humidity']
    city_name = weather_data["name"]



    malumotlar = f"""
    🌤 <b>Ob-havo ma'lumotlari</b>

    📍 Shahar: <b>{city_name}</b>

    🌡 Harorat: <b>{havo_harorati}°C</b>
    🤒 Tana sezadigan harorat: <b>{tana_sezadigan_harora}°C</b>

    ☁️ Havo holati: <b>{havo_turi}</b>
    💧 Namlik: <b>{namlik}%</b>

    📊 Yaxshi kun tilaymiz!
    """
        
    bomdod_namozi = namoz_vaqtlari["data"]["timings"]["Fajr"]
    quyosh_chiqishi = namoz_vaqtlari["data"]["timings"]["Sunrise"]
    peshin_namozi = namoz_vaqtlari["data"]["timings"]["Dhuhr"]
    asr_namozi = namoz_vaqtlari["data"]["timings"]["Asr"]
    shom_namozi = namoz_vaqtlari["data"]["timings"]["Maghrib"]
    xufton_namozi = namoz_vaqtlari["data"]["timings"]["Isha"]
    saharlik_tugashi = namoz_vaqtlari["data"]["timings"]["Imsak"]
    text = f"""
    🕌 <b>Bugungi namoz vaqtlari</b>

    🌙 Saharlik tugashi: <b>{saharlik_tugashi}</b>

    🌅 Bomdod: <b>{bomdod_namozi}</b>
    🌄 Quyosh chiqishi: <b>{quyosh_chiqishi}</b>

    ☀️ Peshin: <b>{peshin_namozi}</b>
    🌤 Asr: <b>{asr_namozi}</b>

    🌇 Shom: <b>{shom_namozi}</b>
    🌙 Xufton: <b>{xufton_namozi}</b>

    🤲 Alloh ibodatlaringizni qabul qilsin!
    """


    await calback_data.message.answer(text=malumotlar,parse_mode="HTML")
    await calback_data.message.answer(text=text,parse_mode="HTML")