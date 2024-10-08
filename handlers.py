from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

handler_router = Router()

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from cons import database
from keyboard import show_categories, make_plus_minus, main_keyboard_btn

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    rkb = main_keyboard_btn()
    msg = _('Assalomu alaykum! Tanlang.')
    if str(message.from_user.id) not in database['users']:
        msg = _('Assalomu alaykum! \nXush kelibsiz!')
        users = database['users']
        users[str(message.from_user.id)] = True
        database['users'] = users
    await message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(_('''Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam'''))


@main_router.message(F.text == __('🌐 Tilni almashtirish'))
async def change_language(message: Message) -> None:
    keyboards = InlineKeyboardBuilder()
    keyboards.row(InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
                  InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en'))

    await message.answer(_('Tilni tanlang: '), reply_markup=keyboards.as_markup())


@main_router.callback_query(F.data.startswith('lang_'))
async def languages(callback: CallbackQuery, state: FSMContext) -> None:
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    if lang_code == 'uz':
        lang = _('Uzbek', locale=lang_code)
    else:
        lang = _('Ingiliz', locale=lang_code)

    await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))

    rkb = main_keyboard_btn(locale=lang_code)
    msg = _('Assalomu alaykum! Tanlang.', locale=lang_code)
    await callback.message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(F.text == __('🔵Biz ijtimoyi tarmoqlarda'))
async def our_social_network(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='IKAR | Factor Books', url='https://t.me/ikar_factor'))
    ikb.row(InlineKeyboardButton(text='Factor Books', url='https://t.me/factor_books'))
    ikb.row(InlineKeyboardButton(text='\"Factor Books\" nashiryoti', url='https://t.me/factorbooks'))
    await message.answer(_('Biz ijtimoiy tarmoqlarda'), reply_markup=ikb.as_markup())


@main_router.message(F.text == __('📚 Kitoblar'))
async def books(message: Message) -> None:
    ikb = show_categories(message.from_user.id)
    await message.answer(_('Kategoriyalardan birini tanlang'), reply_markup=ikb.as_markup())


@main_router.callback_query(F.data.startswith('orqaga'))
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text(_('Kategoriyalardan birini tanlang'),
                                     reply_markup=show_categories(callback.from_user.id).as_markup())


@main_router.message(F.text == __("📞 Biz bilan bog'lanish"))
async def message(message: Message) -> None:
    text = _("""\n
\n
Telegram: @C_W24\n
📞  +{number}\n
🤖 Bot Kozimov Temur (@C_W24) tomonidan tayorlandi.\n""".format(number=998970501655))
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@main_router.message(lambda msg: msg.text[-36:] in database['products'])
async def answer_inline_query(message: Message):
    msg = message.text[-36:]
    product = database['products'][msg]
    ikb = make_plus_minus(1, msg)
    await message.delete()
    await message.answer_photo(photo=product['image'], caption=product['text'], reply_markup=ikb.as_markup())


@main_router.callback_query()
async def product_handler(callback: CallbackQuery):
    if callback.data in database['categories']:
        ikb = InlineKeyboardBuilder()
        for k, v in database['products'].items():
            if 'category_id' in v and v['category_id'] == callback.data:
                ikb.add(InlineKeyboardButton(text=v['name'], callback_data=k))
        if str(callback.from_user.id) in database['basket']:
            ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(database["basket"][str(callback.from_user.id)])})',
                                         callback_data='savat'))
        ikb.add(InlineKeyboardButton(text=_("◀️ orqaga"), callback_data='orqaga'))
        ikb.adjust(2, repeat=True)
        await callback.message.edit_text(str(database['categories'][callback.data]), reply_markup=ikb.as_markup())
    elif callback.data in database['products']:
        product = database['products'][callback.data]
        ikb = make_plus_minus(1, callback.data)
        await callback.message.delete()
        await callback.message.answer_photo(photo=product['image'], caption=product['text'],
                                            reply_markup=ikb.as_markup())
