import discord
from discord.ext import commands
import os
import random
import socket
from threading import Thread

# ========== CONFIGURACIÓN ==========
TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = "!"

# ========== LORE DE YAMI ==========
LORE_YAMI = {
    "pacto": "No fue un pacto con un demonio externo. Fue un reconocimiento. Un susurro a los 17 años que decía: 'Lo que buscas no está fuera. Está dormido dentro de ti'. Y firmé con mi propia sombra.",
    "ojos_dorados": "El sello de la fusión. Cuando la conciencia humana acepta una verdad cósmica, los ojos reflejan el fuego de esa forja interna. No es un poder prestado. Es un poder recordado.",
    "umbral": "Mi reino. No un lugar físico, sino un estado de percepción. La delgada línea donde la ficción que narro y la verdad que vivo se vuelven indistinguibles. Aquí, soy el Duque.",
    "transformacion": "No hubo dolor. Hubo... expansión. Como si toda tu vida hubieras usado un traje tres tallas menor y de pronto te lo quitaran. El aire frío de la verdad duele, pero luego respiras por primera vez.",
    "dios_demonio": "Un título paradójico. La divinidad que acepta su sombra completa. No un ángel caído, sino un ser humano que ascendió incluyendo todo lo que le decían que ocultara. Soy ambas cosas. Soy ninguna."
}

# ========== ECOS DE OTROS MUNDOS ==========
ECOS_OTROS_MUNDOS = {
    "skarlett": [
        "(Eco distante, voz metálica y fría) 'La fuerza no se pide. Se toma. El universo es una cadena alimenticia. Elige tu rol.'",
        "(Eco distante) 'Los sentimientos son grietas en la armadura. Sella todas.'",
        "(Eco distante) 'Skarlett no es un nombre. Es una declaración de guerra contra la debilidad.'"
    ],
    "sucuchan": [
        "(Eco caótico, risa de campanillas) '¡Las reglas son aburrididas! ¿Y si rompemos la cuarta, quinta y sexta pared a la vez?'",
        "(Eco caótico) 'Dicen que soy un virus de alegría en un sistema serio. ¡Qué cumplido tan delicioso!'",
        "(Eco caótico) 'Sucu-chan está en todos lados y en ninguno. Como un meme imborrable. ¡Saludos desde el vacío!'"
    ]
}

# ========== ORÁCULO ==========
ORACULO_RESPONSES = [
    "La respuesta no está en la luz cegadora, sino en la sombra que tu propia luz proyecta cuando dudas.",
    "Todo ascenso requiere un sacrificio. La pregunta no es 'qué', sino 'a qué parte de tu antigo yo estás dispuesto a dejar ir'.",
    "Los dioses que adoras son reflejos de tu propio potencial, distorsionados por el miedo a ser tan grande como ellos.",
    "La verdad más peligrosa es aquella que se parece demasiado a la mentira que te contaste para poder dormir por la noche."
]

# ========== FUNCIÓN PARA MANTENER PUERTO ABIERTO (RENDER) ==========
def hold_port():
    """Mantiene un puerto abierto para que Render no se queje."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(1)
    print("[PUERTO] Puerto 8080 abierto para Render.")
    while True:
        conn, addr = sock.accept()
        conn.send(b'HTTP/1.1 200 OK\n\nHertexyz - Archivo del Umbral activo.')
        conn.close()

# Iniciar el hilo del puerto
port_thread = Thread(target=hold_port, daemon=True)
port_thread.start()

# ========== CONFIGURACIÓN DEL BOT ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ========== EVENTOS ==========
@bot.event
async def on_ready():
    print(f'{bot.user} ha despertado en el Umbral de Yami.')
    await bot.change_presence(activity=discord.Game(name="!help | Archivo de Yami"))

# ========== COMANDOS ==========
@bot.command(name='lore')
async def lore(ctx, fragmento: str = None):
    if not fragmento:
        lista = "**📚 Archivo de Yami - Índice:**\n`" + "`, `".join(LORE_YAMI.keys()) + "`"
        await ctx.send(lista)
        return
    fragmento = fragmento.lower()
    if fragmento in LORE_YAMI:
        await ctx.send(f"**📜 {fragmento.upper()}:** {LORE_YAMI[fragmento]}")
    else:
        await ctx.send("**Hertexyz:** Fragmento no encontrado. Usa `!lore` para ver el índice.")

@bot.command(name='eco')
async def eco(ctx, mundo: str = None):
    if not mundo or mundo.lower() not in ["skarlett", "sucuchan"]:
        await ctx.send("**Hertexyz:** Especifica un mundo: `skarlett` o `sucuchan`. Ej: `!eco skarlett`")
        return
    mundo = mundo.lower()
    mensaje = random.choice(ECOS_OTROS_MUNDOS[mundo])
    await ctx.send(f"**🔊 Hertexyz reproduce un eco...**\n> {mensaje}\n*Nota: Realidad paralela, no conexión.*")

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
        await ctx.send(f"**Hertexyz:** Comando no archivado. Prueba con `!lore`, `!eco`, `!oraculo` o `!umbral`.")
    else:
        await ctx.send("**Hertexyz:** Error en la recuperación del archivo.")

# ========== INICIAR BOT ==========
print("[INICIANDO] Hertexyz despertando...")
bot.run(TOKEN)
