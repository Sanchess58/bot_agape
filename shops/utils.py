def format_product(product: dict) -> str:
    return (
        f"📌 <b>{product['name']}</b>\n\n"
        f"📝 {product['description']}\n\n"
        f"📦 Количество: {product['quantity']}\n\n"
        f"💰 Цена: {product['price']} монет\n\n"
    )
