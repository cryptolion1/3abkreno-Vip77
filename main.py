import json
import os
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ملف الاشتراكات
if not os.path.exists("subs.json"):
    with open("subs.json", "w") as f:
        json.dump({}, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 الاشتراك", callback_data="subscribe_menu")],
        [InlineKeyboardButton("💎 مميزات القناة الخاصة", callback_data="features")],
        [InlineKeyboardButton("💼 تحويل وكالة", callback_data="agency")],
    ]
    await update.message.reply_text("أهلاً بك 👋\nاختر من القائمة:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    msg = (
        "💎 مميزات القناة الخاصة:\n\n"
        "🔹 نقدم من 3 إلى 6 صفقات يوميًا – صفقات مدروسة بعناية فائقة\n"
        "🔹 أكثر من 70% من الصفقات دون أي انعكاس\n"
        "🔹 فريق عمل متخصص يعمل باستمرار لاختيار أفضل الفرص في السوق\n"
        "🔹 قناة مناقشات مباشرة لمتابعة الصفقات أولًا بأول\n"
        "🔹 خدمة عملاء جاهزة للرد على استفساراتكم طوال الأسبوع\n"
        "🔹 متوسط الربح اليومي يتراوح بين 200 إلى 400 نقطة بفضل الله\n"
        "🔹 الاستوب مشابه لما نقدمه في القناة العامة – من 50 إلى 80 نقطة كحد أقصى"
    )
    keyboard = [[InlineKeyboardButton("🔙 عودة", callback_data="back")]]
    await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("1 شهر", callback_data="sub_1")],
        [InlineKeyboardButton("2 شهر", callback_data="sub_2")],
        [InlineKeyboardButton("3 شهر", callback_data="sub_3")],
        [InlineKeyboardButton("🔙 عودة", callback_data="back")]
    ]
    await query.edit_message_text("🔢 اختر مدة الاشتراك:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("sub_"):
        duration = int(query.data.split("_")[1])
        prices = {1: 70, 2: 140, 3: 210}
        offers = {1: 70, 2: 100, 3: 150}
        msg = (
            f"💳 السعر الحالي ({duration} شهر): {offers[duration]}$\n"
            f"💰 السعر قبل الخصم : {prices[duration]}$\n\n"
            "📩 أرسل المبلغ إلى المحفظة التالية: \n"
            "<code>TRC20: TJ8p56jcUSGwJANdykP5a1KBT5QXVR9QAa</code>\n"
            "ثم أرسل إثبات الدفع (صورة) هنا."
        )
        context.user_data['duration'] = duration
        keyboard = [[InlineKeyboardButton("🔙 عودة", callback_data="back")]]
        await query.edit_message_text(msg, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

async def confirm_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")
    user_id = int(data[1])
    duration = int(data[2])
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=30 * duration)

    with open("subs.json", "r") as f:
        subs = json.load(f)
    subs[str(user_id)] = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat(),
        "duration": duration
    }
    with open("subs.json", "w") as f:
        json.dump(subs, f)

    message_text = (
        f"مبروك ✔️\n"
        f"أصبحت مشتركًا لمدة {duration} شهر\n"
        f"المدة: من {start_date.date()} إلى {end_date.date()}\n\n"
        f"📥 للتواصل: @abkreno_Forex"
    )

    try:
        with open("IMG_20250704_152709_763.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=user_id, photo=photo, caption=message_text)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=user_id, text=message_text)

    await context.bot.send_message(chat_id=ADMIN_ID, text=f"✅ تم تأكيد اشتراك المستخدم {user_id} لمدة {duration} شهر.")
    await query.edit_message_text("✅ تم التأكيد.")

async def handle_agency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    msg = (
        "💼 للانضمام مجانًا:\n"
        "حوّل تحت وكالتنا في Exness بأقل إيداع 300$\n"
        "🔗 رابط: https://one.exness-track.com/a/w0wcqjn0u4\n"
        "🔢 رقم وكالة: 1042718889596697948"
    )
    keyboard = [[InlineKeyboardButton("🔙 عودة", callback_data="back")]]
    await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def confirm_agency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = int(query.data.split("_")[1])
    start_date = datetime.datetime.now()

    with open("subs.json", "r") as f:
        subs = json.load(f)
    subs[str(user_id)] = {
        "start": start_date.isoformat(),
        "end": "permanent",
        "duration": "agency"
    }
    with open("subs.json", "w") as f:
        json.dump(subs, f)

    message_text = (
        f"✅ تم تسجيلك كعضو دائم (وكالة) من {start_date.date()}.\n"
        f"للتواصل: @abkreno_Forex"
    )

    try:
        with open("IMG_20250704_152709_763.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=user_id, photo=photo, caption=message_text)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=user_id, text=message_text)

    await context.bot.send_message(chat_id=ADMIN_ID, text=f"✅ تم تأكيد تحويل الوكالة للمستخدم {user_id}.")
    await query.edit_message_text("✅ تم التأكيد.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text or ""
    caption = f"💼 إثبات من {user.full_name} (ID: {user.id})\n\n{text}"
    keyboard = [[InlineKeyboardButton("✅ تأكيد تحويل الوكالة", callback_data=f"agencyconfirm_{user.id}")]]
    if update.message.photo:
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=caption, reply_markup=InlineKeyboardMarkup(keyboard))

    await update.message.reply_text("📨 تم الإرسال. ننتظر تأكيد الإدارة.")

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📥 الاشتراك", callback_data="subscribe_menu")],
        [InlineKeyboardButton("💎 مميزات القناة الخاصة", callback_data="features")],
        [InlineKeyboardButton("💼 تحويل وكالة", callback_data="agency")],
    ]
    await query.edit_message_text("🔙 تم الرجوع للقائمة:", reply_markup=InlineKeyboardMarkup(keyboard))

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_features, pattern="^features$"))
    app.add_handler(CallbackQueryHandler(show_subscription_menu, pattern="^subscribe_menu$"))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(confirm_subscription, pattern="^confirm_"))
    app.add_handler(CallbackQueryHandler(handle_agency, pattern="^agency$"))
    app.add_handler(CallbackQueryHandler(confirm_agency, pattern="^agencyconfirm_"))
    app.add_handler(CallbackQueryHandler(go_back, pattern="^back$"))
    app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), handle_message))

    print("✅ البوت شغال...")
    await app.run_polling()

import asyncio
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
