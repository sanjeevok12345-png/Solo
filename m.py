import logging
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, mute

TOKEN = "7256838089:AAHZRHb-z7qK_FtYwAjsyyKaI7maZ99BgtU"
GROUP_ID = -1002624988004
CHANNEL_ID = -1002412045756

logging.basicConfig(level=logging.INFO)

async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def handle_message(update, context):
    if update.effective_chat.id != GROUP_ID:
        return
    
    user = update.effective_user
    message = update.effective_message
    
    if str(user.id).startswith('-'):
        return
    
    is_member = await check_membership(user.id, context)
    
    if not is_member:
        try:
            await message.delete()
            
            user_name = user.first_name or "User"
            user_id = user.id
            username = f"@{user.username}" if user.username else "No username"
            
            warning_text = f"""JOIN https://t.me/Quantumadz to message here

Hello {user_name}
User ID: {user_id}
Username: {username}"""

            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=warning_text
            )
            
        except Exception as e:
            print(f"Error: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(MessageHandler(
        filters.Chat(GROUP_ID) & filters.TEXT & ~filters.COMMAND,
        handle_message
    ))
    
    print("Bot is running...")
    application.run_polling()

if name == 'main':
    main()