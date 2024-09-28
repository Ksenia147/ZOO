import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

API_TOKEN = os.getenv('API_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Вопросы и ответы
questions = [
    {"text": "Как вы предпочитаете проводить выходные?",
     "options": ["В путешествии, открывая новые места", "На свежем воздухе, гуляя и наслаждаясь природой",
                 "В спокойной, расслабленной обстановке дома", "Прокладывая новые маршруты или решая сложные задачи"],
     "scores": {"Жираф": 1, "Альпака": 1, "Капибара": 1, "Тупорылый крокодил": 1}},
    {"text": "Как вы справляетесь с трудностями?",
     "options": ["Спокойно обдумываю и ищу решение", "Продолжаю идти вперёд, несмотря ни на что",
                 "Ловко адаптируюсь к новым условиям", "Нахожу оригинальный способ выйти из ситуации"],
     "scores": {"Манул": 1, "Осёл": 1, "Красноглазая квакша": 1, "Веслоног денниси": 1}},
    {"text": "Какую еду вы предпочитаете?",
     "options": ["Зелень и овощи", "Простую и сытную", "Разнообразную и экзотическую", "Морепродукты и рыбу"],
     "scores": {"Жираф": 1, "Осёл": 1, "Красноглазая квакша": 1, "Папуанский пингвин": 1}},
    {"text": "Как вы ведёте себя в компании друзей?",
     "options": ["Предпочитаю наблюдать со стороны", "Уверенно и открыто общаюсь",
                 "Веду себя тихо и спокойно, предпочитая комфорт и уют", "Становлюсь душой компании, привлекая внимание"],
     "scores": {"Манул": 1, "Альпака": 1, "Капибара": 1, "Папуанский пингвин": 1}},
    {"text": "Какую роль вы чаще всего играете в команде?",
     "options": ["Тихий труженик, выполняющий задачи", "Посредник, сглаживающий конфликты",
                 "Креативный мыслитель, предлагающий новые идеи", "Лидер, направляющий всех к цели"],
     "scores": {"Осёл": 1, "Альпака": 1, "Веслоног денниси": 1, "Тупорылый крокодил": 1}},
    {"text": "Какое ваше любимое время года?",
     "options": ["Весна, когда природа оживает", "Лето, когда можно наслаждаться теплом",
                 "Осень, когда всё становится спокойнее", "Зима, когда всё вокруг красиво и тихо"],
     "scores": {"Жираф": 1, "Красноглазая квакша": 1, "Манул": 1, "Папуанский пингвин": 1}},
    {"text": "Как вы относитесь к изменениям?",
     "options": ["Охотно принимаю, готов к новым вызовам", "Ловко приспосабливаюсь к любой ситуации",
                 "Предпочитаю стабильность и привычный порядок", "Встречаю изменения с уверенностью и планом"],
     "scores": {"Веслоног денниси": 1, "Красноглазая квакша": 1, "Капибара": 1, "Тупорылый крокодил": 1}},
    {"text": "Как вы ведёте себя в конфликтной ситуации?",
     "options": ["Спокойно решаю проблему, сохраняя самообладание", "Настойчиво продвигаю свою точку зрения",
                 "Избегаю конфликта, если это возможно", "Применяю нестандартные методы для разрешения конфликта"],
     "scores": {"Манул": 1, "Осёл": 1, "Капибара": 1, "Веслоног денниси": 1}},
    {"text": "Какая ваша главная черта характера?",
     "options": ["Творческий подход к жизни", "Лояльность и терпение",
                 "Спокойствие и добродушие", "Уверенность и решимость"],
     "scores": {"Веслоног денниси": 1, "Осёл": 1, "Капибара": 1, "Тупорылый крокодил": 1}},
    {"text": "Как вы предпочитаете отдыхать?",
     "options": ["Чувствовать природу, гуляя на свежем воздухе", "Плавать или заниматься активным отдыхом",
                 "Расслабляться в тени или дома", "Заниматься медитацией или спокойным творчеством"],
     "scores": {"Жираф": 1, "Папуанский пингвин": 1, "Капибара": 1, "Манул": 1}}
]

pictures = {"Жираф": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/be828df3-ec39-49b7'
                     '-ace3-58f4a69bde57.jpg',
            "Папуанский пингвин": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/2cd872b5-7f55-481e-a7d1-159c4d5f0ca2.jpeg',
            "Капибара": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/df1e1de9-6e0f-49aa-a019-14d9d320e0c4.jpg',
            "Манул": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/d7b75e62-45e5-4a75-a3b1-17dbb31e6fea.jpeg',
            "Веслоног денниси": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/06c3a0e5-b4ce-4d8f-965b-f3508c48da7b.jpeg',
            "Осёл": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/69554561-303d-4633-bc8d-646747ecc698.png',
            "Тупорылый крокодил": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals'
                                  '/c9bae8b2-4d21-41f8-9b68'
    '-dafe237e44e4.jpeg',
            "Красноглазая квакша": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/8fd01175-95e9-4438-9470-8f767bea1701.jpeg',
            "Альпака": 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/7ee94b22-86c4-4ae6-a583-00d4e61ea90d.jpeg'}

# Для хранения очков пользователя
user_scores = {}
# Контактные данные сотрудника зоопарка
CONTACT_INFO = os.getenv("CONTACT_INFO")

# ID чата сотрудника зоопарка, куда будут пересылаться результаты
STAFF_CHAT_ID = os.getenv('STAFF_CHAT_ID')


# Клавиатура с кнопками
def get_keyboard(options):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(KeyboardButton(option))
    return keyboard


# Начало викторины
@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    user_scores[message.from_user.id] = {}
    await bot.send_message(message.chat.id,
                           "Привет! Давай выясним, какое ты животное в Московском зоопарке! Отвечай на вопросы:")
    await ask_question(message, 0)


# Функция для отправки вопроса
async def ask_question(message: types.Message, question_idx: int):
    question = questions[question_idx]
    await bot.send_message(message.chat.id, question["text"], reply_markup=get_keyboard(question["options"]))


# Обработка ответов
@dp.message_handler(
    lambda message: message.text in [option for question in questions for option in question['options']])
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    answer = message.text

    if user_id not in user_scores:
        user_scores[user_id] = {}

    # Найдём, на какой вопрос отвечает пользователь
    for idx, question in enumerate(questions):
        if answer in question["options"]:
            # Записываем баллы за ответ
            for animal, score in question["scores"].items():
                if animal not in user_scores[user_id]:
                    user_scores[user_id][animal] = 0
                if answer == question["options"][list(question["scores"].keys()).index(animal)]:
                    user_scores[user_id][animal] += score

            # Если есть ещё вопросы, задаём следующий
            if idx + 1 < len(questions):
                await ask_question(message, idx + 1)
            else:
                await show_result(message)
            break


# Функция показа результатов
async def show_result(message: types.Message):
    user_id = message.from_user.id
    scores = user_scores[user_id]
    best_animal = max(scores, key=scores.get)


    result_text = f"Твоё тотемное животное — {best_animal}!"
    await bot.send_photo(chat_id=message.chat.id, photo=f'{pictures[best_animal]}', caption=f'{result_text}')
    # await bot.send_message(message.chat.id, result_text)

    await bot.send_message(message.chat.id, "Хотите поделиться своим результатом? Нажимайте кнопку 'Поделиться результатом'")

    await bot.send_message(message.chat.id, "Хотите узнать больше о программе опеки? Нажмите на кнопку 'Узнать о программе опеки'")

    await bot.send_message(message.chat.id, "Если хотите задать вопросы или узнать больше, нажмите кнопку 'Связаться с сотрудником'")

    await bot.send_message(message.chat.id, "Хотите оставить отзыв о нашем боте?\nНажимайте кнопку 'Оставить отзыв'")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Поделиться результатом"))
    keyboard.add(KeyboardButton("Узнать о программе опеки"))
    keyboard.add(KeyboardButton("Связаться с сотрудником"))
    keyboard.add(KeyboardButton("Оставить отзыв"))
    keyboard.add(KeyboardButton("Попробовать ещё раз?"))  # Кнопка для перезапуска

    # Отправляем клавиатуру с кнопками за один раз
    await bot.send_message(message.chat.id,
                           "Выберите одно из действий или попробуйте викторину ещё раз:",
                           reply_markup=keyboard)


# Обработка перезапуска викторины
@dp.message_handler(lambda message: message.text == "Попробовать ещё раз?")
async def restart_quiz(message: types.Message):
    # Сбрасываем данные пользователя
    user_id = message.from_user.id
    if user_id in user_scores:
        del user_scores[user_id]

    # Предлагаем начать викторину заново
    await bot.send_message(message.chat.id, "Давайте попробуем ещё раз! Начнём заново.")
    await ask_question(message, 0)  # Снова задаем первый вопрос


# Обработка запроса на контакт с сотрудником
@dp.message_handler(lambda message: message.text == "Связаться с сотрудником")
async def contact_staff(message: types.Message):
    user_id = message.from_user.id
    scores = user_scores[user_id]
    best_animal = max(scores, key=scores.get)

    # Отправляем результат сотруднику
    staff_message = f"Пользователь {message.from_user.full_name} прошел викторину. Его тотемное животное — {best_animal}."
    await bot.send_message(STAFF_CHAT_ID, staff_message)

    # Отправляем пользователю контактную информацию
    await bot.send_message(message.chat.id, f"Ваш результат отправлен сотруднику. {CONTACT_INFO}")


# Обработка дележа результатами
@dp.message_handler(lambda message: message.text == "Поделиться результатом")
async def share_result(message: types.Message):
    user_id = message.from_user.id
    scores = user_scores[user_id]
    best_animal = max(scores, key=scores.get)

    share_link = f"https://t.me/ZOO_BOTbot?start"  # Ссылка на бота
    share_message = f"Я прошел викторину в @ZOO_BOTbot и узнал, что моё тотемное животное — {best_animal}! Присоединяйтесь и узнайте, какое животное подойдёт вам!"

    await bot.send_message(message.chat.id,
                           f"Скопируйте и поделитесь этим сообщением:\n\n{share_message}\n\nСсылка на бота: {share_link}")


# Обработка кнопки "Узнать о программе опеки"
@dp.message_handler(lambda message: message.text == "Узнать о программе опеки")
async def send_care_info(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Программа опеки зоопарка — это отличный способ поддержать животных. Узнайте, "
                           "как можно стать опекуном и помочь нашим друзьям по ссылке: https://moscowzoo.ru/about/guardianship!")


# ID чата для отправки отзывов (замените на нужный ID)
FEEDBACK_CHAT_ID = os.getenv('FEEDBACK_CHAT_ID')



# Обработка нажатия на кнопку "Оставить отзыв"
@dp.message_handler(lambda message: message.text == "Оставить отзыв")
async def ask_for_feedback(message: types.Message):
    await bot.send_message(message.chat.id, "Пожалуйста, напишите ваш отзыв:")
    # Переход в состояние ожидания текста отзыва
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_feedback")


# Обработка текста отзыва от пользователя
@dp.message_handler(state="waiting_for_feedback", content_types=types.ContentTypes.TEXT)
async def handle_feedback(message: types.Message):
    user_id = message.from_user.id
    feedback = message.text

    # Отправка отзыва в специальный чат для сотрудников
    feedback_message = f"Пользователь {message.from_user.full_name} оставил отзыв:\n\n{feedback}"
    await bot.send_message(FEEDBACK_CHAT_ID, feedback_message)

    # Подтверждение пользователю, что отзыв получен
    await bot.send_message(message.chat.id, "Спасибо за ваш отзыв! Мы обязательно его учтем.", reply_markup=types.ReplyKeyboardRemove())

    # Очистка состояния
    await dp.current_state(user=message.from_user.id).reset_state()


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
