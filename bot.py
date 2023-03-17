from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor
from utils import send_email, create_pdf_loading, create_pdf_client, create_pdf_uploading, write_data_to_excel_uploading, write_data_to_excel_loading, write_data_to_excel_client, insert_db_client, insert_db_loading, insert_db_uploading
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import dbase as fc
import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from word import create_word
from word2 import create_pass_word


# Здесь необходимо указать токен вашего бота, который вы получили у @BotFather
bot = Bot(token='6243897431:AAFgVVNcRxkSaj-PNVXwSV0b32TwRqpElMQ')

# Создание объекта диспетчера и подключение к нему памяти
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    if message.from_user.id == 396595993 or message.from_user.id == 2090061565 or message.from_user.id == 6096101009:
        try:
            fc.add_user(message.from_user.id, message.from_user.username)
            with open('welcome.jpg', 'rb') as photo_file:
                photo = types.InputFile(photo_file)
                await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='👋Добро пожаловать!\n Я бот Компании "Юнифол" для оформления пропусков.🤖 \nЧтобы узнать как пользоваться ботом, воспользуйтесь командой /help\nНаш адресс: г. Фрязино, Окружной пр., д. 5\nК успеху вместе!✅')
            await bot.send_message(chat_id=message.from_user.id, text='Добро пожаловать, как Администратору вам доступны следующие команды\n/get_all_loading - получить все заявки на погрузку\n/get_all_uploading - получить все заявки на выгрузку\n/broadcast - запустить текстовую рассылку\n/send_file - загрузить excel отчет')
        except Exception as e:
            print(e)
            await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')
    else:
        try:
            fc.add_user(message.from_user.id, message.from_user.username)
            with open('welcome.jpg', 'rb') as photo_file:
                photo = types.InputFile(photo_file)
                await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='👋Добро пожаловать!\n Я бот Компании "Юнифол" для оформления пропусков.🤖 \nЧтобы узнать как пользоваться ботом, воспользуйтесь командой /help\nНаш адресс: г. Фрязино, Окружной пр., д. 5\nК успеху вместе!✅')
        except:
            await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(commands=['help'])
async def help_cmd_handler(message: types.Message):
    await message.answer("Наш бот предназначен для оформления пропусков🪪 для клиентов, машин выгрузки и погрузки\nЧтобы заполнить заявку на пропуск воспользуйтесь боковым меню и выберите подходящий для вас пункт!👇")


class PassForm(StatesGroup):
    company = State()
    fio = State()
    doc = State()

class LoadingForm(StatesGroup):
    fio = State()
    company = State()
    doc = State()
    car_num = State()
    tel = State()
    fio_man = State()
    transit = State()
    attorney = State()

class UploadingForm(StatesGroup):
    company = State()
    fio = State()
    doc = State()
    car_num = State()
    fio_man = State()
    transit = State()
    attorney = State()

class MyForm(StatesGroup):
    text = State()


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Нет активных операций для отмены')
        return

    async with state.proxy() as data:
        
        # очистка состояний формы
        data.clear()
    
    # отправка сообщения о том, что заявка отменена
    await message.answer('Операция прервана')

    # завершение FSM
    await state.finish()


@dp.message_handler(commands=['pass_client'])
async def pass_cmd_handler(message: types.Message, state: FSMContext):
    try:
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()
        
        # Запрос ФИО пользователя
        await message.answer("🙋‍♂️Оформление пропуска для клиентов\nОтменить действие /cancel\nНазвание компании:")
        await PassForm.company.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=PassForm.company)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['company'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите ваше ФИО:")
        await PassForm.fio.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=PassForm.fio)
async def process_birth_date(message: types.Message, state: FSMContext):
    try:
        # Сохранение даты рождения пользователя
        async with state.proxy() as data:
            data['fio'] = message.text
    
    
        # Запрос даты визита пользователя
        await message.answer("Введите номер документа удостоверяющего личность")
        await PassForm.doc.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(state=PassForm.doc)
