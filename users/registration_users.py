import httpx
from datetime import datetime
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants import API_BASE_URL
from main_menu import menu
from routers import users_router


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()
    church = State()
    referral_source = State()
    birthday = State()


@users_router.message(F.text == "Регистрация")
async def register_start(message: types.Message, state: FSMContext):
    await state.set_state(Registration.first_name)
    await message.answer("Введите ваше имя:")


@users_router.message(Registration.first_name)
async def reg_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Registration.last_name)
    await message.answer("Введите вашу фамилию:")


@users_router.message(Registration.last_name)
async def reg_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.gender)
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Укажите ваш пол:", reply_markup=kb)


@users_router.message(Registration.gender)
async def reg_gender(message: types.Message, state: FSMContext):
    valid_genders = {"Мужской", "Женский"}

    if message.text not in valid_genders:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer(
            "❌ Неверный выбор. Пожалуйста, выберите пол, используя кнопки ниже:",
            reply_markup=kb
        )
        return
    await state.update_data(gender=message.text)
    await state.set_state(Registration.birthday)
    await message.answer("Введите вашу дату рождения (в формате ДД-ММ-ГГГГ):")


@users_router.message(Registration.birthday)
async def reg_birthday(message: types.Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, "%d-%m-%Y")
        birthday = datetime.strftime(date_obj, "%Y-%d-%m")
    except ValueError:
        await message.answer("❌ Некорректно указана дата! Введите вашу дату рождения (в формате ДД-ММ-ГГГГ):")
        return

    await state.update_data(birthday=birthday)
    await state.set_state(Registration.church)
    await message.answer("Укажите храм, куда ходите:")
    

@users_router.message(Registration.church)
async def reg_church(message: types.Message, state: FSMContext):
    await state.update_data(church=message.text)
    await state.set_state(Registration.referral_source)
    await message.answer("Откуда о нас узнали:")


@users_router.message(Registration.referral_source)
async def reg_referral_source(message: types.Message, state: FSMContext):
    await state.update_data(referral_source=message.text)

    data = await state.get_data()

    user_payload = {
        "telegram_id": message.from_user.id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "login": message.from_user.username,
        "birthday": data["birthday"],
        "gender": data["gender"],
        "church": data.get("church", ""),
        "referral_source": data.get("referral_source", "")
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/users/", json=user_payload)
            if response.status_code == httpx.codes.BAD_REQUEST:
                await message.answer("Аккаунт уже зарегистрирован")
                return await menu(message)
            response.raise_for_status()
            await message.answer("Регистрация прошла успешно!")
            await menu(message)

    except Exception:
        await message.answer("⚠️ Ошибка при регистрации! Попробуйте снова!")
        await state.set_state(Registration.first_name)
        await message.answer("Введите ваше имя:")

    await state.clear()
