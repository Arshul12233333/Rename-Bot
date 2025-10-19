import os, time, asyncio, shutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# -------------------------------
# CONFIG
# -------------------------------
class Config(object):
    # Pyrogram client config
    API_ID    = os.environ.get("API_ID", "27198464")
    API_HASH  = os.environ.get("API_HASH", "ee48c6b9ca05a9f95db7b78b2d268ea3")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7794252669:AAFQ26m_9A5tABApom87fdibHNAqxmw_KBc") 
   
    # Database config
    DB_NAME = os.environ.get("DB_NAME", "rename")     
    DB_URL  = os.environ.get(
        "DB_URL",
        "mongodb+srv://ArshulGod:ArshulGod@cluster0.u1hpidc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )

    # Other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://i.postimg.cc/gjx0nTGq/IMG-20251013-105149-145.jpg")
    ADMIN = int(os.environ.get("ADMIN", "6333237164"))

    # Channels / Logs
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Anime_Universe_In_Hindi_Dub") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002700449333"))
    
    # Web / server configuration     
    PORT = int(os.environ.get("PORT", "8080"))
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))

# -------------------------------
# TEXT CONFIG
# -------------------------------
class Txt(object):
    START_TXT = """Hello {} 👋 

➻ This Is An Advanced And Yet Powerful Bot.

➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.

➻ You Can Also Convert Video To File And File To Video.

➻ This Bot Also Supports Custom Thumbnail And Custom Caption.

<b>Bot Is Made By :</b> @iwant2boobies"""

    ABOUT_TXT = """
╭───────────────⍟
├🤖 My Name : Anime universe
├🖥️ Developer : @iwant2boobies
├📕 Library : Pyrogram
├✏️ Language : Python 3
├💾 Database : Mongo DB
├📊 Build Version : v4.5.0     
╰───────────────⍟
"""

    HELP_TXT = """
🌌 <b><u>How To Set Thumbnail</u></b>
  
➪ /start - Start The Bot And Send Any Photo To Automatically Set Thumbnail.
➪ /del_thumb - Delete Your Old Thumbnail.
➪ /view_thumb - View Your Current Thumbnail.

📑 <b><u>How To Set Custom Caption</u></b>

➪ /set_caption - Set A Custom Caption
➪ /see_caption - View Your Custom Caption
➪ /del_caption - Delete Your Custom Caption
➪ Example - <code>/set_caption 📕 Name ➠ : {filename}
🔗 Size ➠ : {filesize} 
⏰ Duration ➠ : {duration}</code>

✏️ <b><u>How To Rename A File</u></b>

➪ Send Any File And Type New File Name And Select Format [ Document, Video, Audio ]  

For Support / Help Contact :- <a href=https://t.me/ABOUT_ll_KAKASHI_xd_lll>Click Here</a>
"""

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Size: {1} | {2}
┣⪼ ⏳️ Done : {0}%
┣⪼ 🚀 Speed: {3}/s
┣⪼ ⏰️ ETA: {4}
┣⪼ 🥺 Join Plz: @iwant2boobies
╰━━━━━━━━━━━━━━━➣ </b>"""

    DONATE_TXT = """
<b>Thanks For Showing Interest In Donation! ❤️</b>

If You Like My Bots & Projects, You Can 🎁 Donate Any Amount From 10₹ 😁 Up To Your Choice.

<b>UPI ID:</b> `PandaWep@ybl`
"""

# -------------------------------
# BOT INSTANCE
# -------------------------------
app = Client(
    "AnimeUniverseBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# -------------------------------
# START COMMAND
# -------------------------------
@app.on_message(filters.private & filters.command("start"))
async def start_bot(client, message):
    await message.reply_text(
        Txt.START_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Support", url="https://t.me/ABOUT_ll_KAKASHI_xd_lll")]]
        ),
        disable_web_page_preview=True
    )

# -------------------------------
# CALLBACK QUERY HANDLER
# -------------------------------
@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    await query.answer("Processing...")

    if data == "video":
        await process_file(query, "video")
    elif data == "audio":
        await process_file(query, "audio")
    elif data == "document":
        await process_file(query, "document")

# -------------------------------
# ASYNC FILE PROCESSING
# -------------------------------
async def process_file(query, ftype):
    file_id = query.message.reply_to_message.document.file_id if query.message.reply_to_message.document else None
    if not file_id:
        await query.message.reply_text("No file found to process!")
        return

    file_path = await app.download_media(file_id, file_name=f"downloads/input")
    output_path = f"downloads/output"

    if ftype == "video":
        output_path += ".mp4"
        cmd = ["ffmpeg", "-i", file_path, "-c:v", "copy", "-c:a", "aac", output_path]
    elif ftype == "audio":
        output_path += ".mp3"
        cmd = ["ffmpeg", "-i", file_path, output_path]
    else:  # document
        ext = query.message.reply_to_message.document.file_name.split(".")[-1]
        output_path += f".{ext}"
        shutil.copy(file_path, output_path)

    # Async ffmpeg
    if ftype in ["video", "audio"]:
        proc = await asyncio.create_subprocess_exec(*cmd)
        await proc.wait()

    # Send the file
    await query.message.reply_document(output_path)

    # Log
    try:
        await app.send_message(Config.LOG_CHANNEL, f"File processed by {query.from_user.mention}")
    except Exception as e:
        print("LOG_CHANNEL error:", e)

    # Cleanup
    os.remove(file_path)
    os.remove(output_path)

# -------------------------------
# RUN BOT
# -------------------------------
app.run()
