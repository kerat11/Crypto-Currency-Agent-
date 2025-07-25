import os
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in .env file")

import openai
openai.api_key = api_key

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content

    if "price" in user_input.lower():
        symbol = "BTCUSDT"  # Default symbol
        if "eth" in user_input.lower():
            symbol = "ETHUSDT"
        elif "bnb" in user_input.lower():
            symbol = "BNBUSDT"

        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url)
            price = response.json()["price"]
            reply = f"The current price of **{symbol}** is **${price}**."
        except Exception as e:
            reply = f"Error fetching price: {e}"
    else:
        # Let OpenAI respond normally
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = completion.choices[0].message.content

    await cl.Message(content=reply).send()
