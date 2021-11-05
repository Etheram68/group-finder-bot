import sqlite3

class DaoFactory:
	def __init__(self):
		print("Init Database ...")
		self.con = sqlite3.connect('finder.db')
		self.cur = self.con.cursor()
		self.cur.execute('''SELECT count(*) from sqlite_master WHERE type='table' AND name='expeditions' ''')
		rows = self.cur.fetchall()
		if rows is None:
			self.__init_tables_expeditions()
		print("Init Database ok")


	def __init_tables_expeditions(self):
		self.cur.execute('''CREATE TABLE IF NOT EXISTS expeditions
               (name text, level int, number_p int, territory text)''')
		self.cur.execute('''CREATE TABLE IF NOT EXISTS guild
               (guildID text, id text, channelID text, categoryID text)''')
		# Init Expeditions
		self.cur.execute('''INSERT INTO expeditions VALUES('Amrine Excavation', 25, 5, 'Windsward')''')
		self.cur.execute('''INSERT INTO expeditions VALUES('Starstone Barrows', 35, 5, 'Everfall')''')
		self.cur.execute('''INSERT INTO expeditions VALUES('The Depths', 45, 5, 'Restless Shore')''')
		self.cur.execute('''INSERT INTO expeditions VALUES('Dynasty Shipyard', 55, 5, 'Ebonscale Reach')''')
		self.cur.execute('''INSERT INTO expeditions VALUES('Garden of Genesis', 60, 5, 'Edengrove')''')
		self.cur.execute('''INSERT INTO expeditions VALUES('Lazarus Instrumentality', 60, 5, 'Reekwater')''')
		self.con.commit()

	# def __del__(self):
	# 	self.cur.close()