async def process_visit_date(message: types.Message, state: FSMContext):
    try:
        # Сохранение даты визита пользователя
        async with state.proxy() as data:
            data['doc'] = message.text

        
        # Создание pdf документа
        pdf_data = create_pdf_client(data['company'], data['fio'], data['doc'])
        # Отправка email администратору
        await message.answer("⌛️Ожидайте...")
        insert_db_client(data['company'], data['fio'], data['doc'])
        send_email(pdf_data, theme="Новая заявка на пропуск для клиента")
        write_data_to_excel_client(data['company'], data['fio'], data['doc'])
        # Ответ пользователю
        await message.answer("✅Ваша заявка на пропуск отправлена администратору компании.")
        
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()

        # Завершение FSM
        await state.finish()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

#код по загрузке//////////////////////////////////////////////////////
@dp.message_handler(commands=['pass_load'])
async def pass_cmd_handler(message: types.Message, state: FSMContext):
    try:
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()
        
        # Запрос ФИО пользователя
        await message.answer("🚛(ПОГРУЗКА) Оформление пропуска для машин погрузки\nОтменить действие /cancel\nВведите ваше ФИО:")
        await LoadingForm.fio.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(state=LoadingForm.fio)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['fio'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите название компании грузополучателя:")
        await LoadingForm.company.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=LoadingForm.company)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['company'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите номер документа удостоверяющего личность:")
        await LoadingForm.doc.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=LoadingForm.doc)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['doc'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите номер машины:")
        await LoadingForm.car_num.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=LoadingForm.car_num)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['car_num'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите номер телефона:")
        await LoadingForm.tel.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=LoadingForm.tel)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['tel'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите ФИО менеджера нашей компании:")
        await LoadingForm.fio_man.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(state=LoadingForm.fio_man)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['fio_man'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Машина тразнитная или пустая?")
        await LoadingForm.transit.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(state=LoadingForm.transit)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['transit'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Доверенность есть или нет?")
        await LoadingForm.attorney.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=LoadingForm.attorney)
async def process_visit_date(message: types.Message, state: FSMContext):
    try:
        # Сохранение даты визита пользователя
        async with state.proxy() as data:
            data['attorney'] = message.text

        
        # Создание pdf документа
        pdf_data = create_pdf_loading(data['fio'], data['company'], data['doc'], data['car_num'], data['tel'], data['fio_man'], data['transit'], data['attorney'])
        # Отправка email администратору
        await message.answer("⌛️Ожидайте...")
        create_pass_word(data['fio'], data['company'],  data['doc'], data['car_num'])
        insert_db_loading(data['fio'], data['company'], data['doc'], data['car_num'], data['tel'], data['fio_man'], data['transit'], data['attorney'])
        send_email(pdf_data, theme="Новая заявка на пропуск для машины погрузки")
        # Ответ пользователю
        write_data_to_excel_loading(data['fio'], data['company'], data['doc'], data['car_num'], data['tel'], data['fio_man'], data['transit'], data['attorney'])
        await message.answer("✅Ваша заявка на пропуск отправлена администратору компании.")
        
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()

        # Завершение FSM
        await state.finish()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


#код по выгрузке//////////////////////////////////////////////////////
@dp.message_handler(commands=['pass_upload'])
async def pass_cmd_handler(message: types.Message, state: FSMContext):
    try:
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()
        
        # Запрос ФИО пользователя
        await message.answer("🚚(ВЫГРУЗКА) Оформление пропуска для машин выгрузки\nОтменить действие /cancel\nВведите название компании грузоотправителя:")
        await UploadingForm.company.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.company)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['company'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите ФИО:")
        await UploadingForm.fio.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.fio)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['fio'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите название документа удостоверяющего личность:")
        await UploadingForm.doc.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.doc)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['doc'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите номер машины:")
        await UploadingForm.car_num.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.car_num)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['car_num'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Введите контактное лицо:")
        await UploadingForm.fio_man.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.fio_man)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['fio_man'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Тразнит или пустая машина?")
        await UploadingForm.transit.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')

@dp.message_handler(state=UploadingForm.transit)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        # Сохранение ФИО пользователя
        async with state.proxy() as data:
            data['transit'] = message.text
        
        # Запрос даты рождения пользователя
        await message.answer("Есть доверенность или нет?")
        await UploadingForm.attorney.set()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(state=UploadingForm.attorney)
async def process_visit_date(message: types.Message, state: FSMContext):
    try:
        # Сохранение даты визита пользователя
        async with state.proxy() as data:
            data['attorney'] = message.text

        
        # Создание pdf документа
        pdf_data = create_pdf_uploading(data['company'], data['fio'], data['doc'], data['car_num'], data['fio_man'], data['transit'], data['attorney'])
        # Отправка email администратору
        await message.answer("⌛️Ожидайте...")
        create_pass_word(data['fio'], data['company'],  data['doc'], data['car_num'])
        insert_db_uploading(data['company'], data['doc'], data['car_num'], data['fio'], data['fio_man'], data['transit'], data['attorney'])
        send_email(pdf_data, theme="Новая заявка на пропуск для машины выгрузки")
        # Ответ пользователю
        write_data_to_excel_uploading(data['company'], data['fio'], data['doc'], data['car_num'], data['fio_man'], data['transit'], data['attorney'])
        await message.answer("✅Ваша заявка на пропуск отправлена администратору компании.")
        
        # Очистка состояний формы
        async with state.proxy() as data:
            data.clear()

        # Завершение FSM
        await state.finish()
    except:
        await message.answer('Что-то пошло не так!\nПопробуйте заново или обратитесь по телефону +79999999999')


@dp.message_handler(commands=['broadcast'])
async def handle_broadcast(message: types.Message):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id == 396595993 or message.from_user.id == 2090061565 or message.from_user.id == 6096101009:
        # Запрашиваем текст для рассылки
        await message.answer("Введите текст для рассылки:")
        # Устанавливаем состояние, в котором будем ждать текста для рассылки
        await MyForm.text.set()
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

# Функция, которая будет вызываться после ввода текста для рассылки
@dp.message_handler(state=MyForm.text)
async def send_broadcast(message: types.Message, state: FSMContext):
    # Получаем текст для рассылки из состояния
    text = message.text
    users = fc.all_user()
    c=0
    # Отправляем сообщение каждому пользователю из списка
    for user_id in users:
        try:
            await bot.send_message(user_id[0], text)
            c = c + 1
        except:
            pass
    # Сбрасываем состояние
    await state.finish()


#Админ панель///////////////////////////////////////////////////////////////////////
# создание объекта CallbackData для обработки коллбэков кнопок "одобрить" и "отказать"
approve_decline_callback = CallbackData("approve_decline", "id", "action", "t")

@dp.message_handler(commands=['get_all_loading'])
async def get_all_client_handler(message: types.Message):
    if message.from_user.id == 396595993 or message.from_user.id == 2090061565 or message.from_user.id == 6096101009:
        conn = sqlite3.connect('database_uf.db')
        cursor = conn.cursor()
        
        # Получение всех заявок со статусом 0
        cursor.execute("SELECT * FROM loading WHERE status = 0")
        rows = cursor.fetchall()

        # Если нет заявок с таким статусом
        if not rows:
            await message.answer("Нет заявок на пропуск со статусом 'ожидание'!")
            return

        # Создание клавиатуры с кнопками "одобрить" и "отказать" для каждой заявки
        
        for row in rows:
            markup = InlineKeyboardMarkup()
            # Создание кнопок
            approve_button = InlineKeyboardButton("Одобрить", callback_data=approve_decline_callback.new(id=row[9], action="approve", t="l"))
            decline_button = InlineKeyboardButton("Отказать", callback_data=approve_decline_callback.new(id=row[9], action="decline", t="l"))
            # Добавление кнопок в клавиатуру
            markup.row(approve_button, decline_button)
            # Отправка сообщения в чат с данными о заявке и клавиатурой
            await message.answer(f"Заявка от {row[0]}\nКомпания: {row[1]}\nФИО: {row[0]}\nНомер документа: {row[2]}\nНомер машины: {row[3]}\nФИО ответственного: {row[5]}\nТранзит: {row[6]}\nДоверенность: {row[7]}", reply_markup=markup)

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


@dp.message_handler(commands=["send_file"])
async def send_file_command_handler(message: types.Message):
    if message.from_user.id == 396595993 or message.from_user.id == 2090061565 or message.from_user.id == 6096101009:
        # получаем имя файла из текста сообщения
        # открываем файл в бинарном режиме
        with open('work_pass_data.xlsx', "rb") as file:
            # отправляем файл пользователю
            await bot.send_document(message.chat.id, file)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.callback_query_handler(approve_decline_callback.filter())
async def process_approve_decline_callback(callback_query: types.CallbackQuery, callback_data: dict):
    # Извлекаем id заявки и действие из callback_data
    pass_id = callback_data['id']
    action = callback_data['action']
    type = callback_data['t']
    # Открываем соединение с базой данных
    conn = sqlite3.connect('database_uf.db')
    cursor = conn.cursor()
    # Обновляем статус заявки в базе данных в соответствии с действием
    if type == 'l':
        row = cursor.execute(f"SELECT * FROM loading WHERE id = '{pass_id}'").fetchone()
        if action == "approve":
            try:
                cursor.execute(f"UPDATE loading SET status=1 WHERE id='{pass_id}'")
                status_text = "одобрена"
                create_pass_word(row[0], row[1], row[2], row[3])
                await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
                with open('pass.docx', 'rb') as file:
                    await bot.send_document(callback_query.from_user.id, file, caption=f'Пропуск для {row[0]} готов')

            except:
                pass
        elif action == "decline":
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'Заявка от {row[0]} отклонена')
            cursor.execute(f"UPDATE loading SET status=2 WHERE id='{pass_id}'")
            status_text = "отклонена"
    elif type == 'u':
        print(pass_id)
        row = cursor.execute(f"SELECT * FROM uploading WHERE id = '{pass_id}'").fetchone()
        print(row)
        if action == "approve":
            try:
                cursor.execute(f"UPDATE uploading SET status=1 WHERE id='{pass_id}'")
                status_text = "одобрена"
                create_pass_word(row[2], row[0], row[3], row[1])
                await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
                with open('pass.docx', 'rb') as file:
                    await bot.send_document(callback_query.from_user.id, file, caption=f'Пропуск для {row[2]} готов')

            except Exception as e:
                print(e)
        elif action == "decline":
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            print(row)
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'Заявка от {row[2]} отклонена')
            cursor.execute(f"UPDATE uploading SET status=2 WHERE id='{pass_id}'")
            status_text = "отклонена"

    # Сохраняем изменения в базе данных
    conn.commit()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    # Отправляем сообщение с текстом об одобрении или отклонении заявки
    await callback_query.answer(f"Заявка №{pass_id} {status_text}")


