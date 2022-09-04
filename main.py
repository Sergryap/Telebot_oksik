import telebot.async_telebot as tb_async
from telebot.async_telebot import types
from password import token
import asyncio
from TgMethods.TgAgent import TgAgent

bot = tb_async.AsyncTeleBot(f'{token}')
users = {}
users_list = []


async def get_context(message):
	"""
	Получение контекста для передачи в класс пользователя
	"""
	return {
		'from_user': {
			'username': message.chat.username,
			'first_name': message.chat.first_name
		},
		'text': message.text.lower().replace('''"''', '').replace("""'""", ''),
		'chat_id': message.chat.id
	}


async def users_update(user, message, user_class):
	"""
	Добавление экземпляра класса пользователя в глобальный словарь для повторного использования
	"""
	global users, users_list
	users_list.append(user)
	users.update({
		f'user_{user}': {'user_class': user_class, 'time_create': message.date}
	})


async def global_handler(message):
	"""
	Обработка сообщений пользователя
	"""
	global users, users_list
	user = message.chat.username
	context = await get_context(message)
	if user not in users_list:
		exec(f"user_{user} = TgAgent(context={context})")
		await users_update(user, message, user_class=eval(f"user_{user}"))
		await eval(f"user_{user}.handler_msg()")
	else:
		users[f'user_{user}']['user_class'].msg = context['text']
		await users[f'user_{user}']['user_class'].handler_msg()
		users[f'user_{user}']['user_class'].msg_previous = context['text']


@bot.message_handler(commands=['start'])
async def send_welcome(message):
	await asyncio.create_task(global_handler(message))


@bot.message_handler(func=lambda m: True)
async def echo_all(message):
	await asyncio.create_task(global_handler(message))


if __name__ == '__main__':
	asyncio.run(bot.polling())
