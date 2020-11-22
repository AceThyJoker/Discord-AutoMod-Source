import discord, random, aiohttp, asyncio
import praw
import pendulum
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord.ext.commands import *
from colorama import Fore as C
from colorama import Style as S
from datetime import datetime

#Put your bot token here
token ="YOUR BOT TOKEN"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name= "!help | AntiRaid"))
  print("Bot is on")

bot.remove_command("help")

#Help Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
	    title='Commands', description=None, colour=discord.Colour.blue())
	embed.add_field(
	    name='!modhelp', value='Shows The Moderation Help!!', inline=False)
	embed.add_field(
	    name='!funhelp', value='Shows All The Fun Commands!', inline=False)
	embed.set_footer(text='Terminal Bot | Created By AceTheJoker')
	await ctx.send(embed=embed)


#Moderation Stuff


#Kick-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send('Please input a user.')
        else:
            await channel.send(":boot: Terminal has kicked **{}**".format(member.name))
            await member.kick()
    else:
        await channel.send('You lack the required permission to perform this action *{}*!')

#Fact Command-------------------------------------------------------------------------------------------------#Currently Broken#
    @bot.command()
    async def fact(pass_context=True):
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                fact = r['text']
                embed = discord.Embed(title=f'Random Fact', colour=ctx.author.colour, timestamp=ctx.message.created_at)

                embed.add_field(name='***Fun Fact***', value=fact, inline=False)
                await ctx.send(embed=embed)

#Ban-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send('Please input a user.')
        else:
            await channel.send("Get banned **{}**.".format(member.name))
            await member.ban()
    else:
        await channel.send('You lack the required permission to perform this action *{}*!')

#Unban-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

	if (user.name, user.discriminator) == (member_name, member_discriminator):
		await ctx.guild.unban(user)
		await ctx.send(f"{user} has been unbanned sucessfully")
		return


#Mute Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def mute(ctx, member: discord.Member):
	role = discord.utils.get(ctx.guild.roles, name='Muted')
	await member.remove_roles("Members")
	await member.add_roles("Muted")
	await ctx.send("**{user}** Was Muted")

#Unmute Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def unmute(ctx, member: discord.Member):
	role = discord.utils.get(ctx.guild.roles, name='Members')
	await member.remove_roles("Muted")
	await member.add_roles("Members")

	await ctx.send("**{user}** Was Un Muted")


#Purge Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
	await ctx.channel.purge(limit=limit)
	await ctx.send('Cleared by {}'.format(ctx.author.mention))
	await ctx.message.delete()
	
#Invite Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def invite(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.add_field(name="Invite me!: ", value="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=779289293662453770&permissions=8&scope=bot)")
    await channel.send(embed=embed)

#Whois Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(aliases=['userinfo'])
async def whois(ctx, member: discord.Member):
    roles = [role for role in member.roles]

    embed=discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Member Name:", value=member.display_name)
    embed.add_field(name="Created Account At:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role:", value=member.top_role.mention)
    embed.add_field(name="Bot", value=member.bot)
    await ctx.send(embed=embed)

#Blacklisted Links----------------------------------------------------------------------------------------------#Currently Working#
blacklist = ['.com', '.co.uk', '.gg']  # you could put .com, .co.uk etc

#Blacklisted Command
@bot.event
async def on_message(message):
	try:
		for word in blacklist:
			if word in message.content:
				await message.delete()
				await message.channel.send(
				    f'{message.author.mention} you cannot say that.)')
				break

	except:
		pass

	await bot.process_commands(message)

#Moderation Help Page------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def modhelp(ctx):

	await ctx.message.delete()
	embed = discord.Embed(
	    title='Moderation',
	    description=None,
	    colour=discord.Colour.blue())
	embed.add_field(
	    name=' `!mute` ', value='MutesThe Mentioned User!!', inline=False)
	embed.add_field(
	    name=' `!kick` ', value='Kicks the user that is mentioned!', inline=False)
	embed.add_field(
	    name=' `!ban` ', value='Bans the mentioned user forever,', inline=False)
	embed.add_field(
	    name=' `!unban` ', value='Unbans the users ID or mentioned,', inline=False)
	embed.add_field(
	    name=' `!lockdown` ',
	    value=
	    'Makes the channel you executed the command in, close so nobody can type',
	    inline=False)
	embed.add_field(
	    name=' `!whois @mention` ',
	    value=
	    'Info on the user',
	    inline=False)
	embed.add_field(
	    name=' `!unmute` ', value='Unmutes The Mentioned User!!', inline=False)
	embed.add_field(
	    name=' `Anti-Link` ', value='Anti Link Is Always on!!', inline=False)
	embed.set_footer(text='Terminal Bot')
	await ctx.send(embed=embed)


#fun stuff

#Pat Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def pat(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/pat")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)

#Feed Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def feed(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/feed")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)

#Penis size Command-------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def pp(ctx, member: discord.Member):
    sizes = ['8D',
                '8=D',
                '8==D',
                '8===D',
                '8====D',  
                '8=====D',
                '8======D', 
                '8=======D',
                '8========D',
                '8=========D',
                '8==========D',
                '8===========D',
                '8============D',
                '8=============D',
                '8==============D',
                '8===============D',
                '8================D']
    await ctx.send(f"{member.mention} has this dick size: {random.choice(sizes)}")

