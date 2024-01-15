import discord
from discord.ext import commands
import os
import requests
import datetime
import re

# functions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="vipid", description="Wish the web has Vips while waitting")
@commands.cooldown(1, 10, commands.BucketType.user)

async def vipid(interaction: discord.Interaction, game_id: str):
    await interaction.response.defer()
    try:
        if "games/" in game_id:
            game_id = game_id.split("/games/")[1].split("/")[0]
        else:
            game_id = game_id

        url = f'https://rbxservers.xyz/games/{game_id}'
        response = requests.get(url)

        if response.status_code == 200:
            content = response.content.decode('utf-8')  
            matches = re.finditer(r'/servers/', content)

            vip_links = []  

            if matches:
                for match in matches:
                    start_index = match.end() 
                    end_index = content.find('"', start_index) 
                    if end_index != -1:
                        server_id = content[start_index:end_index]
                        server_url = f'https://rbxservers.xyz/servers/{server_id}'

                        server_response = requests.get(server_url)
                        if server_response.status_code == 200:
                            server_content = server_response.content.decode('utf-8')
                            vip_matches = re.finditer(r'https://www\.roblox\.com/\S+', server_content)
                            if vip_matches:
                                for vip_match in vip_matches:
                                    vip_link = vip_match.group()
                                    if vip_link.endswith('"'):
                                        vip_link = vip_link[:-1]
                                    vip_links.append(vip_link) 
                            else:
                                await interaction.response.send_message('No Vips Found')
                        else:
                            await interaction.response.send_message('No Vips Found')                                
            if vip_links:
                embed = discord.Embed(title=f"Vip Servers Found in rbxservers.xyz web", description='```' + '\n'.join(vip_links) + '```' + '\n', color=7419530)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='Robo (ty reblue)',icon_url="https://imgur.com/EpLwRun")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.response.send_message('No Vips Found')
        else:
            await interaction.response.send_message('Failed to fetch content for the specified game ID')
    except Exception as a:
        print(a)
        await interaction.followup.send("No Vips Found or u give invalid id")

@vipid.error
async def id_error(interaction: discord.Interaction, error):
    await interaction.response.defer()
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='Robo is in love with Single',icon_url="https://imgur.com/EpLwRun")
        await interaction.followup.send(embed=em)


token = os.environ.get("TOKEN")
bot.run(token)