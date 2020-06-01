# coding: utf-8

from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor


BOT_TOKEN = '123456789:AAAA-AAAAAAAAAAAAAAAAAAAAAAAA'
PAYMENTS_PROVIDER_TOKEN = '123456789:TEST:12345'


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


prices = [
    types.LabeledPrice(label='test', amount=60000)
]


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "cmd: /buy",
        parse_mode='Markdown'
    )


@dp.message_handler(commands=['buy'])
async def cmd_buy(message: types.Message):
    await bot.send_invoice(
        message.chat.id, title='Test',
        description='test',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='RUB',
        is_flexible=False,
        prices=prices,
        start_parameter='example',
        payload='test'
    )


@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query: types.ShippingQuery):
    await bot.answer_shipping_query(
        shipping_query.id, ok=True, error_message='skip')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="skip")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    amount = message.successful_payment.total_amount / 100
    currency = message.successful_payment.currency

    await bot.send_message(
        message.chat.id,
        '{} {}'.format(amount, currency),
        parse_mode='Markdown'
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