async def update_message_with_pass_info(message: types.Message, pass_id: int):
    # Открываем соединение с базой данных
    conn = sqlite3.connect('database_uf.db')
    cursor = conn.cursor()

    # Получаем данные о заявке из базы данных
    cursor.execute(f"SELECT * FROM loading WHERE id='{pass_id}'")
    row = cursor.fetchone()

    # Если заявка не найдена, отправляем сообщение и выходим из функции
    if row is None:
        await message.answer('Заявка не найдена')
        return

    # Создаем новую клавиатуру с кнопками в соответствии с новым статусом заявки
    markup = InlineKeyboardMarkup()
    if row[8] == 0:
        approve_button = InlineKeyboardButton("Одобрить", callback_data=approve_decline_callback.new(id=pass_id, action="approve"))
        decline_button = InlineKeyboardButton("Отказать", callback_data=approve_decline_callback.new(id=pass_id, action="decline"))
        markup.row(approve_button, decline_button)

    # Обновляем сообщение с новыми данными и клавиатурой
    await message.edit_text(f"Заявка от {row[0]}:\nКомпания: {row[1]}\nНомер документа: {row[2]}\nНомер машины: {row[3]}\nФИО ответственного: {row[5]}\nТранзит: {row[6]}\nДоверенность: {row[7]}")



