from aiogram.filters.callback_data import CallbackData


class RegisterEventCallback(CallbackData, prefix="register_event"):
    event_id: int


class GetUserEventCallback(CallbackData, prefix="user_event"):
    event_id: int


class ConfirmationUserEventCallback(CallbackData, prefix="confirmation_user_event"):
    event_id: int
    user_id: int
    attended: bool
