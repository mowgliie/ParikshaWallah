import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# JSON file load karo
with open('data.json', 'r') as f:
    data = json.load(f)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exams = list(data['exams'].keys())
    keyboard = [[InlineKeyboardButton(exam, callback_data=f"exam_{exam}")] for exam in exams]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select an exam:", reply_markup=reply_markup)

# Button clicks handle karo
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data_str = query.data

    if data_str.startswith("exam_"):
        exam = data_str.replace("exam_", "")
        subjects = list(data['exams'][exam]['subjects'].keys())
        keyboard = [[InlineKeyboardButton(subject, callback_data=f"subject_{exam}_{subject}")] for subject in subjects]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select a subject for {exam}:", reply_markup=reply_markup)

    elif data_str.startswith("subject_"):
        _, exam, subject = data_str.split("_")
        years = list(data['exams'][exam]['subjects'][subject].keys())
        keyboard = [[InlineKeyboardButton(year, callback_data=f"year_{exam}_{subject}_{year}")] for year in years]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select a year for {subject}:", reply_markup=reply_markup)

    elif data_str.startswith("year_"):
        _, exam, subject, year = data_str.split("_")
        pdf_link = data['exams'][exam]['subjects'][subject][year]
        await query.message.reply_text(f"Download {exam} {subject} {year} PDF: {pdf_link}")

def main():
    # Apna API token yahan daalein
    app = Application.builder().token('7927544746:AAF2BKkhzDMEgugh6A6a8XXxSOrXBvp_yfU').build()

    # Handlers add karo
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # Bot start karo
    app.run_polling()

if __name__ == '__main__':
    main()