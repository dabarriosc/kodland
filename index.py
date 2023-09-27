import discord
import youtube_dl 
import os
from discord.ext import commands
from discord.utils import get
from urllib import parse,request   
import re

bot = commands.Bot(command_prefix='-',intents=discord.Intents.all())

# Permite ver el estado del servidor 
@bot.event
async def on_ready():
    print(f"I am{bot.user}")


# Devuelve respuesta del bot en caso de que este conectado
@bot.command()
async def ping(ctx):
    await ctx.send("Hola amigo en que puedo ayudarte")


# Permite  buscar un video directamente desde discor con un palabra clave
@bot.command()
async def video(ctx,*,search):
    query_string = parse.urlencode({"search_query": search} )
    html_content = request.urlopen("http://www.youtube.com/results?"+ query_string)
    search_results=re.findall('watch\?v=(.{11})',html_content.read().decode('utf-8'))

    print(search_results)
    await ctx.send("http://www.youtube.com/watch/?v="+ search_results[0])


# Permite conectar el bot al canal de voz
@bot.command(pass_context = True)
async def conectar(ctx):
    author = ctx.author
    if not author.voice:
        await ctx.send("No estás en ningún canal de voz")
        return

    canal = author.voice.channel
    voice = ctx.voice_client

    if voice and voice.is_connected():
        await voice.move_to(canal)
    else:
        voice = await canal.connect()

# Desconecta al bot del canal de voz
@bot.command(pass_context =True)
async def desconectar(ctx):
    author = ctx.author
    canal = author.voice.channel
    
    if canal is not None:
        await canal.disconnect() 
    else:
        await ctx.send("No estás en un canal de voz.")


#Permite reproducir musica atravez de la libreria  youtube_dl
@bot.command(pass_context = True)
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel

    if not voice_channel:
        await ctx.send("Debes estar en un canal de voz para usar este comando.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(url2))
        await ctx.send(f'Reproduciendo: {info["title"]}')


# Pausa la reproduccion de musica de musica
@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Reproducción detenida.")
    

bot.run("MTE1NDk4Njg2NTExNjU5ODI3Mw.GtoUOX.opI2Sr4uQrYZQChLyI_bfZ5p0QBJLczttQWyRg")
