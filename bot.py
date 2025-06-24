from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import json
import nest_asyncio
import re

# Path to your scores file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")
TEAMS = ["Team Shraddha", "Team Nishtha", "Team Bhakti", "Team Seva", "Team Agna", "Team Rajipo"]

def load_scores():
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def reset_scores():
    return {team: 0 for team in TEAMS}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Scoreboard Bot. Use /score to adjust team points.")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(team, callback_data=team)] for team in TEAMS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Select a team:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("Select a team:", reply_markup=reply_markup)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scores = reset_scores()
    save_scores(scores)
    await update.message.reply_text("✅ Scores have been reset to 0.")
    await score(update, context)

def team_controls(team):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add 5", callback_data=f"{team}+5"),
         InlineKeyboardButton("➖ Subtract 5", callback_data=f"{team}-5")],
        [InlineKeyboardButton("➕ Add 10", callback_data=f"{team}+10"),
         InlineKeyboardButton("➖ Subtract 10", callback_data=f"{team}-10")],
        [InlineKeyboardButton("↩️ Go back to teams", callback_data="BACK")]
    ])

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "BACK":
        await score(update, context)
        return

    if data in TEAMS:
        await query.edit_message_text(
            text=f"{data} selected:",
            reply_markup=team_controls(data)
        )
    elif "+" in data or "-" in data:
        match = re.match(r"(.+?)([+-]\d+)", data)
        if match:
            team, change = match.groups()
            change = int(change)
            scores = load_scores()
            scores[team] = max(0, scores.get(team, 0) + change)
            save_scores(scores)
            await query.edit_message_text(
                text=f"{team} score updated: {scores[team]}",
                reply_markup=team_controls(team)
            )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unknown command.")

# Run the bot
async def main():
    app = ApplicationBuilder().token("8073398946:AAHyl4Rg9As5hcn914zJhXsDtrxQZ4AHN2E").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
