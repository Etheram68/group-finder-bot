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
               (guildID str, authorID str, name text, level int, number_p int, departure text, mesId int)''')
		self.cur.execute('''CREATE TABLE IF NOT EXISTS guild
               (guildID str, ownerID str, channelID str, categoryID str)''')
		self.con.commit()


	def check_if_mess_exist(self, guildID:str, mesId:str):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND mesId=?", (guildID, mesId))
		res = self.cur.fetchone()
		if res is None:
			return False
		return True

	def drop_groups_mes(self, guildID:str, mesId:str):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND mesId=?", (guildID, mesId))
		res = self.cur.fetchone()
		if res:
			self.cur.execute("DELETE FROM groups WHERE mesId=?", (mesId,))
			self.con.commit()

	def drop_groups_author(self, guildID:str, authorID:str):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND authorID=?", (guildID, authorID))
		res = self.cur.fetchone()
		if res:
			self.cur.execute("DELETE FROM groups WHERE authorID=?", (authorID,))
			self.con.commit()


	def get_id_mess(self, guildID:str, authorID:str):
		self.cur.execute("SELECT mesId FROM groups WHERE guildID=? AND authorID=?", (guildID, authorID))
		res = self.cur.fetchone()
		if res:
			return res[0]


	def get_channel_id(self, guildID:str):
		self.cur.execute("SELECT channelID FROM guild WHERE guildID=?", (guildID,))
		res = self.cur.fetchone()
		return res[0]


	def get_groups_author(self, guildID:str, authorID:str):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND authorID=?", (guildID, authorID))
		res = self.cur.fetchone()
		return res


	def set_groups_table(self, guildID:str, authorID:str, name:str, level:int, nb_player:int, departure:str, messId:int):
		self.cur.execute("SELECT * FROM groups WHERE guildID=? AND authorID=?", (guildID, authorID))
		res = self.cur.fetchone()
		if res is None:
			self.cur.execute("INSERT INTO groups VALUES(?, ?, ?, ?, ?, ?, ?)", \
							(guildID, authorID, name, level, nb_player, departure, messId))
			self.con.commit()


	def set_guild_table(self, guildID:str, ownerID:str, channelID:str, categoryID:str):
		self.cur.execute("SELECT * FROM guild WHERE guildID=? AND ownerID=?", (guildID, ownerID))
		res = self.cur.fetchone()
		if res is None:
			self.cur.execute("INSERT INTO guild VALUES(?, ?, ?, ?)", \
					(guildID, ownerID, channelID, categoryID))
		else:
			self.cur.execute('''UPDATE guild SET guildID=?, ownerID=?,
								channelID=?, categoryID=?''', \
					(guildID, ownerID, channelID, categoryID))
		self.con.commit()

	# def __del__(self):
	# 	self.cur.close()
