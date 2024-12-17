# |========> Import necessary libraries <========|
import random
import re
import os
from time import time
from pyrogram import Client, filters, errors
from pyrogram.enums import ChatType, UserStatus
import logging
import asyncio
import psutil
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pysondb import db

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)

# |========> Global variables <========|

# آیدی عددی ادمین اولیه رو اینجا قرار بده
main_admin_id = 0000000000

# لیست لینکدونی ها را اینجا قرار بده
linkdoni_list = ["@linkdoni","@linkdoniXe","@linkdoniVe","@mehdiLinkdonii","@linkdoni24h","@liinkdooniiraniian","@LinkdoniCactus","@Li_mc","@linkdooni_iraniann", ]

# لیست پیام های پیام خودکار را اینجا قرار بده میتونید هر چقد که میخواید اضافه کنید. ","," با اینا.
auto_chat_texts = ["بچها نفر چنتا استیکر بفرستین پیوی مه از ریپورتی در بیام ممنون:|", "من رل هیچ پسری نیستم(پروفایل 90 درصد دخترا چند سال پیش)😂🐈", "منم اصلا به زندگیم رل نزدم و نمیزنم هیچ موقع😒🥹", "ادمین گروه تو دزد داره همش لینک میفرستن پیوی🐈","احسان جو هستی بیا پی کارت دارم","بچها برای ترم اخر کدوم بخش خوبه؟؟😐","خوشگلم و هزارتا خاطر خا دارم🐈‍⬛️🦋","کاش بشه دوباره برم هرات جو خو🥲👩‍🦯","رل گدا پی🐈‍⬛️","ابجی یه دیقه میایی پیوی کارت دارم🥹","مخو از هراتم شماها از کجایم بچه ها🫤","خستههه شدمممممم","رل چیش ساوز پی👀","بچها برای ترم اخر کدوم بخش خوبه؟؟😐","طرف اماده پیوی سین نمیزنم میگه تو‌ رباتی😔😂🦶🏻","بچها یک فیلتر خوبی بفرستین برام یا پروکسی🥲🥲","چقد هوا سرده کسیو نداریم بغلش گرم بشیم😏😂","بچها شماره خو ایشته مخفی کنم کسی بلده بگه بهم🥹","پشماام قابلیت جدید تلگرامو دیدین؟؟","همی خره ریمو کن هعی پیوی فحش میده😕😕","امشاو میگن شب جمعس🙈😂❤️","فیلم جدید هنانه رو دیدی؟ 🥹💦","کانال عاشقانه دارین بفرستین بهم🥲❣","کی میره خودی مه بریم کلاس زبان؟😐🦋","🐈میو میو","سلامم خار دشت؟😏🐈"]

auto_forward_message = None

auto_send_message = None

is_init_need = True

# |========> Setup config.json <========|
ConfigAcc = db.getDb('config.json')

# Get account info from config.json
check = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})

# Keep default config
default_config = {
    'admin_list': [main_admin_id],
    'ignore_pvs': [main_admin_id],
    'saved_links': [],
    'secretary_text': "",
    'auto_chat': {'status': 1, 'time': 550},
    'auto_join': 1,
    'auto_clear': 1,
    'save_links': 1,
    'main_admin_id': main_admin_id
}

# Add account default config to config.json if it not exists
if not check:
    ConfigAcc.add(default_config)

# |========> Setup scheduler <========|
scheduler = AsyncIOScheduler()
scheduler.start()


