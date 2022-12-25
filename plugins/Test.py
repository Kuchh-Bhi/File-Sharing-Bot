import requests
from pyrogram import filters, idle
from pyrogram.types import Message 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TEXT = """ Testing..."""

@Bot.on_message(filters.regex("!rks1 e1"))
async def kuchhbhimsg(_, message):
  await message.reply_text(TEXT)
                 
