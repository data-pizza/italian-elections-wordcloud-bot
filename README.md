# ItalianElectionsWordCloudBot ๐ 
## Un bot Discord in Python per generare word clouds dai tweets dei candidati alle prossime elezioni politiche italiane ๐ฎ๐น

Il bot รจ stato creato per il server **Datapizza Community** di **Datapizza**, la piรน grande community di Data Science italiana!๐

*Entra nel server con questo link per usare il bot!* ๐  https://discord.gg/5vvC2sYBDd

## Backend (wordbackend.py)

Il bot รจ servito dalla piattaforma Heroku. 
Inserendo l'username Twitter di un politico italiano (e non), il bot raccoglie i tweets pubblicati dal quel profilo (tramite la libreria tweepy) a partire dalla data della caduta del governo (21 Luglio 2022). 
Dopo una pulizia di base (punteggiatura, simboli e stop words), tramite la libreria python Wordcloud, genera una nuvola di parole basate sui tweets. 

## Integrazione su Discord (bot.py)
Per la creazione del bot รจ stata utilizzata la libreria python Pycord.

# Made by Datapizza Team ๐ (https://datapizza.super.site/)
