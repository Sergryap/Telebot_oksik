import telebot.async_telebot as tb_async
from password import token
import asyncio
from TgMethods.TgAgent import TgAgent

bot = tb_async.AsyncTeleBot(f'{token}')


async def get_context(message):
	return {
		'from_user': {
			'username': message.chat.username,
			'first_name': message.chat.first_name
		},
		'text': message.text.lower().replace('''"''', '').replace("""'""", ''),
		'chat_id': message.chat.id
	}


@bot.message_handler(commands=['start'])
async def send_welcome(message):
	user = message.chat.username
	context = await get_context(message)
	exec(f"user_{user} = TgAgent(context={context})")
	await eval(f"user_{user}.handler_msg()")


@bot.message_handler(func=lambda m: True)
async def echo_all(message):
	user = message.chat.username
	chat_id = message.chat.id
	context = await get_context(message)
	exec(f"user_{user} = TgAgent(context={context})")
	await eval(f"user_{user}.handler_msg()")


if __name__ == '__main__':
	asyncio.run(bot.polling())
