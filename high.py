import discord
from discord.ext import commands
import re
from flask import Flask, render_template
from threading import Thread
import os
app = Flask('')
@app.route('/')
def home():
  return "bot python is online!"
def index():
  return render_template("index.html")
def run():
  app.run(host='0.0.0.0', port=8080)
def h():
  t = Thread(target=run)
  t.start()

# ตั้งค่าบอท
bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    intents=discord.Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True, 
)
h()
# ไวท์ลิสต์สมาชิก
whitelisted_members = ['highzixdev_69']

# ฟังก์ชันสำหรับการตรวจสอบลิงก์
def contains_link(message):
    link_pattern = re.compile(r'https?://\S')
    return bool(link_pattern.search(message.content))

# อีเวนท์สำหรับการตรวจสอบข้อความ
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if contains_link(message) and message.author not in whitelisted_members:
        # แบนผู้ใช้เป็นเวลา 1 สัปดาห์
        await message.author.ban(reason='จะส่งลิ้งค์หาพ่อมึงหรอ', delete_message_days=0)
        await message.channel.send(f'{message.author.mention} ** __ถูกแบนเป็นเวลา 1 สัปดาห์เนื่องจากส่งลิงค์ครับ__\n|| @everyone || **')

    await bot.process_commands(message)

# คำสั่งสำหรับการไวท์ลิสต์สมาชิก
@bot.command()
@commands.has_permissions(administrator=True)
async def whitelist(ctx, member: discord.Member):
    if member in whitelisted_members:
        await ctx.send(f'{member.mention} อยู่ในไวท์ลิสต์แล้ว')
    else:
        whitelisted_members.append(member)
        await ctx.send(f'{member.mention} ได้ถูกเพิ่มในไวท์ลิสต์')
        
@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} is ready!")
  await bot.change_presence(activity=discord.Streaming(
      name='Bot by Highzy', url='https://www.twitch.tv/example_channel'))        

bot_key = os.environ['bot']
token = bot_key
# เรียกใช้บอท
bot.run(token)
