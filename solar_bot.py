
import requests
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import nest_asyncio

# Mevcut döngüyü desteklemek için
nest_asyncio.apply()

async def get_solar_radiation_data():
    latitude = 40.8402  # Düzce'nin enlemi
    longitude = 30.8753  # Düzce'nin boylamı
    start_date = "20240101"  # Başlangıç tarihi
    end_date = "20240131"  # Bitiş tarihi

    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"
    response = requests.get(url)
    data = response.json()
    return data

def save_to_excel(data, filename):
    df = pd.DataFrame(data['properties']['parameter']['ALLSKY_SFC_SW_DWN'])
    df.to_excel(filename, index=False)

async def solar_radiation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_solar_radiation_data()
    filename = "solar_radiation_data.xlsx"
    save_to_excel(data, filename)

    with open(filename, 'rb') as file:
        await update.message.reply_document(file)

async def main():
    # Telegram bot tokeninizi buraya ekleyin
    application = ApplicationBuilder().token("7347737370:AAEAXbWMy57fWffbHCFh4Q7hSXVNH62-MMY").build()
    
    application.add_handler(CommandHandler("solar_radyasyon", solar_radiation))
    
    # Botu başlat
    await application.run_polling()

# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    asyncio.run(main())
