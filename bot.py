import os
import urllib.request, json

import pokebase
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

effectiveness = {
    'normal': 1,
    'fire': 1,
    'water': 1,
    'grass': 1,
    'electric': 1,
    'ice': 1,
    'fighting': 1,
    'poison': 1,
    'ground': 1,
    'flying': 1,
    'psychic': 1,
    'bug': 1,
    'rock': 1,
    'ghost': 1,
    'dark': 1,
    'dragon': 1,
    'steel': 1,
    'fairy': 1
}

def calculate_effectiveness(multiplier, value):
    if effectiveness[multiplier.name] != 0:
        effectiveness[multiplier.name] = effectiveness[multiplier.name] * value
    else:
        effectiveness[multiplier.name] = effectiveness[multiplier.name] + value
        
def process_command(pokemon):
    pokemon = pokebase.pokemon(pokemon)
    for type in pokemon.types:
        api_type = pokebase.type_(type.type.name).damage_relations
        for calculated_type in api_type.double_damage_from:
            calculate_effectiveness(calculated_type, 2)
        for calculated_type in api_type.half_damage_from:
            calculate_effectiveness(calculated_type, 0.5)
        for calculated_type in api_type.no_damage_from:
            calculate_effectiveness(calculated_type, 0)
    
    strong = {}
    weak = {}
    for type in effectiveness:
        if effectiveness[type] > 1:
           strong[type] = effectiveness[type]
        elif effectiveness[type] < 1:
            weak[type] = effectiveness[type]
            
    message = 'Strong against {}:\n'.format(pokemon)
    for type in strong:
        message = message + '{} - {}\n'.format(type, strong[type])
        
    message = message + 'Weak against {}:\n'.format(pokemon)
    for type in weak:
        message = message + '{} - {}\n'.format(type, weak[type])
    
    return message
    

@tree.command(name = "peff", description = "Pokemon Type Effectiveness")
async def first_command(interaction, pokemon: str):
    await interaction.response.send_message("Calculating...")
    result = process_command(pokemon)
    await interaction.edit_original_response(content=result)
    
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

client.run(TOKEN)