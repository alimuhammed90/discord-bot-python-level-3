import discord
from discord.ext import commands
from config import token  # Botun tokenini config dosyasından içe aktarma

intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.event
async def on_message(message):
    # Botların kendi mesajlarını kontrol etme
    if message.author.bot:
        return

    # Mesajda https:// varsa
    if "https://" in message.content:
        # Botun banlama yetkisi var mı?
        if message.guild.me.guild_permissions.ban_members:
            try:
                await message.guild.ban(
                    message.author,
                    reason="Mesajda bağlantı bulundu"
                )
                await message.channel.send(
                    f"{message.author.name} bağlantı gönderdiği için banlandı."
                )
            except discord.Forbidden:
                await message.channel.send(
                    "Kullanıcıyı banlayamadım. Botun yetkilerini kontrol edin."
                )

    # Diğer ! komutlarının çalışmaya devam etmesi için
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        await channel.send(f"Hoşgeldin umarım iyisindir., {member.mention}!")

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanızı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

bot.run(token)
