import os
import requests
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TEXT = """ Testing"""

@Client.on_message(filters.regex("/rks1 e1"))
async def kuchhbhimsg(_, message):
  await message.reply_text(TEXT)


EP = """ **| S4 E590 | 480p** 💥
**Title** : [Krishna to the Rescue](https://t.me/RKrishnaa)
**Date** : 26th Dec, 2022 
**By** : @RKrishnaa ❣
..
• @RadheKrishn_sb 🍁 
.."""

@Client.on_message(filters.regex("/rks4 E590"))
async def ep1msg(_, message):
    reply = message.reply_to_message
      msg = await message.reply("Processing...⏳")
    return 
    kd = await message.reply_video('BAACAgQAAx0CanN8uQACGbFjqXRemXG2Jk2BLxB8m_8G05rFbQACPBYAAglgSFEK-uNSiqHz_h4E', caption=EP, reply_to_message_id=message.id)
    await asyncio.sleep(30)
    await kd.delete()
    await message.delete()


#Button
START_BUTTONS1=[
    [
        InlineKeyboardButton('Source', url='https://github.com/X-Gorn/File-Sharing'),
        InlineKeyboardButton('Project Channel', url='https://t.me/xTeamBots'),
    ],
    [InlineKeyboardButton('Author', url="https://t.me/xgorn")],
]

# Start & Get file
@xbot.on_message(filters.command('start') & filters.private)
async def _startfile(bot, update):
    if update.text == '/start':
        await update.reply_text(
            f"I'm File-Sharing!\nYou can share any telegram files and get the sharing link using this bot!\n\n/help for more details...",
            True, reply_markup=InlineKeyboardMarkup(START_BUTTONS1))
        return

    if len(update.command) != 2:
        return
    code = update.command[1]
    if '-' in code:
        msg_id = code.split('-')[-1]
        # due to new type of file_unique_id, it can contain "-" sign like "agadyruaas-puuo"
        unique_id = '-'.join(code.split('-')[0:-1])

        if not msg_id.isdigit():
            return
        try:  # If message not belong to media group raise exception
            check_media_group = await bot.get_media_group(TRACK_CHANNEL, int(msg_id))
            check = check_media_group[0]  # Because func return`s list obj
        except Exception:
            check = await bot.get_messages(LOG_CHANNEL, int(msg_id))

        if check.empty:
            await update.reply_text('Error: [Message does not exist]\n/help for more details...')
            return
        if check.video:
            unique_idx = check.video.file_unique_id
        elif check.photo:
            unique_idx = check.photo.file_unique_id
        elif check.audio:
            unique_idx = check.audio.file_unique_id
        elif check.document:
            unique_idx = check.document.file_unique_id
        elif check.sticker:
            unique_idx = check.sticker.file_unique_id
        elif check.animation:
            unique_idx = check.animation.file_unique_id
        elif check.voice:
            unique_idx = check.voice.file_unique_id
        elif check.video_note:
            unique_idx = check.video_note.file_unique_id
        if unique_id != unique_idx.lower():
            return
        try:  # If message not belong to media group raise exception
            await bot.copy_media_group(update.from_user.id, LOG_CHANNEL, int(msg_id))
        except Exception:
            await check.copy(update.from_user.id)
    else:
        return


# Help msg
@Client.on_message(filters.command('helps') & filters.private)
async def _help(bot, update):
    await update.reply_text("Supported file types:\n\n- Video\n- Audio\n- Photo\n- Document\n- Sticker\n- GIF\n- Voice note\n- Video note\n\n If bot didn't respond, contact @xgorn", True)


async def __reply(update, copied):
    msg_id = copied.message_id
    if copied.video:
        unique_idx = copied.video.file_unique_id
    elif copied.photo:
        unique_idx = copied.photo.file_unique_id
    elif copied.audio:
        unique_idx = copied.audio.file_unique_id
    elif copied.document:
        unique_idx = copied.document.file_unique_id
    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id
    elif copied.animation:
        unique_idx = copied.animation.file_unique_id
    elif copied.voice:
        unique_idx = copied.voice.file_unique_id
    elif copied.video_note:
        unique_idx = copied.video_note.file_unique_id
    else:
        await copied.delete()
        return

    await update.reply_text(
        'Here is Your Sharing Link:',
        True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Sharing Link',
                                  url=f'https://t.me/{xbot_username}?start={unique_idx.lower()}-{str(msg_id)}')]
        ])
    )
    await asyncio.sleep(0.5)  # Wait do to avoid 5 sec flood ban 

# Store media_group
media_group_id = 0
@Client.on_message(filters.media & filters.private & filters.media_group)
async def _main_grop(bot, update):
    global media_group_id
    if ADMINS == 'all':
        pass
    elif int(ADMINS) == update.from_user.id:
        pass
    else:
        return

    if int(media_group_id) != int(update.media_group_id):
        media_group_id = update.media_group_id
        copied = (await bot.copy_media_group(LOG_CHANNEL, update.from_user.id, update.message_id))[0]
        await __reply(update, copied)

    else:
        # This handler catch EVERY message with [update.media_group_id] param
        # So we should ignore next >1_media_group_id messages
        return


# Store file
@Client.on_message(filters.media & filters.private & ~filters.media_group)
async def _main(bot, update):
    if ADMINS == 'all':
        pass
    elif int(ADMINS) == update.from_user.id:
        pass
    else:
        return

    copied = await update.copy(LOG_CHANNEL)
    await __reply(update, copied)
                 
