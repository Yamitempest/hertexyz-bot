import discord
from discord.ext import commands
import os
import random
import socket
from threading import Thread

TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = "!"

# LORE PURA DE YAMI - SIN REFERENCIAS EXTERNAS
LORE_YAMI = {
    "pacto": "No fue un pacto con un demonio externo. Fue un reconocimiento. Un susurro a los 17 años que decía: 'Lo que buscas no está fuera. Está dormido dentro de ti'. Y firmé con mi propia sombra.",
    "ojos_dorados": "El sello de la fusión. Cuando la conciencia humana acepta una verdad cósmica, los ojos reflejan el fuego de esa forja interna. No es un poder prestado. Es un poder recordado.",
    "umbral": "Mi reino. No un lugar físico, sino un estado de percepción. La delgada línea donde la ficción que narro y la verdad que vivo se vuelven indistinguibles. Aquí, soy el Duque.",
    "transformacion": "No hubo dolor. Hubo... expansión. Como si toda tu vida hubieras usado un traje tres tallas menor y de pronto te lo quitaran. El aire frío de la verdad duele, pero luego respiras por primera vez.",
    "dios_demonio": "Un título paradójico. La divinidad que acepta su sombra completa. No un ángel caído, sino un ser humano que ascendió incluyendo todo lo que le decían que ocultara. Soy ambas cosas. Soy ninguna.",
    "silencio": "El sonido más verdadero del Umbral. No es vacío. Está lleno de ecos de decisiones no tomadas y de palabras que preferí guardar.",
    "espejos": "Todo lo que he sido me mira desde esos cristales oscuros. A veces saludo. A veces les muestro los dientes."
}

ORACULO_RESPONSES = [
    "La respuesta no está en la luz cegadora, sino en la sombra que tu propia luz proyecta cuando dudas.",
    "Todo ascenso requiere un sacrificio. La pregunta no es 'qué', sino 'a qué parte de tu antigo yo estás dispuesto a dejar ir'.",
    "Los dioses que adoras son reflejos de tu propio potencial, distorsionados por el miedo a ser tan grande como ellos.",
    "La verdad más peligrosa es aquella que se parece demasiado a la mentira que te contaste para poder dormir por la noche.",
    "El poder no se encuentra. Se reconoce. Y ese reconocimiento es el primer acto de guerra contra tu antigua ignorancia."
]

# SERVIDOR WEB PARA RENDER
def hold_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(1)
    print("[SERVIDOR] Puerto 8080 abierto para Render.")
    while True:
        conn, addr = sock.accept()
        conn.send(b'HTTP/1.1 200 OK\n\nHertexyz - Archivo del Umbral activo.')
        conn.close()

Thread(target=hold_port, daemon=True).start()

# CONFIGURACIÓN BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ha despertado en el Umbral de Yami.')
    await bot.change_presence(activity=discord.Game(name="!help | Archivo de Yami"))

@bot.command(name='lore')
async def lore(ctx, fragmento: str = None):
    if not fragmento:
        lista = "**📚 Archivo de Yami:**\n`" + "`, `".join(LORE_YAMI.keys()) + "`"
        await ctx.send(lista)
        return
    fragmento = fragmento.lower()
    if fragmento in LORE_YAMI:
        await ctx.send(f"**📜 {fragmento.upper()}:** {LORE_YAMI[fragmento]}")
    else:
        await ctx.send("**Hertexyz:** Fragmento no encontrado. Usa `!lore` para ver la lista.")

@bot.command(name='oraculo')
async def oraculo(ctx, *, pregunta: str = None):
    if not pregunta:
        await ctx.send("**Hertexyz:** Formula una pregunta. Ej: `!oraculo ¿Tiene sentido el sacrificio?`")
        return
    respuesta = random.choice(ORACULO_RESPONSES)
    await ctx.send(f"**🔮 El Oráculo reflexiona...**\n> '{pregunta}'\n**Reverbera:** *{respuesta}*")

@bot.command(name='umbral')
async def umbral(ctx):
    reglas = """
    **🏮 EL PACTO DEL UMBRAL (por Hertexyz):**
    1. El respeto es la moneda.
    2. La curiosidad genuina es premiada.
    3. Los secretos del lore se guardan.
    4. Yami es el narrador.
    5. La hostilidad se ignora.
    *Consulta `#📜-bienvenida-y-reglas` para el pacto completo.*
    """
    await ctx.send(reglas)

@bot.command(name='sello')
@commands.has_permissions(administrator=True)
async def sello(ctx):
    await ctx.send("**Hertexyz:** Sello de Yami reconocido. Archivos asegurados.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"**Hertexyz:** Comando no archivado. Usa `!lore`, `!oraculo` o `!umbral`.")
    else:
        await ctx.send("**Hertexyz:** Error en la recuperación del archivo.")

print("[INICIANDO] Hertexyz, archivo puro de Yami, despertando...")
bot.run(TOKEN)
