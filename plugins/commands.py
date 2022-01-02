import os
import logging
import random
from Script import script
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, LOG_CHANNEL, PICS, JOIN_IMG
from utils import get_size, is_subscribed, temp

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('🤴ʙᴏᴛ ᴏᴡɴᴇʀ🤴', url=f'https://t.me/im_odiyan'),
            InlineKeyboardButton('🍁ʙᴏᴛ ɢʀᴏᴜᴘ🍁', url='https://t.me/Cinemalokham1')    
            ],[
            InlineKeyboardButton('🍿ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ🍿', url='https://t.me/LatestmoviedriveCL')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "🤖 Join Updates Channel", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            btn.append([InlineKeyboardButton("🌀ʜᴇʟʟᴏ.. ɪ ᴀᴍ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ🌀", callback_data=f"checksub#{message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            photo=JOIN_IMG, caption=f"**❯────「ɪ ɴ ғ ᴏ ʀ ᴍ ᴀ ᴛ ɪ ᴏ ɴ」────❮\n\nആദ്യം [【 ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ɢʀᴏᴜᴘ 】](https://t.me/LatestmoviedriveCL1) എന്ന ബട്ടൺ ക്ലിക്ക് ചെയ്തു ഗ്രൂപ്പിൽ ജോയിൻ ചെയ്.എന്നിട്ട് വീണ്ടു ബോട്ടിൽ വന്നിട്ട്【 ʜᴇʟʟᴏ.. ɪ ᴀᴍ ᴊᴏɪɴᴇᴅ 】എന്ന ബട്ടൺ ക്ലിക്ക് ചെയ്താൽ ഫയൽ കിട്ടുന്നതായിറിക്കും\n\nFɪʀsᴛ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ [【 ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ɢʀᴏᴜᴘ 】](https://t.me/LatestmoviedriveCL) ʙᴜᴛᴛᴏɴ ᴀɴᴅ ᴊᴏɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ. ᴛʜᴇɴ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴄʟɪᴄᴋ ᴏɴ【 ʜᴇʟʟᴏ.. ɪ ᴀᴍ ᴊᴏɪɴᴇᴅ 】ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇ...\n\n(c) copyrights 2021 @Cinemalokham1**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
        return
    if len(message.command) ==2 and message.command[1] in ["subscribe", "error", "okay"]:
        buttons = [[
            InlineKeyboardButton('🤴ʙᴏᴛ ᴏᴡɴᴇʀ🤴', url=f'https://t.me/im_odiyan'),
            InlineKeyboardButton('🍁ʙᴏᴛ ɢʀᴏᴜᴘ🍁', url='https://t.me/Cinemalokham1')    
            ],[
            InlineKeyboardButton('🍿ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ🍿', url='https://t.me/LatestmoviedriveCL')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
        return
    file_id = message.command[1]
    files = (await get_file_details(file_id))[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
        except Exception as e:
            print(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    buttons = [
        [
            InlineKeyboardButton("🍁 ᴊᴏɪɴ ɢʀᴏᴜᴘ 🍁", url="https://t.me/Cinemalokham1"),
            InlineKeyboardButton("💥 ꜱʜᴀʀᴇ 💥", url="https://t.me/share/url?url=**%F0%9F%A4%A9%20%E0%B4%B8%E0%B4%BF%E0%B4%A8%E0%B4%BF%E0%B4%AE%20%E0%B4%B2%E0%B5%8B%E0%B4%95%E0%B4%82%20%F0%9F%A4%A9%0A%0A%E0%B4%8F%E0%B4%A4%E0%B5%8D%20%E0%B4%85%E0%B5%BC%E0%B4%A7%E0%B4%B0%E0%B4%BE%E0%B4%A4%E0%B5%8D%E0%B4%B0%E0%B4%BF%20%E0%B4%9A%E0%B5%8B%E0%B4%A6%E0%B4%BF%E0%B4%9A%E0%B5%8D%E0%B4%9A%E0%B4%BE%E0%B4%B2%E0%B5%81%E0%B4%82%20%E0%B4%AA%E0%B4%9F%E0%B4%82%20%E0%B4%95%E0%B4%BF%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B5%81%E0%B4%82,%20%E0%B4%B2%E0%B5%8B%E0%B4%95%E0%B4%A4%E0%B5%8D%E0%B4%A4%E0%B4%BF%E0%B4%B2%E0%B5%86%20%E0%B4%92%E0%B4%9F%E0%B5%8D%E0%B4%9F%E0%B5%81%E0%B4%AE%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%20%E0%B4%AD%E0%B4%BE%E0%B4%B7%E0%B4%95%E0%B4%B3%E0%B4%BF%E0%B4%B2%E0%B5%81%E0%B4%AE%E0%B5%81%E0%B4%B3%E0%B5%8D%E0%B4%B3%20%E0%B4%B8%E0%B4%BF%E0%B4%A8%E0%B4%BF%E0%B4%AE%E0%B4%95%E0%B4%B3%E0%B5%81%E0%B4%9F%E0%B5%86%20%E0%B4%95%E0%B4%B3%E0%B4%95%E0%B5%8D%E0%B4%B7%E0%B5%BB..%20%E2%9D%A4%EF%B8%8F%0A%0A%F0%9F%91%87%20GROUP%20LINK%20%F0%9F%91%87%0A@Cinemalokham1%0A@Cinemalokham1%0A@Cinemalokham1**")
        ],
        [
            InlineKeyboardButton("🔖 ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴜʙᴛɪᴛɪʟᴇ 🔖", url="https://t.me/subtitle_dl_bot")
        ]
        ]                    
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup(buttons)
        )
                    

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer()
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