@dp.message_handler(commands=['get_all_uploading'])
async def get_all_client_handler(message: types.Message):
    if message.from_user.id == 396595993 or message.from_user.id == 2090061565 or message.from_user.id == 6096101009:
        # Открытие соединения с базой данных
        conn = sqlite3.connect('database_uf.db')
        cursor = conn.cursor()
        
        # Получение всех заявок со статусом 0
        cursor.execute("SELECT * FROM uploading WHERE status = 0")
        rows = cursor.fetchall()

        # Если нет заявок с таким статусом
        if not rows:
            await message.answer("Нет заявок на пропуск со статусом 'ожидание'!")
            return

        # Создание клавиатуры с кнопками "одобрить" и "отказать" для каждой заявки
        markup = InlineKeyboardMarkup()
        for row in rows:
            # Создание кнопок
            markup = InlineKeyboardMarkup()
            approve_button = InlineKeyboardButton("Одобрить", callback_data=approve_decline_callback.new(id=row[8], action="approve", t="u"))
            decline_button = InlineKeyboardButton("Отказать", callback_data=approve_decline_callback.new(id=row[8], action="decline", t="u"))
            # Добавление кнопок в клавиатуру
            markup.row(approve_button, decline_button)
            # Отправка сообщения в чат с данными о заявке и клавиатурой
            await message.answer(f"Заявка от {row[2]}\nКомпания: {row[0]}\nФИО: {row[2]}\nНомер документа: {row[3]}\nНомер машины: {row[1]}\nФИО ответственного: {row[4]}\nТранзит: {row[5]}\nДоверенность: {row[6]}", reply_markup=markup)

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