#Tickle Command-------------------------------------------------------------------------------------------------#Currently Broken#
@bot.command()
async def tickle(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/tickle")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)

#Slap Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def slap(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/slap")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)

#Hug Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command()
async def hug(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/hug")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)


#Hack Command------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def hack(ctx, member:discord.Member = None):
    if not member:
        await ctx.send("Please specify a member")
        return

    passwords=['imnothackedlmao','sendnoodles63','ilovenoodles','icantcode','christianmicraft','server','icantspell','hackedlmao','WOWTONIGHT','69'] 
    fakeips=['154.2345.24.743','255.255. 255.0','356.653.56','101.12.8.6053','255.255. 255.0']

    m = await ctx.send(f"**Hacking: {member}** 0%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 19%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 34%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 55%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 67%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 84%")
    await asyncio.sleep(3)

    await m.edit(content=f"**Hacking: {member}** 99%")
    await asyncio.sleep(3)

    await m.edit(embed=f"**Hacking: {member}** 100%")
    await asyncio.sleep(3)
    
    await ctx.send("**Sold content**")
    await ctx.send("*IP address is: 124.234.232*")
    await ctx.send("**")
    
    await bot.delete_message(m)

    embed=discord.Embed(title=f"{member} info ", description=f"*Email `{member}@gmail.com` Password `{random.choice(passwords)}`  IP `{random.choice(fakeips)}`*", color=0x2f3136)
    embed.set_footer(text="So Hacker.")
    await ctx.send(embed=embed)
 
#Smerk Command-------------------------------------------------------------------------------------------------#Currently Broken#
@bot.command()
async def smerk(ctx, user: discord.Member):
	await ctx.message.delete()
	r = requests.get("https://nekos.life/api/v2/img/smug")
	res = r.json()
	em = discord.Embed(description=user.mention)
	em.set_image(url=res['url'])
	await ctx.send(embed=em)


reddit = praw.Reddit(
    client_id='MpEsS61a-ZTQ5A',
    client_secret='vwpmt5WylGnlNiOY3kv9wupuy3s',
    user_agent='No u')

#Meme Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def meme(ctx):
  memes_submissions = reddit.subreddit('memes').hot()
  post_to_pick = random.randint(1, 100)
  for i in range(0, post_to_pick):
    submission = next(x for x in memes_submissions if not x.stickied)
  embed = discord.Embed(color=0x00008b)
  embed.set_image(url=submission.url)
  await ctx.send(embed=embed)

#Embed Command-------------------------------------------------------------------------------------------------#Currently Working#
@bot.command(pass_context=True)
async def embed(ctx, *, text):
	await ctx.message.delete()
	emb = discord.Embed(description=f"{text}", color=0x00008b)
	emb.set_footer(text="Terminal Bot")
	await ctx.send(embed=emb)

#Translator Command----------------------------------------------------------------------------------------------#Currently Broken#
@bot.command()
async def translate(ctx, lang, *, message):
	await ctx.message.delete()
	try:
		translator = Translator()
		translations = translator.translate(message, dest=lang)
		await ctx.send(translations.text)
	except:
		print(
		    f"{Fore.YELLOW}[ERROR]: {Fore.CYAN}Translation unsuccesfull fore: '{message}'"
		)


#Spotify Command-----------------------------------------------------------------------------------------------#Currently Broken#
@bot.command()
async def spotify(ctx, user: discord.Member=None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            em = discord.Embed(color=activity.color)
            em.title = f'{user.name} is listening to {activity.title}'
            em.set_thumbnail(url=activity.album_cover_url)
            em.description = f"**Song Name**: {activity.title}\n**Song Artist**: {activity.artist}\n**Song Album**: {activity.album}\n**Song Length**: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
            await ctx.send(embed=em)
            break
    else:
          embed = discord.Embed(color=0xff0000)
          embed.title = f'{user.name} is not listening Spotify right now!'
          await ctx.send(embed=embed)

#Fun Help Embed-----------------------------------------------------------------------------------------------#Currently Working#         
@bot.command(pass_context=True)
async def funhelp(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
	    title='Fun',
	    description=None,
	    colour=discord.Colour.blue())
	embed.add_field(
	    name=' `!penis @mention` ', value='Shows the dick size of the user you mention!', inline=False)
	embed.add_field(
	    name=' `!hack @mention` ', value='Fake Hack!', inline=False)
	embed.add_field(
	    name=' `!spotify @mention` ', value='Shows the song of the user you mention!', inline=False)
	embed.add_field(
	    name=' `!slap @mention` ', value='Slaps The Mentioned User!!', inline=False)
	embed.add_field(
	    name=' `!pat @mention` ',
	    value='Pats the user that is mentioned!',
	    inline=False)
	embed.add_field(
	    name=' `!smerk @mention` ',
	    value='Smerks At the mentioned user forever,',
	    inline=False)
	embed.add_field(
	    name=' `!hug @mention` ',
	    value='Hugs The user That is mentioned,',
	    inline=False)
	embed.add_field(
	    name=' `!meme` ', value='Sends the most random reddit memes', inline=False)
	embed.add_field(
	    name=' `!embed` ',
	    value=
	    'Embeds the message you say, EG: !embed Hi, and it will embed your message!',
	    inline=False)
	embed.add_field(
	    name=' `!feed @mention` ',
	    value='Feeds The user That is mentioned,',
	    inline=False)
	embed.add_field(
	    name=' `!tickle @mention` ',
	    value='Tickels The user That is mentioned,',
	    inline=False)
	embed.add_field(
	    name=' `!fact` ',
	    value='Random Fact!',
	    inline=False)
	embed.set_footer(text='Terminal Bot')
	await ctx.send(embed=embed)
	
bot.run(token)
