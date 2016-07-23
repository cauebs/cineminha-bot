import os
import urllib.parse
import psycopg2

class DataBase():

	def __init__(self):
		urllib.parse.uses_netloc.append("postgres")
		self.url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		self.conn = psycopg2.connect(
		    database=self.url.path[1:],
		    user=self.url.username,
		    password=self.url.password,
		    host=self.url.hostname,
		    port=self.url.port
		)
		self.cur = self.conn.cursor()

	def get_user_location(self, tid):
		self.cur.execute("SELECT location FROM users WHERE id="+str(tid))
		return self.cur.fetchone()[0]

	def atualizar_local(self, tid, loc):
		self.cur.execute("SELECT * FROM users WHERE id="+tid)
		if self.cur.fetchone() is None:
			self.cur.execute("INSERT INTO users VALUES ("+tid+", "+loc+");")
			self.conn.commit()
		else:
			self.cur.execute("UPDATE users SET location="+loc+" WHERE id="+tid+";")
			self.conn.commit()