# @dp.callback_query_handler(approve_decline_callback_uploading.filter())
# async def process_approve_decline_callback(callback_query: types.CallbackQuery, callback_data: dict):
#     # Извлекаем id заявки и действие из callback_data
#     print(1)
#     print(callback_query)
#     pass_id = callback_data['id']
#     print(pass_id)
#     action = callback_data['action']
#     print(action)
#     # Открываем соединение с базой данных
#     conn = sqlite3.connect('database_uf.db')
#     cursor = conn.cursor()
#     row = cursor.execute(f"SELECT * FROM uploading WHERE id = '{pass_id}'").fetchone()
#     print(row)
#     # Обновляем статус заявки в базе данных в соответствии с действием
#     if action == "approve":
#         try:
#             cursor.execute(f"UPDATE uploading SET status=1 WHERE id='{pass_id}'")
#             status_text = "одобрена"
#             create_pass_word(row[0], row[1], row[2], row[3])
#             await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
#             with open('pass.docx', 'rb') as file:
#                 await bot.send_document(callback_query.from_user.id, file, caption=f'Пропуск для {row[0]} готов')

#         except Exception as e:
#             print(e)
#     elif action == "decline":
#         await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
#         print(row)
#         await bot.send_message(chat_id=callback_query.from_user.id, text=f'Заявка от {row[0]} отклонена')
#         cursor.execute(f"UPDATE loading SET status=2 WHERE id='{pass_id}'")
#         status_text = "отклонена"

#     # Сохраняем изменения в базе данных
#     conn.commit()

#     # Закрываем соединение с базой данных
#     cursor.close()
#     conn.close()

#     # Отправляем сообщение с текстом об одобрении или отклонении заявки
#     await callback_query.answer(f"Заявка №{pass_id} {status_text}")

async def update_message_with_pass_info(message: types.Message, pass_id: int):
    # Открываем соединение с базой данных
    conn = sqlite3.connect('database_uf.db')
    cursor = conn.cursor()

    # Получаем данные о заявке из базы данных
    cursor.execute(f"SELECT * FROM uploading WHERE id='{pass_id}'")
    row = cursor.fetchone()

    # Если заявка не найдена, отправляем сообщение и выходим из функции
    if row is None:
        await message.answer('Заявка не найдена')
        return

    # Создаем новую клавиатуру с кнопками в соответствии с новым статусом заявки
    markup = InlineKeyboardMarkup()
    if row[8] == 0:
        approve_button = InlineKeyboardButton("Одобрить", callback_data=approve_decline_callback.new(id=pass_id, action="approve"))
        decline_button = InlineKeyboardButton("Отказать", callback_data=approve_decline_callback.new(id=pass_id, action="decline"))
        markup.row(approve_button, decline_button)

    # Обновляем сообщение с новыми данными и клавиатурой
    await message.edit_text(f"Заявка от {row[0]}:\nКомпания: {row[1]}\nФИО: {row[2]}\nНомер документа: {row[3]}\nНомер машины: {row[4]}\nФИО ответственного: {row[5]}\nТранзит: {row[6]}\nДоверенность: {row[7]}")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
