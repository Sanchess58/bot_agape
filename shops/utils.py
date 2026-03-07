from typing import Any


def format_product(product: dict[str, Any]) -> str:
    description = f"📝 {product['description']}\n\n" if "description" in product else ""
    return (
        f"📌 <b>{product['name']}</b>\n\n"
        f"{description}"
        f"📦 Количество: {product['quantity']}\n\n"
        f"💰 Цена: {product['price']} монет\n\n"
    )
