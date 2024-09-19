from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

register_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Поделитесь контактом!", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

commands_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Список артефактов", callback_data="arts_list"),
                      InlineKeyboardButton(text="Список предметов", callback_data="items_list")],
                     [InlineKeyboardButton(text="Избранное", callback_data="marked_items"),
                      InlineKeyboardButton(text="Связь с разработчиком", callback_data="developer")],
                     ])

go_back_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")]]
)

rarities = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обычный", callback_data="rarity_0"),
         InlineKeyboardButton(text="Необычный", callback_data="rarity_1"),
         InlineKeyboardButton(text="Особый", callback_data="rarity_2")],
        [InlineKeyboardButton(text="Редкий", callback_data="rarity_3"),
         InlineKeyboardButton(text="Исключительный", callback_data="rarity_4"),
         InlineKeyboardButton(text="Легендарный", callback_data="rarity_5")]],
    one_time_keyboard=True,
    resize_keyboard=True
)

find_lots_kb = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Первые 3", callback_data="lots_3"),
        InlineKeyboardButton(text="Первые 5", callback_data="lots_5")
    ], [
        InlineKeyboardButton(text="Первые 10", callback_data="lots_10"),
        InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
    ]]
)
