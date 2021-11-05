import sqlite3

class DaoFactory:
	def __init__(self):
		self.con = sqlite3.connect('finder.db')
		self.cur = self.con.cursor()
		self.cur.execute('''SELECT count(*) from sqlite_master
								WHERE type='table' AND name='expeditions' ''')
		rows = self.cur.fetchall()
		if not rows[0][0]:
			self.__init_tables_expeditions()


	def __init_tables_expeditions(self):
		self.cur.execute('''CREATE TABLE IF NOT EXISTS groups
               (guildID str, authorID str, name text, level int, number_p int, departure text)''')
		self.cur.execute('''CREATE TABLE IF NOT EXISTS guild
               (guildID str, ownerID str, channelID str, categoryID str)''')
		# # Init Expeditions
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('Amrine Excavation', 25, 5, 'Windsward')''')
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('Starstone Barrows', 35, 5, 'Everfall')''')
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('The Depths', 45, 5, 'Restless Shore')''')
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('Dynasty Shipyard', 55, 5, 'Ebonscale Reach')''')
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('Garden of Genesis', 60, 5, 'Edengrove')''')
		# self.cur.execute('''INSERT INTO expeditions
		# 			VALUES('Lazarus Instrumentality', 60, 5, 'Reekwater')''')
		self.con.commit()


	def set_groups_table(self, guildID:str, authorID:str, name:str, level:int, nb_player:int, departure:str):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND authorID=?", (guildID, authorID))
		res = self.cur.fetchone()
		if res is None:
			print('Create')
			self.cur.execute("INSERT INTO groups VALUES(?, ?, ?, ?, ?, ?)", \
							(guildID, authorID, name, level, nb_player, departure))
			self.con.commit()
		else:
			raise Exception('User find always groups')

	def set_guild_table(self, guildID:str, ownerID:str, channelID:str, categoryID:str):
		self.cur.execute("SELECT * FROM guild WHERE guildID=? AND ownerID=?", (guildID, ownerID))
		res = self.cur.fetchone()
		if res is None:
			print('create')
			self.cur.execute("INSERT INTO guild VALUES(?, ?, ?, ?)", \
					(guildID, ownerID, channelID, categoryID))
		else:
			print('Update')
			self.cur.execute('''UPDATE guild SET guildID=?, ownerID=?,
								channelID=?, categoryID=?''', \
					(guildID, ownerID, channelID, categoryID))
		self.con.commit()

	# def __del__(self):
	# 	self.cur.close()
