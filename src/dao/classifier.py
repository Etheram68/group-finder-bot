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
		self.cur.execute('''CREATE TABLE IF NOT EXISTS expeditions
               (name text, level int, number_p int, territory text)''')
		self.cur.execute('''CREATE TABLE IF NOT EXISTS guild
               (guildID int, ownerID int, channelID int, categoryID int)''')
		# Init Expeditions
		self.cur.execute('''INSERT INTO expeditions
					VALUES('Amrine Excavation', 25, 5, 'Windsward')''')
		self.cur.execute('''INSERT INTO expeditions
					VALUES('Starstone Barrows', 35, 5, 'Everfall')''')
		self.cur.execute('''INSERT INTO expeditions
					VALUES('The Depths', 45, 5, 'Restless Shore')''')
		self.cur.execute('''INSERT INTO expeditions
					VALUES('Dynasty Shipyard', 55, 5, 'Ebonscale Reach')''')
		self.cur.execute('''INSERT INTO expeditions
					VALUES('Garden of Genesis', 60, 5, 'Edengrove')''')
		self.cur.execute('''INSERT INTO expeditions
					VALUES('Lazarus Instrumentality', 60, 5, 'Reekwater')''')
		self.con.commit()


	def set_guild_table(self, guildID:int, ownerID:int, channelID:int, categoryID:int):
		print(f"guildID = {guildID} ownerID = {ownerID} channelID = {channelID} categoryID = {categoryID}")
		self.cur.execute("SELECT * FROM guild WHERE guildID=? AND ownerID=?", (guildID, ownerID))
		res = self.cur.fetchone()
		print(f"result: {res}")
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
