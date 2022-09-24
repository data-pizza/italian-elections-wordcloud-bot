# Script per la creazione del bot Discord tramite Pycord

import discord
import os
import wordbackend
from io import BytesIO #Per inviare le immagini generate senza salvarle su disco
import tweepy

#from dotenv import load_dotenv
#load_dotenv()


bot = discord.Bot(debug_guilds=["950060009897754685"])

@bot.slash_command(name="wordcloud", description = "Inserisci il nome utente di un politico italiano per generare la sua WordCloud (dati da Twitter)")

@discord.option(
    "username",
    str,
    description="Inserisci l'username twitter del politico"
)
@discord.option(
    "ntweets",
    int,
    description="Inserisci il numero di tweets di cui il Word Cloud deve tenere conto (min 10, max 100)"
)

async def sendwordcloud(ctx, username):
    
    await ctx.defer()
    try:
        res = wordbackend.wordcloud(username)

    except tweepy.errors.NotFound:
        await ctx.followup.send(f"{username} non esiste, riprova con un altro username.")
    
    else:
        
        image = res[0].to_image()
        ntweets = res[1]
        bytes = BytesIO()
        image.save(bytes, format = "PNG")
        bytes.seek(0)
        final = discord.File(bytes,filename="image.png")
        text = f"*Word Cloud di **{username}** basato sui suoi ultimi **{ntweets}** tweets dall'inizio della campagna elettorale:*"
        await ctx.followup.send(content = text, file = final)
    

        



bot.run(os.getenv('TOKEN'))
