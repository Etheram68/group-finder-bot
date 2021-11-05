import discord
from discord import channel
from discord import client
from discord.ext import commands
import asyncio
from src.dao.classifier import DaoFactory


class Search(commands.Cog):
	def __init__(self, bot, db):
		print("Init Cog")
		self.db = db
		self.bot = bot


	@commands.command()
	async def __dm_user(ctx, member: discord.Member):
		await ctx.author.send("** You have 60 second to answer each Questions! **")
		await ctx.author.send("** Enter name of activity: (e.g  `Amrine Excavation`) **")


	@commands.command()
	async def help(self, ctx):
		embed = discord.Embed(title="Help", description="",color=0x7289da)
		embed.set_author(name=f"{ctx.guild.me.display_name}", icon_url=f"{ctx.guild.me.avatar_url}")
		embed.add_field(name=f'**Commands**', value=f'**Create new find group:**\n\n`!find`\n\n------------\n\n', inline='false')
		await ctx.channel.send(embed=embed)


	@commands.command(name="del")
	async def delete(self, ctx, number: int):
		messages = await ctx.channel.history(limit=number+1).flatten()
		for each_message in messages:
			await each_message.delete()


	@commands.command(name="find")
	async def find_group(self, ctx):
		guildID = ctx.guild.id
		authorID = ctx.author.id
		def check(m):
			return m.author.dm_channel == ctx.author.dm_channel
		messages = await ctx.channel.history(limit=1).flatten()
		for each_message in messages:
			await each_message.delete()
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
				await ctx.channel.send('Took too long to answer!')
			else:
				await ctx.author.send("** Enter number of players for this activity: (e.g  `5`) **")
				try:
					number_player = await self.bot.wait_for('message',check=check, timeout=60.0)
					number_player = int(number_player.content)
				except asyncio.TimeoutError:
					await ctx.channel.send('Took too long to answer!')
				else:
					await ctx.author.send("** Enter departure for this activity: (e.g  `18h30`) **")
					try:
						departure = await self.bot.wait_for('message',check=check, timeout=60.0)
						departure = departure.content
					except asyncio.TimeoutError:
						await ctx.channel.send('Took too long to answer!')
					else:
						try:
							self.db.set_groups_table(guildID, authorID, name_activity, level_activity, number_player, departure)
						except ValueError:
							await ctx.author.send("** You find a group destruct this and restart **")

		print(f"Name: {name_activity}, level: {level_activity}, nbPlayer: {number_player}, departure: {departure}")


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
