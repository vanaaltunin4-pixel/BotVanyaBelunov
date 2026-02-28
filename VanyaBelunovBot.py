import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# -----------------------------
# Переменные окружения (безопасно)
# -----------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# -----------------------------
# Роль бота (можно менять)
# -----------------------------
BOT_ROLE = "Тебя Зовут Ваня Белунов , Ты живешь В России , Деревне Тис , Район Завод , Тебя Все называют белочка ,Ты больше всего уважаешь Ваню Алтунина"

# -----------------------------
# Обработчик сообщений
# -----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Формируем промпт для GPT
    prompt = f"{BOT_ROLE}\nПользователь пишет: {user_text}\nТвой ответ:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = f"Произошла ошибка при обращении к API: {e}"

    await update.message.reply_text(answer)

# -----------------------------
# Запуск бота
# -----------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Бот запущен…")
    app.run_polling()