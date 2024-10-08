from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
import logging

from cons import database

inline_router = Router()


@inline_router.inline_query()
async def user_inline_handler(inline_query: InlineQuery):
    try:
        if inline_query.query == "":
            products = database['products']
            inline_list = []
            for i, (product_k, product_v) in enumerate(products.items()):
                inline_list.append(InlineQueryResultArticle(
                    id=product_k,
                    title=product_v.get('name', 'Unknown'),
                    input_message_content=InputTextMessageContent(
                        message_text=f"<i>{product_v.get('text', 'No description available')[2:]}</i>Buyurtma qilish uchun  : @temurs_book_shop_bot\n\nbook_id: {product_k}"
                    ),
                    thumbnail_url=product_v.get('thumbnail_url', 'default_thumbnail_url'),
                    description=f"Factor Books\n💵 Narxi: {product_v.get('price', 'default_price')} so'm",
                ))
                if i == 50:
                    break

            await inline_query.answer(inline_list)
        else:
            products = {k: v for k, v in database['products'].items() if
                        inline_query.query.lower() in v.get('name', 'Unknown').lower()}
            inline_list = []
            for i, (product_k, product_v) in enumerate(products.items()):
                inline_list.append(InlineQueryResultArticle(
                    id=product_k,
                    title=product_v['name'],
                    input_message_content=InputTextMessageContent(
                        message_text=f"<i>{product_v['text'][2:]}</i>Buyurtma qilish uchun  : @Temurs_book_shop_bot\n\nbook_id: {product_k}"
                    ),
                    thumbnail_url=product_v['thumbnail_url'],
                    description=f"Factor Books\n💵 Narxi: {product_v['price']} so'm",
                ))
                if i == 50:
                    break

            await inline_query.answer(inline_list)


    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"Error handling inline query: {e}")