# |========> New Message Handler <========|
@app.on_message(filters.command('usage'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("در حال بررسی...♻️", quote=True)

    txt = f"""
❈ Ram Status :
┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 

•|🎗️|•  RAM Size:﹝ {psutil.virtual_memory().total // (1024 ** 2):,d} MB﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
•|🎗️|•  RAM Available :﹝ {psutil.virtual_memory().available // (1024 ** 2):,d} MB﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
•|🎗️|•  RAM Used:﹝ {psutil.virtual_memory().used // (1024 ** 2):,d} MB﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
•|🎗️|•  RAM Usage:﹝ {psutil.virtual_memory().percent}%﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
•|🎗️|•  CPU Usage:﹝ {psutil.cpu_percent(4)}%﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
 
  𓏺 Bʏ ⌯ @m3dpy 𓏺
"""

    await message.reply(txt, quote=True)


@app.on_message(filters.command('bot'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("Online!", quote=True)


@app.on_message(filters.command('init'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    init(datas)

    await message.reply("❈ تنظیمات اولیه انجام شد.", quote=True)


def init(datas):
    if datas['auto_chat']['status']:
        this_job = scheduler.get_job(job_id="autochat")
        if this_job is not None:
            scheduler.remove_job(job_id="autochat")

        scheduler.add_job(auto_chat_job, "interval", seconds=datas['auto_chat']['time'], id="autochat")

    if datas['save_links']:
        this_job = scheduler.get_job(job_id="savelink")
        if this_job is not None:
            scheduler.remove_job(job_id="savelink")

        scheduler.add_job(join_saved_job, "interval", seconds=150, id="savelink")

    if datas['auto_clear']:
        this_job = scheduler.get_job(job_id="autoclear")
        if this_job is not None:
            scheduler.remove_job(job_id="autoclear")

        scheduler.add_job(auto_clear_job, "interval", seconds=900, id="autoclear")


@app.on_message(filters.command('ping'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    t1 = time()
    await app.get_me()
    t2 = time()
    await message.reply(f"❈ Ping : {round((t2 - t1) * 1000, 1)} ms", quote=True)


@app.on_message(filters.command('binfo'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    my_acc = await app.get_me()

    txt = f"""
❈ My Information ❈

❈ Profile Name:﹝ `{my_acc.first_name}` ﹞
❈ UserID:﹝  `{my_acc.id}` ﹞
❈ Phone Number:﹝ `+{my_acc.phone_number}` ﹞
❈ Folder Location:﹝ `{os.getcwd()}` ﹞
 ┈┅┅┅┈ 𖣔 ┈┅┅┅┈ 
 
 𓏺 Bʏ ⌯ @m3dpy
"""

    await message.reply(txt, quote=True)


@app.on_message(filters.command('help'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    txt = """
❈ راهنماے تبچے ❈

 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/init`
🎖️ راه اندازی اولیه تبچی
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/ping` ▫️ `/bot`
🎖️ دریافت وضعیت ربات
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/usage`
🎖️ نمایش مصرف منابع تبچی
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/binfo`
🎖️ دریافت اطلاعات اکانت
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/amar`
🎖️  دریافت آمار اکانت
 ┈┅┅┅┈ ✿ ┈┅┅┅┈
💠 `/clear` ▫️ پاکسازی
🎖️ خروج از گروه هایے که سکوت کردند و حذف کاربران مسدود از لیست
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/autoclear` ▫️⟮𝖮𝖭 𓏺 𝖮𝖥𝖥⟯
🎖️  پاکسازی اکانت در هر 15 دقیقه
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/dellinks`
🎖️  خالی کردن لینک های درصف انتظار برای عضویت
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/addadmin` ▫️⟮𝗂𝖣⟯
🎖️  افزودن ادمین جدید
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/adminlist`
🎖️  لیست ادمین ها
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/deladmin` ▫️⟮𝗂𝖣⟯
🎖️  حذف ادمین از لیست
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/addpv2contact`
🎖️ افزودن همه ے افرادے که در پیوے هستن به مخاطبین
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/clearcontacts`
🎖️ خالی کردن لیست مخاطبین
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/addpvs` ▫️⟮LINK⟯
🎖️  ادد کردن همه ے افرادے که در پیوے هستن به یڪ گروه
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/f2pv` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️ فروارد کردن پیام ریپلاے شده به همه کاربران
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/s2pvs` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️  ارسال کردن پیام ریپلاے شده به همه کاربران
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/f2sgps` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️  فروارد کردن پیام ریپلاے شده به همه سوپرگروه ها
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/s2sgps` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️  ارسال کردن پیام ریپلاے شده به تمامی سوپر گروه ها
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/setFtime` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️ فعالسازے فروارد خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/setStime` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️ فعالسازے ارسال خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delFtime`
🎖️  حذف فروارد خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delStime`
🎖️ حذف ارسال خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/SetId` ❗⟮𝖳𝖤𝖷𝖳⟯
🎖️  تنظیم نام کاربرے (آیدے)ربات
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/name` ❗⟮𝖳𝖤𝖷𝖳⟯
🎖️ تنظیم نام پروفایل ربات
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/lastname` ❗⟮𝖳𝖤𝖷𝖳⟯
🎖️  تنظیم فامیلی پروفایل ربات
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/setbio` ❗⟮𝖳𝖤𝖷𝖳⟯
🎖️  تنظیم بیو پروفایل ربات
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/setPhoto` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️  اپلود عکس پروفایل جدید با ریپلای روی عکس
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delPhoto`
🎖️ حذف آخرین عکس پروفایل اکانت
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/join` ▫️⟮𝖴𝗌𝖾𝗋𝖭𝖺𝗆𝖾⟯
🎖️  عضویت در یڪ آیدی
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delchs`
🎖️  خروج از همه ے کانال ها
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delgps` ❗⟮𝖭𝖴𝖬𝖡𝖱⟯ ▫️ all
🎖️ خروج از گروه ها به تعداد موردنظر یا همه
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/autochat` ▫️⟮𝖮𝖭 𓏺 𝖮𝖥𝖥⟯ ▫️ (زمان وقفه)
🎖️ فعال یا خاموش کردن چت خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/savelink` ▫️⟮𝖮𝖭 𓏺 𝖮𝖥𝖥⟯
🎖️ فعال یا خاموش کردن عضویت در لینک های ذخیره شده بعد از فلود
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/autojoin` ▫️⟮𝖮𝖭 𓏺 𝖮𝖥𝖥⟯
🎖️ فعال یا خاموش کردن عضویت خودکار در لینک های پیام های جدید کانال ها
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/slinks` ▫️⟮𝖴𝗌𝖾𝗋𝖭𝖺𝗆𝖾⟯
🎖️ دریافت، بررسی و ذخیره 500 لینک آخر یک لینکدونی
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/monshi` ▫️⟮𝖱𝖾𝗉𝗅𝖺𝗒⟯
🎖️  تنظیم بنر منشی خودکار (ارسال یک بنر بصورت خودکار به افرادی که جدیدا پیوی ربات پیام میدهند)
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/delMonshi`
🎖️  حذف و غیرفعالسازی منشی خودکار
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
💠 `/linkdooni`
🎖️ جوین در لینکدونی ها

 ┈┅┅┅┅┅┅┈
 ❈ **By : @m3dpy ▪️
  ┈┅┅┅┅┅┅┈
"""

    await message.reply(txt, quote=True)


@app.on_message(filters.command('amar'))
async def new_message_handler(client, message):
    global main_admin_id
    global auto_forward_message
    global auto_send_message
    global is_init_need

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("⌛️", quote=True)

    dialogs = await all_chat()

    contacts = await app.get_contacts()

    txt = f"""
    
    ❈ Tabchi Status :
    	
❈ All :   `{len(dialogs['group_id_list']) + len(dialogs['channel_id_list']) + len(dialogs['private_id_list'])}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Groups :   `{len(dialogs['group_id_list'])}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Channels :   `{len(dialogs['channel_id_list'])}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Private :   `{len(dialogs['private_id_list'])}`
┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Auto Chat :   `{f'on  -->  {datas["auto_chat"]["time"]}s' if datas['auto_chat']['status'] else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Auto Join :   `{'on' if datas['auto_join'] else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Auto Clear :   `{'on' if datas['auto_clear'] else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Join Saved Links :   `{'on' if datas['save_links'] else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Monshi :   `{'on' if (datas['secretary_text'] != "") else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Auto Forward :   `{'on' if (auto_forward_message is not None) else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Auto Send :   `{'on' if (auto_send_message is not None) else 'off'}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Number of admins :   `{len(datas['admin_list'])}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Number of contacts :   `{len(contacts)}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
❈ Number of saved links :   `{len(datas['saved_links'])}`
 ┈┅┅┅┈ ✿ ┈┅┅┅┈ 
 
 𓏺 Bʏ ⌯ @m3dpy 𓏺
"""


    if is_init_need:
        txt = "لطفا دستور `/init` را ارسال کنید!!!"
        is_init_need = False

    await message.reply(txt, quote=True)


@app.on_message(filters.command('addpv2contact'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ در حال اضافه کردن.", quote=True)

    all_chats = await all_chat()
    all_pvs_id = all_chats['private_id_list']

    contacts = await app.get_contacts()

    for contact in contacts:
        if contact.id in all_pvs_id:
            all_pvs_id.remove(contact.id)

    for pv_id in all_pvs_id:
        try:
            await app.add_contact(pv_id, "User")
            await asyncio.sleep(0.1)
        except:
            pass

    await message.reply("تمام افرادی که پیوی هستن به مخاطبین اضافه شدن ✅", quote=True)


@app.on_message(filters.command('clearcontacts'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ در حال حذف کردن.", quote=True)

    contacts = await app.get_contacts()

    contacts_id = []
    for contact in contacts:
        contacts_id.append(contact.id)

    await app.delete_contacts(contacts_id)

    await message.reply("تمام افرادی که پیوی هستن به مخاطبین حذف شدن ❌", quote=True)


@app.on_message(filters.command('addadmin'))
async def new_message_handler(client, message):
    global main_admin_id

    if message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return

    # Skip if given_account_id is invalid
    given_account_id = msg[1]
    try:
        given_account_id = int(given_account_id)
    except ValueError:
        return

    if given_account_id in datas['admin_list']:
        txt = "**❈ کاربر مورد نظر در حال حاضر ادمین است.**"
    else:
        datas['admin_list'].append(given_account_id)

        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'admin_list': datas['admin_list']})

        txt = "**❈ کاربر مورد نظر به لیست ادمین ها اضافه شد.**"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('deladmin'))
async def new_message_handler(client, message):
    global main_admin_id

    if message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return

    # Skip if given_account_id is invalid
    given_account_id = msg[1]
    try:
        given_account_id = int(given_account_id)
    except ValueError:
        return

    if given_account_id not in datas['admin_list']:
        txt = "**❈ کاربر مورد نظر در حال حاضر ادمین نیست.**"
    else:
        datas['admin_list'].remove(given_account_id)

        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'admin_list': datas['admin_list']})

        txt = "**❈ کاربر مورد نظر از لیست ادمین ها حذف شد.**"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('adminlist'))
async def new_message_handler(client, message):
    global main_admin_id

    if message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    txt = "**ادمین اصلی :**"
    for admin in datas['admin_list']:
        txt += f"`❈ : {admin}`\n"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('addpvs'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return
    msg = msg[1]

    await message.reply("❈ در حال ادد زدن.", quote=True)

    try:
        await app.join_chat(msg)
    except:
        pass

    try:
        gap = await app.get_chat(msg)
    except:
        await message.reply("Can't find gap!", quote=True)
        return

    all_chats = await all_chat()
    all_pvs_id = all_chats['private_id_list']

    counter = 0
    for pv_id in all_pvs_id:
        try:
            await app.add_chat_members(chat_id=gap.id, user_ids=pv_id)
            counter += 1
            await asyncio.sleep(5)
        except:
            pass

    await message.reply(f"{counter} members added!", quote=True)


@app.on_message(filters.command('f2sgps'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    message = message.reply_to_message

    await message.reply("❈ در حال فروارد .", quote=True)

    all_chats = await all_chat()
    all_groups_id = all_chats['group_id_list']

    for group_id in all_groups_id:
        try:
            await message.forward(group_id)
            await asyncio.sleep(5)
        except:
            pass

    await message.reply("❈ با موفقیت پیام ریپلی شده به تمام گپها فروارد شد.", quote=True)


@app.on_message(filters.command('f2pv'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    message = message.reply_to_message

    await message.reply("❈ در حال فروارد .", quote=True)

    all_chats = await all_chat()
    all_pvs_id = all_chats['private_id_list']

    for pv_id in all_pvs_id:
        try:
            await message.forward(pv_id)
            await asyncio.sleep(5)
        except:
            pass

    await message.reply("❈ با موفقیت پیام ریپلی شده به تمام پیوی ها فروارد شد.", quote=True)


@app.on_message(filters.command('setFtime'))
async def new_message_handler(client, message):
    global main_admin_id
    global auto_forward_message

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    replied_message = message.reply_to_message

    this_job = scheduler.get_job(job_id="setFtime")

    if this_job is not None:
        scheduler.remove_job(job_id="setFtime")

    auto_forward_message = replied_message
    scheduler.add_job(setFtime_job, "interval", seconds=900, id="setFtime")

    txt = "پیام ریپلای شده هر 15 دقیقه در همه گپ ها فوروارد خواهد شد!"
    await message.reply(txt, quote=True)


@app.on_message(filters.command('delFtime'))
async def new_message_handler(client, message):
    global main_admin_id
    global auto_forward_message

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    this_job = scheduler.get_job(job_id="setFtime")

    if this_job is not None:
        auto_forward_message = None
        scheduler.remove_job(job_id="setFtime")
        txt = "فوروارد خودکار با موفقیت خاموش شد!"
    else:
        txt = "فوروارد خودکار خاموش بوده است!"

    await message.reply(txt, quote=True)


async def setFtime_job():
    global auto_forward_message

    if auto_forward_message is None:
        return

    all_chats = await all_chat()
    all_id = all_chats['group_id_list']

    for given_id in all_id:
        try:
            await auto_forward_message.forward(given_id)
            await asyncio.sleep(5)
        except:
            pass


@app.on_message(filters.command('s2sgps'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    text = message.reply_to_message.text

    await message.reply("❈ در حال ارسال .", quote=True)

    all_chats = await all_chat()
    all_groups_id = all_chats['group_id_list']

    for group_id in all_groups_id:
        try:
            await app.send_message(group_id, text)
            await asyncio.sleep(5)
        except:
            pass

    await message.reply("❈ با موفقیت پیام ریپلی شده به تمام گپها ارسال شد.", quote=True)


@app.on_message(filters.command('s2pvs'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    text = message.reply_to_message.text

    await message.reply("❈ در حال ارسال .", quote=True)

    all_chats = await all_chat()
    all_pvs_id = all_chats['private_id_list']

    for pv_id in all_pvs_id:
        try:
            await app.send_message(pv_id, text)
            await asyncio.sleep(5)
        except:
            pass

    await message.reply("❈ با موفقیت پیام ریپلی شده به تمام پیوی ها ارسال شد.", quote=True)


@app.on_message(filters.command('setStime'))
async def new_message_handler(client, message):
    global main_admin_id
    global auto_send_message

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    replied_message_text = message.reply_to_message.text

    this_job = scheduler.get_job(job_id="setStime")

    if this_job is not None:
        scheduler.remove_job(job_id="setStime")

    auto_send_message = replied_message_text
    scheduler.add_job(setStime_job, "interval", seconds=900, id="setStime")

    txt = "پیام ریپلای شده هر 15 دقیقه در همه گپ ها ارسال خواهد شد!"
    await message.reply(txt, quote=True)


@app.on_message(filters.command('delStime'))
async def new_message_handler(client, message):
    global main_admin_id
    global auto_send_message

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    this_job = scheduler.get_job(job_id="setStime")

    if this_job is not None:
        auto_send_message = None
        scheduler.remove_job(job_id="setStime")
        txt = "ارسال خودکار با موفقیت خاموش شد!"
    else:
        txt = "ارسال خودکار خاموش بوده است!"

    await message.reply(txt, quote=True)


async def setStime_job():
    global auto_send_message

    if auto_send_message is None:
        return

    all_chats = await all_chat()
    all_id = all_chats['group_id_list']

    for given_id in all_id:
        try:
            await app.send_message(chat_id=given_id, text=auto_send_message)
            await asyncio.sleep(5)
        except:
            pass


@app.on_message(filters.command('name'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.replace("/name ", "")

    try:
        await app.update_profile(first_name=msg)

        await message.reply("❈ اسم با موفقیت تغیر کرد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('lastname'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.replace("/lastname ", "")

    try:
        await app.update_profile(last_name=msg)

        await message.reply("❈ فامیلی با موفقیت تغیر کرد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('setbio'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.replace("/setbio ", "")

    try:
        await app.update_profile(bio=msg)

        await message.reply("❈ بیو با موفقیت تغیر کرد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('SetId'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return
    msg = msg[1]

    try:
        await app.set_username(msg)

        await message.reply("❈ آیدی با موفقیت تغیر کرد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('setPhoto'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    photo = message.reply_to_message

    if photo.photo is None:
        return

    try:
        await message.reply("❈ کمی صبر کنید ..", quote=True)
        photo = await app.download_media(photo, in_memory=True)
        await app.set_profile_photo(photo=photo)
        await message.reply("❈ پروفایل با موفقیت اضافه شد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('delPhoto'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    try:
        await message.reply("❈ کمی صبر کنید ..", quote=True)

        # Get the photos to be deleted
        photo = None
        async for photo in app.get_chat_photos("me"):
            photo = photo.file_id
            break

        if photo is None:
            await message.reply("Empty!", quote=True)
            return

        # Delete one photo
        await app.delete_profile_photos(photo)

        await message.reply("❈ پروفایل با موفقیت حذف شد.", quote=True)

    except:
        await message.reply("Not changed!", quote=True)


@app.on_message(filters.command('join'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return

    msg = msg[1]

    try:
        await app.join_chat(msg)
        await message.reply("Joined!", quote=True)

    except errors.FloodWait:
        await message.reply("اکانت در حال حاضر محدود شده است!", quote=True)

    except:
        await message.reply("Can't join!", quote=True)


@app.on_message(filters.command('delchs'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ کمی صبر کنید ..", quote=True)

    all_chats = await all_chat()
    all_channel_id = all_chats['channel_id_list']

    for channel_id in all_channel_id:
        try:
            await app.leave_chat(channel_id, delete=True)
        except:
            pass

    await message.reply("با موفقیت از تمام چنل ها لفت دادم.", quote=True)


@app.on_message(filters.command('delgps'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return

    count = msg[1]
    if count != "all":
        try:
            count = int(count)
        except ValueError:
            return

    await message.reply("❈ کمی صبر کنید ..", quote=True)

    all_chats = await all_chat()
    all_group_id = all_chats['group_id_list']

    left_counter = 0
    for group_id in all_group_id:
        if count != "all":
            if left_counter >= count:
                break

        try:
            await app.leave_chat(group_id, delete=True)
            left_counter += 1
        except:
            pass

    await message.reply("❈ با موفقیت از گپ ها لفت دادم.", quote=True)


@app.on_message(filters.command('clear'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ درحال پاکسازی اکانت ..", quote=True)

    await clear_action(datas)

    await message.reply("❈ با موفیقت اکانت پاکسازی شد.", quote=True)


async def clear_action(datas):
    all_chats = await all_chat()
    all_pvs_id = all_chats['private_id_list']
    all_group_id = all_chats['group_id_list']

    my_acc = await app.get_me()
    if my_acc.id not in datas['ignore_pvs']:
        datas['ignore_pvs'].append(my_acc.id)

    for pv_id in all_pvs_id:
        user = await app.get_users(pv_id)
        if user.status is UserStatus.LONG_AGO:
            if pv_id not in datas['ignore_pvs']:
                datas['ignore_pvs'].append(pv_id)

    for admin_id in datas['admin_list']:
        if admin_id not in datas['ignore_pvs']:
            datas['ignore_pvs'].append(admin_id)

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'ignore_pvs': datas['ignore_pvs']})

    for group_id in all_group_id:
        sended_msg = None
        try:
            sended_msg = await app.send_message(group_id, "علی بیا اینجا")
            await asyncio.sleep(2)
            sended_msg = await app.get_messages(group_id, sended_msg.id)
            await sended_msg.delete()
        except:
            pass

        if sended_msg is None or sended_msg.empty:
            chat = await app.get_chat(group_id)
            await chat.leave()


@app.on_message(filters.command('autoclear'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":

        this_job = scheduler.get_job(job_id="autoclear")

        if this_job is None:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_clear': 1})
            scheduler.add_job(auto_clear_job, "interval", seconds=900, id="autoclear")
            txt = "حالت پاکسازی خودکار اکانت در هر 15 دقیقه روشن شد!"
        else:
            txt = "حالت پاکسازی خودکار اکانت در هر 15 دقیقه روشن بوده است!"

    elif msg == "off":

        this_job = scheduler.get_job(job_id="autoclear")

        if this_job is None:
            txt = "حالت پاکسازی خودکار اکانت در هر 15 دقیقه خاموش بوده است!"
        else:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_clear': 0})
            scheduler.remove_job(job_id="autoclear")
            txt = "حالت پاکسازی خودکار اکانت در هر 15 دقیقه خاموش شد!"

    else:
        return

    await message.reply(txt, quote=True)


async def auto_clear_job():
    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    await clear_action(datas)


@app.on_message(filters.command('dellinks'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    datas['saved_links'].clear()
    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'saved_links': datas['saved_links']})

    await message.reply("❈ با موفیقت لینک های ذخیره شده خالی شد.", quote=True)


@app.on_message(filters.command('monshi'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list'] or message.reply_to_message is None:
        return

    datas['secretary_text'] = message.reply_to_message.text

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'secretary_text': datas['secretary_text']})

    await message.reply("❈ منشی خودکار باموفقیت تنظیم شد.", quote=True)


@app.on_message(filters.command('delMonshi'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    datas['secretary_text'] = ""

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'secretary_text': datas['secretary_text']})

    await message.reply("❈ منشی با موفقیت حذف شد .", quote=True)


@app.on_message(filters.command('autochat'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    if len(msg) == 3 and msg[1] == "on":
        time = msg[2]

        # Skip if time is invalid
        try:
            time = int(time)
        except ValueError:
            return

        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_chat': {'status': 1, 'time': time}})

        # Add to scheduler
        this_job = scheduler.get_job(job_id="autochat")
        if this_job is not None:
            scheduler.remove_job(job_id="autochat")

        scheduler.add_job(auto_chat_job, "interval", seconds=time, id="autochat")

        txt = f"حالت چت خودکار در هر {time} ثانیه روشن شد!"

    elif len(msg) == 2 and msg[1] == "off":

        this_job = scheduler.get_job(job_id="autochat")

        if this_job is None:
            txt = "حالت چت خودکار خاموش بوده است!"
        else:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_chat': {'status': 0, 'time': 0}})
            scheduler.remove_job(job_id="autochat")
            txt = "حالت چت خودکار خاموش شد!"

    else:
        return

    await message.reply(txt, quote=True)


async def auto_chat_job():
    global auto_chat_texts

    all_chats = await all_chat()
    all_groups_id = all_chats['group_id_list']

    txt = random.choice(auto_chat_texts)

    for group_id in all_groups_id:
        try:
            await app.send_message(group_id, txt)
        except:
            pass


@app.on_message(filters.command('autojoin'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":
        if datas['auto_join']:
            txt = "حالت جوین خودکار روشن بوده است!"
        else:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_join': 1})
            txt = "حالت جوین خودکار روشن شد!"

    elif msg == "off":
        if datas['auto_join']:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'auto_join': 0})
            txt = "حالت جوین خودکار خاموش شد!"
        else:
            txt = "حالت جوین خودکار خاموش بوده است!"

    else:
        return

    await message.reply(txt, quote=True)


@app.on_message(filters.command('savelink'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":

        this_job = scheduler.get_job(job_id="savelink")

        if this_job is None:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'save_links': 1})
            scheduler.add_job(join_saved_job, "interval", seconds=150, id="savelink")
            txt = "حالت ذخیره لینک و عضویت در آن بعد از فلود روشن شد!"
        else:
            txt = "حالت ذخیره لینک و عضویت در آن بعد از فلود روشن بوده است!"

    elif msg == "off":

        this_job = scheduler.get_job(job_id="savelink")

        if this_job is None:
            txt = "حالت ذخیره لینک و عضویت در آن بعد از فلود خاموش بوده است!"
        else:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'save_links': 0})
            scheduler.remove_job(job_id="savelink")
            txt = "حالت ذخیره لینک و عضویت در آن بعد از فلود خاموش شد!"

    else:
        return

    await message.reply(txt, quote=True)


async def join_saved_job():
    # Get account info from config
    saved_links = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]['saved_links']

    if len(saved_links) == 0:
        return

    link = saved_links.pop()

    try:
        await app.join_chat(link)

    except errors.FloodWait:
        saved_links.append(link)

    except:
        pass

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'saved_links': saved_links})


@app.on_message(filters.command('slinks'))
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ در حال بررسی لینکدونی.", quote=True)

    # Keep new message text in 'msg'
    msg = message.text

    msg = msg.split()

    # Skip if input is invalid
    if len(msg) != 2:
        return
    msg = msg[1]

    try:
        await app.join_chat(msg)
    except:
        pass

    channel = await app.get_chat(msg)

    async for post in app.get_chat_history(chat_id=channel.id, limit=200):
        post_text = post.text or post.caption

        try:
            links = re.findall(pattern="(https://t\.me/\S+)", string=post_text)
        except:
            continue

        for link in links:
            if link not in datas['saved_links']:
                datas['saved_links'].append(link)

    datas['saved_links'].reverse()

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'saved_links': datas['saved_links']})

    await message.reply("❈ با موفقیت 500 لینک اخر لینکدونی رو ذخیره کردم.", quote=True)


@app.on_message(filters.command('linkdooni'))
async def new_message_handler(client, message):
    global main_admin_id
    global linkdoni_list

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        return

    await message.reply("❈ لطفا کمی صبر کنید ..", quote=True)

    for link in linkdoni_list:
        try:
            await app.join_chat(link)

        except errors.FloodWait:
            if datas['save_links']:
                if link not in datas['saved_links']:
                    datas['saved_links'].append(link)

        except:
            pass

        await asyncio.sleep(5)

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'saved_links': datas['saved_links']})

    await message.reply("❈ با موفقیت داخل لینکدونی ها عضو شدم.", quote=True)


# Secretary Action
@app.on_message(filters.private)
async def new_message_handler(client, message):
    global main_admin_id

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if datas['secretary_text'] == "" or message.from_user is None or message.from_user.id in datas['admin_list']:
        return

    messages_count = 0
    async for _ in app.get_chat_history(message.chat.id):
        messages_count += 1

    if messages_count > 1:
        return

    await asyncio.sleep(100)

    await message.reply(datas['secretary_text'], quote=True)


# Join Action
@app.on_message(filters.channel)
async def new_message_handler(client, message):
    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if not datas['auto_join']:
        return

    msg = message.text or message.caption

    try:
        links = re.findall(pattern="(https://t\.me/\S+)", string=msg)
    except:
        return

    for link in links:
        try:
            await app.join_chat(link)

        except errors.FloodWait:
            if datas['save_links']:
                if link not in datas['saved_links']:
                    datas['saved_links'].append(link)

        except:
            pass

        await asyncio.sleep(5)

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'saved_links': datas['saved_links']})


async def all_chat():
    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    private_id_list = []
    group_id_list = []
    channel_id_list = []

    async for dialog in app.get_dialogs():

        if dialog.chat.type is ChatType.PRIVATE:
            private_id_list.append(dialog.chat.id)

        elif dialog.chat.type is ChatType.SUPERGROUP:
            group_id_list.append(dialog.chat.id)

        elif dialog.chat.type is ChatType.CHANNEL:
            channel_id_list.append(dialog.chat.id)

    for ignore_pv in datas['ignore_pvs']:
        if ignore_pv in private_id_list:
            private_id_list.remove(ignore_pv)

    return {'private_id_list': private_id_list, 'group_id_list': group_id_list, 'channel_id_list': channel_id_list}


# |========> Run app <========|
app.run()
