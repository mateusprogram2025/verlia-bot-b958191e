import discord
from discord.ext import commands
import os

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True # Permite que o bot leia o conteúdo das mensagens
intents.members = True # Necessário se você quiser interagir com membros

bot = commands.Bot(command_prefix='!', intents=intents)

# === DADOS DOS PRODUTOS (FIXOS, sem banco de dados) ===
PRODUCTS = {
    "item1": {
        "name": "Produto Incrível 1",
        "description": "Uma descrição detalhada do Produto Incrível 1. É super útil!",
        "price": "R$ 29.99",
        "image_url": "https://i.imgur.com/example1.png", # Substitua pela URL real da imagem
        "link": "https://sua-loja-externa.com/item1"
    },
    "item2": {
        "name": "Produto Fantástico 2",
        "description": "Este é o Produto Fantástico 2, ele vai mudar sua vida!",
        "price": "R$ 59.90",
        "image_url": "https://i.imgur.com/example2.png", # Substitua pela URL real da imagem
        "link": "https://sua-loja-externa.com/item2"
    },
    "item3": {
        "name": "Produto Maravilhoso 3",
        "description": "Não perca o Produto Maravilhoso 3, oferta por tempo limitado!",
        "price": "R$ 19.99",
        "image_url": "https://i.imgur.com/example3.png", # Substitua pela URL real da imagem
        "link": "https://sua-loja-externa.com/item3"
    }
}
# =======================================================


@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print(f'📊 Servidores: {len(bot.guilds)}')
    await bot.tree.sync()  # Sincroniza slash commands

@bot.command(name='produtos')
async def list_products(ctx):
    """Lista todos os produtos disponíveis."""
    embed = discord.Embed(
        title="🛒 Nossos Produtos Incríveis!",
        description="Confira abaixo os itens que temos para você! Clique nos links para comprar.",
        color=discord.Color.blue()
    )
    
    for product_id, product_info in PRODUCTS.items():
        embed.add_field(
            name=f"✨ {product_info['name']} - {product_info['price']}",
            value=f"{product_info['description']}\n[Comprar Agora!]({product_info['link']})",
            inline=False
        )
        if product_info.get("image_url"):
            embed.set_thumbnail(url=product_info["image_url"]) # Você pode preferir colocar a imagem uma vez só no footer ou description

    embed.set_footer(text="Aproveite nossas ofertas! ✨")
    await ctx.send(embed=embed)

@bot.command(name='comprar')
async def buy_product(ctx, product_id: str):
    """Retorna o link de compra para um produto específico."""
    product_id = product_id.lower()
    if product_id in PRODUCTS:
        product = PRODUCTS[product_id]
        embed = discord.Embed(
            title=f"🛍️ Você escolheu: {product['name']}",
            description=f"Preço: {product['price']}\nPara comprar, clique no link abaixo:",
            color=discord.Color.green(),
            url=product['link'] # Link principal do embed
        )
        embed.add_field(name="Link de Compra", value=f"[Acesse aqui para comprar!]({product['link']})", inline=False)
        if product.get("image_url"):
            embed.set_thumbnail(url=product["image_url"])
        embed.set_footer(text="Obrigado pela preferência!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Produto não encontrado! Use `!produtos` para ver a lista completa.")

@bot.command(name='loja')
async def shop_link(ctx):
    """Envia o link geral da sua loja."""
    embed = discord.Embed(
        title="🌐 Visite Nossa Loja Online!",
        description="Confira todos os nossos produtos e novidades em nossa loja virtual:",
        url="https://sua-loja-externa.com", # Substitua pelo link da sua loja
        color=discord.Color.purple()
    )
    embed.add_field(name="Link Direto", value="[Clique aqui para ir para a loja!](https://sua-loja-externa.com)", inline=False)
    embed.set_footer(text="Estamos esperando por você! 😊")
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════
# 🔌 CONEXÃO DO BOT - NUNCA REMOVA ESTA LINHA
# ═══════════════════════════════════════════
bot.run(os.environ.get('BOT_TOKEN'))