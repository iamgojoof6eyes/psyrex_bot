import os

from pyrogram import Client, filters
from pyrogram.enums import ChatType
# from pyrogram.errors import RPCError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from configs import *
from extra import *
from help import *

psy = Client(
    "psy",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pre = PREFIX_HANDLER
CT = ChatType


@psy.on_message(filters.command(["start"], pre))
async def start(_, m: Message):
    me = await psy.get_me()
    BOT_USERNAME = me.username
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "I am alive",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Switch to pm", 
                        url=f"https://{BOT_USERNAME}.t.me",
                        ),
                    ],
                ],
            )
        )

    else:
        await psy.send_message(
            m.chat.id,
            "Forward me any media or message I will forward to the targeted chat.\nUse /help to see the list of commands"
        )
    return
    
@psy.on_message(filters.command(["help"], pre))
async def help(_, m: Message):
    me = await psy.get_me()
    BOT_USERNAME = me.username
    if m.chat.type != CT.PRIVATE:
        await m.reply_text(
            "What do u want to know",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        "Help", 
                        url=f"t.me/{BOT_USERNAME}?start=help",
                        ),
                    ],
                ],
            )
        )
    else:
        await psy.send_message(
            m.chat.id,
            helpmsg
        )
    return

@psy.on_message(filters.command(["addchannel"], pre))
async def addchannel(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:    
        splited = m.text.split(None,1)[1]
        c_id = int(splited)
    except Exception:
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/addchannel <channel id>`")
        x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nAdding current chat ({c_id}) to list")
    channel.append(c_id)
    x.delete()
    return await m.reply_text(f"Added `{c_id}` in the Channel list")


@psy.on_message(filters.command(["rmchannel", "removechannel"], pre))
async def rmchannel(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:
        splited = m.text.split(None, 1)[1]
        c_id = int(splited)
    except Exception:
        if splited.lower() == "all":
            x = await m.reply_text("Clearing all channel id from list")
            channel.clear()
            x.delete()
            return await m.reply_text("Done")
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/rmchannel <channel id> / all`")
        x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nRemoveing current chat ({c_id}) from list")
    if c_id in channel:
        channel.remove(c_id)
        x.delete()
        return await m.reply_text(f"Removed `{c_id}` from the channel list")
    return await m.reply_text(f"{c_id} is not in the list. How am I supposed to remove it?")

@psy.on_message(filters.command(["addsudo", "appendsudo"], pre))
async def addsudo(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and not replied:
        return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    if (len(splited)==2) and not replied:
        try:
            u_id = int(splited[1])
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    elif replied and not (len(splited)==2):
        try:
            u_id = int(replied.from_user.id)
        except Exception:
            return await m.reply_text("**USAGE:** `/addsudo` <user id>")
    else:
        return await m.reply_text("Either reply to a user or pass user id don't do both thing at once")
    SUDOER.append(u_id)
    return await m.reply_text(f"Added `{u_id}` in sudoer list")

@psy.on_message(filters.command(["rmsudo", "removesudo"], pre))
async def rmsudo(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 and replied:
        return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    if splited:
        try:
            if splited not in SUDOER:
                return await m.reply_text("User is not a sudoer")
            u_id = int(splited[1])
        except Exception:
            if splited.lower() == "all":
                x = await m.reply_text("Clearing all channel id from list")
                channel.clear()
                x.delete()
                return await m.reply_text("Done")
            return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    if replied:
        try:
            if replied.from_user.id not in SUDOER:
                return await m.reply_text("User is not a sudoer")
            u_id = int(replied.from_user.id)
        except Exception:
            return await m.reply_text("**USAGE:** `/rmsudo` <user id>")
    SUDOER.remove(u_id)
    return await m.reply_text(f"Removed `{u_id}` from sudoer list")


@psy.on_message(filters.command(["forwardto", "fto"], pre) & filters.text)
async def forwardto(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    splited = m.text.split(None, 1)
    replied = m.reply_to_message
    if len(splited) != 2 or not replied:
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>\n**REPLY TO A MESSAGE**")
    try:
        c_id = int(splited[1])
    except Exception:
        return await m.reply_text("**USAGE:** `/forwardto` <channel id>")
    if not bool(m.photo or m.document or m.video):
        return await m.reply_text("Reply to an image or document or video")
    try:
        file = await replied.download()
        if replied.caption:
            caption = replied.caption
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")
    if not file:
        return await m.reply_text("I can't download that!")
    try:
        if caption:
            if m.photo or m.document.file_name.endswith(exe):
                x = await psy.send_photo(c_id, file, caption)
                await x.reply_document(file, caption=caption)
            if m.document:
                await psy.send_document(c_id, file, caption)
            if m.video:
                await psy.send_video(c_id, file, caption)
        else:
            if m.photo or m.document.file_name.endswith(exe):
                x = await psy.send_photo(c_id, file)
                await x.reply_document(file)
            if m.document:
                await psy.send_document(c_id, file)
            if m.video:
                await psy.send_video(c_id, file)
        os.remove(file)
        return await m.reply_text("Done!")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.command(["channels", "sudos", "default"], pre))
async def channel_sudo(_, m: Message):
    if len(m.text.split()) != 1:
        return await m.reply_text("Do /help to get help")
    try:
        if m.text.lower() == "/channels":
            req = ", ".join(channel)
            return await m.reply_text(f"Here is the list of channel:\n`{req}`")
        elif m.text.lower() == "/default":
            return await m.reply_text(f"The Default chat is `{default[0]}`")
        req = ", ".join(SUDOER)
        return m.reply_text(f"Here is the list of channel:\n`{req}`")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.command(["apdefault"], pre))
async def add_default(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:    
        splited = m.text.split(None,1)[1]
        c_id = int(splited)
    except IndexError:
        c_id = int(m.chat.id)
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/apdefault <channel id>`")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")
    x = await m.reply_text(f"Either no chat id is provided or provided arg is not int type.\nAdding current chat ({c_id}) as default")
    default.clear()
    default.append(c_id)
    x.delete()
    return await m.reply_text(f"Added `{c_id}` as default channel")

@psy.on_message(filters.command(["rmdefault"], pre))
async def rm_default(_, m: Message):
    if m.from_user.id not in SUDOER:
        return await m.reply_text("You can't do that")
    try:
        if m.chat.type == CT.PRIVATE:
            return await m.reply_text("**USAGE:**\n`/rmdefault <channel id>`")
        x = await m.reply_text(f"Clearing default channel.")
        default.clear()
        x.delete()
        return await m.reply_text("Cleared default channel")
    except Exception as e:
        return await m.reply_text(f"Got an error:\n{e}")

@psy.on_message(filters.private & (filters.photo | filters.document | filters.video))
async def forwarder(_, m: Message):
    # me = await psy.get_me()
    # BOT_ID = me.id
    if m.from_user.id in SUDOER:
        if not bool(m.photo or m.document or m.video):
            return await m.reply_text("Send photo or document or video")
        if m.caption:
            caption = m.caption
        try:
            file = await m.download()
        except Exception as e:
            return await m.reply_text(f"Got an error:\n{e}")
        if not file:
            return await m.reply_text("I can't download that!")
        if caption:
            splited = caption.split()[-1]
            try:
                c_id = int(splited)
                caption = caption.strip(str(c_id))
                if m.photo or m.document.file_name.endswith(exe):
                    x = await psy.send_photo(c_id, file, caption)
                    await x.reply_document(file, caption=caption)
                    os.remove(file)
                    return await m.reply_text("Done!")
                if m.document:
                    await psy.send_document(c_id, file, caption=caption)
                    os.remove(file)
                    return await m.reply_text("Done!")
                if m.video:
                    await psy.send_video(c_id, file, caption=caption)
                    os.remove(file)
                    return await m.reply_text("Done!")
            except Exception:
                pass
        try:
            if not default:
                if len(channel) == 1:
                    c_id = channel[0]
                    if m.photo or m.document.file_name.endswith(exe):
                        if caption:
                            x = await psy.send_photo(c_id, file, caption)
                            await x.reply_document(file, caption=caption)
                        if not caption:
                            x = await psy.send_photo(c_id, file)
                            await x.reply_document(file)
                        os.remove(file)
                        return await m.reply_text("Done!")
                    if m.document:
                        if caption:
                            await psy.send_document(c_id, file, caption=caption)
                        if not caption:
                            await psy.send_document(c_id, file)
                        os.remove(file)
                        return await m.reply_text("Done!")
                    if m.video:
                        if caption:
                            await psy.send_video(c_id, file, caption=caption)
                        if not caption:
                            await psy.send_video(c_id, file)
                        os.remove(file)
                        return await m.reply_text("Done!")
                channel = list(set(channel))
                async for c_id in channel:
                    if m.photo or m.document.file_name.endswith(exe):
                        if caption:
                            x = await psy.send_photo(c_id, file, caption)
                            await x.reply_document(file, caption=caption)
                        if not caption:
                            x = await psy.send_photo(c_id, file)
                            await x.reply_document(file)
                        os.remove(file)
                        return await m.reply_text("Done!")
                    if m.document:
                        if caption:
                            await psy.send_document(c_id, file, caption=caption)
                        if not caption:
                            await psy.send_document(c_id, file)
                        os.remove(file)
                        return await m.reply_text("Done!")
                    if m.video:
                        if caption:
                            await psy.send_video(c_id, file, caption=caption)
                        if not caption:
                            await psy.send_video(c_id, file)
                        os.remove(file)
                        return await m.reply_text("Done!")
            c_id = default[0]
            if m.photo or m.document.file_name.endswith(exe):
                if caption:
                    x = await psy.send_photo(c_id, file, caption)
                    await x.reply_document(file, caption=caption)
                if not caption:
                    x = await psy.send_photo(c_id, file)
                    await x.reply_document(file)
                os.remove(file)
                return await m.reply_text("Done!")
            if m.document:
                if caption:
                    await psy.send_document(c_id, file, caption=caption)
                if not caption:
                    await psy.send_document(c_id, file)
                os.remove(file)
                return await m.reply_text("Done!")
            if m.video:
                if caption:
                    await psy.send_video(c_id, file, caption=caption)
                if not caption:
                    await psy.send_video(c_id, file)
        except Exception as e:
            return await m.reply_text(f"Got an error:\n{e}")
    else:
        pass

psy.run()
