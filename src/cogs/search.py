import discord
from discord import channel
from discord import client
from discord.ext import commands
import asyncio
from src.dao.classifier import DaoFactory


class Search(commands.Cog):
	def __init__(self, bot, db):
		print("Init Cog")
		self.__private_emojis = ["\N{SHIELD}", "\N{SPARKLING HEART}", "\N{CROSSED SWORDS}"]
		self.__private_emojis_ut = ['🛡', '💖', '⚔']
		self.db = db
		self.bot = bot


	async def __create_view_embed(self, name, level, nb_player, departure, role, username):
		i = 3
		embed = discord.Embed(title='Group Search', description=f"{name}", color=0xff0000)
		embed.add_field(name="level min", value=f"{level}", inline=True)
		embed.add_field(name="Departure", value=f"{departure}", inline=True)
		embed.add_field(name="Tank: \N{SHIELD}", value=f"{username}" if role == 'tank' else "-", inline=False)
		embed.add_field(name="Heal: \N{SPARKLING HEART}", value=f"{username}" if role == 'heal' else "-", inline=False)
		embed.add_field(name="Dps \N{CROSSED SWORDS}", value=f"{username}" if role == 'dps' else "-", inline=False)
		while i < nb_player:
			embed.add_field(name="Dps \N{CROSSED SWORDS}", value="-", inline=False)
			i += 1
		return embed


	@commands.command()
	async def help(self, ctx):
		embed = discord.Embed(title="Help", description="",color=0x7289da)
		embed.set_author(name=f"{ctx.guild.me.display_name}", icon_url=f"{ctx.guild.me.avatar_url}")
		embed.add_field(name=f'**Commands**', value=f'**Create new find group:**\n\n`!find`\n\n------------\n\n'
							 f'**Remove old find group:**\n\n`!delete`\n\n', inline='false')
		await ctx.channel.send(embed=embed)


	@commands.command(name="del")
	async def delete(self, ctx, number: int):
		messages = await ctx.channel.history(limit=number+1).flatten()
		for each_message in messages:
			await each_message.delete()


	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		print(f"{reaction.message.id}, {user.name}, {reaction.message.guild.id}")
		guildID = reaction.message.guild.id
		msgID = reaction.message.id
		msg =  reaction.message
		if user.id != self.bot.user.id and reaction.emoji in self.__private_emojis_ut:
			if self.db.check_if_mess_exist(guildID, msgID):
				new_embed = None
				for e in msg.embeds:
					new_embed = e.to_dict()
					print(e.to_dict())
					break
				if reaction.emoji == '🛡':
					for e in new_embed['fields']:
						if e['name']  == 'Tank: 🛡' and e['value'] == '-':
							e['value'] = user.name
							break
				elif reaction.emoji == '💖':
					for e in new_embed['fields']:
						if e['name'] == 'Heal: 💖' and e['value'] == '-':
							e['value'] = user.name
							break
				elif reaction.emoji == '⚔':
					for e in new_embed['fields']:
						if e['name'] == 'Dps ⚔' and e['value'] == '-':
							e['value'] = user.name
							break

				await msg.edit(embed=discord.Embed.from_dict(new_embed))
				print(f"{reaction}, {user}")


	@commands.command(name="delete")
	async def drop_group(self, ctx):
		guildID = ctx.guild.id
		authorID = ctx.author.id
		messages = await ctx.channel.history(limit=1).flatten()
		for each_message in messages:
			await each_message.delete()
		id_mess = self.db.get_id_mess(guildID, authorID)
		channel_id = self.db.get_channel_id(guildID)
		chanel = self.bot.get_channel(int(channel_id))
		msg = await chanel.fetch_message(id_mess)
		self.db.drop_groups_author(guildID, authorID)
		await msg.delete()
		await ctx.author.send("** Last find group is removed **")


	@commands.command(name="find")
	async def find_group(self, ctx):
		guildID = ctx.guild.id
		authorID = ctx.author.id
		def check(m):
			return m.author.dm_channel == ctx.author.dm_channel
		messages = await ctx.channel.history(limit=1).flatten()
		for each_message in messages:
			await each_message.delete()
		if not self.db.get_groups_author(guildID, authorID):
			await ctx.author.send("** You have 60 second to answer each Questions! **")
			await ctx.author.send("** Enter name of activity: (e.g  `Amrine Excavation`) **")
			try:
				name_activity = await self.bot.wait_for('message',check=check, timeout=60.0)
				name_activity = name_activity.content
			except asyncio.TimeoutError:
				await ctx.channel.send('Took too long to answer!')
			else:
				await ctx.author.send("** Enter level min for play activity: (e.g  `25`) **")
				try:
					level_activity = await self.bot.wait_for('message',check=check, timeout=60.0)
					level_activity = int(level_activity.content)
				except asyncio.TimeoutError:
					await ctx.author.send('Took too long to answer!')
				else:
					await ctx.author.send("** Enter number of players for this activity: (e.g  `5`) **")
					try:
						number_player = await self.bot.wait_for('message',check=check, timeout=60.0)
						number_player = int(number_player.content)
					except asyncio.TimeoutError:
						await ctx.author.send('Took too long to answer!')
					else:
						await ctx.author.send("** Enter departure for this activity: (e.g  `18h30`) **")
						try:
							departure = await self.bot.wait_for('message',check=check, timeout=60.0)
							departure = departure.content
						except asyncio.TimeoutError:
							await ctx.author.send('Took too long to answer!')
						else:
							mess = await ctx.author.send("** Choose your role: (e.g `dps/tank/heal`) **")
							try:
								role = await self.bot.wait_for('message',check=check, timeout=60.0)
								role = role.content
							except asyncio.TimeoutError:
								await ctx.author.send('Took too long to answer!')
							else:
								embed = await self.__create_view_embed(name_activity, level_activity, \
											number_player, departure, role.lower(), ctx.author.name)
								channel_id = self.db.get_channel_id(guildID)
								chanel = self.bot.get_channel(int(channel_id))
								mess = await chanel.send(embed=embed)
								for emoji in self.__private_emojis:
									await mess.add_reaction(emoji)
								self.db.set_groups_table(guildID, authorID, name_activity, level_activity, number_player, departure, mess.id)
								await ctx.author.send("** find group is created **")
		else:
			await ctx.author.send("** You find a group, please delete this and restart **")


	@commands.command(name="setup")
	@commands.has_permissions(administrator=True)
	async def setup(self, ctx):
		guildID = ctx.guild.id
		ownerID = ctx.author.id
		def check(m):
			return m.author.id == ctx.author.id
		await ctx.channel.send("** You have 60 second to answer each Questions! **")
		await ctx.channel.send("** Enter id of category for create guild channel? **")
		try:
			cat_id = await self.bot.wait_for('message', check=check, timeout=60.0)
			cat_guild = discord.utils.get(ctx.guild.categories, id=int(cat_id.content))
			if not cat_guild:
				raise Exception("Guild id not found")
		except asyncio.TimeoutError:
			await ctx.channel.send('Took too long to answer!')
		except:
			await ctx.channel.send("Error: You didn't enter the id properly.\nUse `!setup` again!")
		else:
			await ctx.channel.send("** Enter the name of the text channel: (e.g Find player)**")
			try:
				channel = await self.bot.wait_for('message', check=check, timeout=60.0)
			except asyncio.TimeoutError:
				await ctx.channel.send('Took too long to answer!')
			else:
				try:
					channel = await cat_guild.create_text_channel(name=channel.content)
					self.db.set_guild_table(guildID, ownerID, channel.id, cat_id.content)
				except:
					await ctx.channel.send("You didn't enter the names properly.\nUse `!setup` again!")
				else:
					await ctx.channel.send(f"** Text Channel `{channel}` created with success**")


def setup(bot):
	db = DaoFactory()
	bot.add_cog(Search(bot, db))
