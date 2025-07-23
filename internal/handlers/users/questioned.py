from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import Config
from internal.app.app import bot
from internal.entities.database import users
from internal.entities.states.StateModels import QuestionedData
from internal.entities.states.states import UserStates
from pkg.get_message import get_mes
from pkg.steps import steps_schema

router = Router()

config = Config.load()

@router.message(Command("reset"))
@router.callback_query(F.data == "start_questioned")
async def start(message: CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()

    step_id = 0
    questioned = QuestionedData()
    await state.set_state(UserStates.steps)

    msg = await bot.send_message(chat_id=user_id,
                                 text=steps_schema.steps[0].prompt,
                                 reply_markup=steps_schema.steps[0].keyboard
                                 )

    await state.update_data(step_id=step_id,
                            questioned=questioned,
                            message_id=msg.message_id)


@router.message(UserStates.steps)
async def step_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    message_id = data.get("message_id")
    questioned: QuestionedData = data.get("questioned")
    step_id = data.get("step_id")
    old_step = steps_schema.steps[step_id]
    setattr(questioned, old_step.name, message.text)
    step_id += 1
    await message.delete()
    if step_id == len(steps_schema.steps):
        user = await users.get(user_id)
        user.city = questioned.city
        user.full_name = questioned.full_name
        user.age = questioned.age
        user.position = questioned.position
        user.ai_level = questioned.ai_level
        await users.update(user)
        await state.clear()
        return await bot.edit_message_text(chat_id=user_id,
                                           message_id=message_id,
                                           text=get_mes("confirm"))
    step = steps_schema.steps[step_id]
    await state.update_data(step_id=step_id,
                            questioned=questioned
                            )
    await bot.edit_message_text(chat_id=user_id,
                                message_id=message_id,
                                text=step.prompt,
                                reply_markup=step.keyboard)


@router.callback_query(UserStates.steps)
async def step_callback(message: CallbackQuery, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    questioned: QuestionedData = data.get("questioned")
    message_id = data.get("message_id")
    step_id = data.get("step_id")

    old_step = steps_schema.steps[step_id]
    setattr(questioned, old_step.name, message.data)
    step_id += 1
    if step_id == len(steps_schema.steps):
        user = await users.get(user_id)
        user.city = questioned.city
        user.full_name = questioned.full_name
        user.age = questioned.age
        user.position = questioned.position
        user.ai_level = questioned.ai_level
        user.position_repeat = questioned.position_repeat
        await users.update(user)
        await state.clear()
        return await bot.edit_message_text(chat_id=user_id,
                                           message_id=message_id,
                                           text=get_mes("confirm"))

    step = steps_schema.steps[step_id]
    await state.update_data(step_id=step_id,
                            questioned=questioned
                            )
    await bot.edit_message_text(chat_id=user_id,
                                message_id=message_id,
                                text=step.prompt,
                                reply_markup=step.keyboard)


questioned_rt = router
