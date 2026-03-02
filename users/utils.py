from datetime import datetime


def format_user(user: dict) -> str:
    birthday = datetime.fromisoformat(user["birthday"]) if user.get("birthday") else ""
    return (
        f"👤 <b>{user['first_name']} {user['last_name']}</b>\n"
        f"🎂 {birthday.date() if birthday else 'Не указано'}\n"
        f"🔗 @{user['login']}\n\n"
    )


def format_event_user(user: dict) -> str:
    return (
        f"👤 <b>{user['first_name']} {user['last_name']}</b>\n"
        f"🔗 @{user['login']}\n\n"
    )
