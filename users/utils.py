from datetime import datetime


def format_user(user: dict) -> str:
    birthday = datetime.fromisoformat(user["birthday"]) if user.get("birthday") else ""
    return (
        f"👤 <b>{user['first_name']} {user['last_name']}</b>\n"
        f"🎂 {datetime.strftime(birthday, '%d.%m.%Y') if birthday else 'Не указано'}\n"
        f"💬 {user.get('referral_source', 'Не указано')}\n"
        f"Из храма: {user.get('church', 'Не указано')}\n"
        f"🔗 @{user['login']}\n\n"
    )
