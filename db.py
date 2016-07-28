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

	def get_loc(self, uid):
		self.cur.execute("SELECT location FROM users WHERE id="+str(uid))
		return self.cur.fetchone()[0]

	def set_loc(self, uid, loc):
		self.cur.execute("SELECT * FROM users WHERE id="+str(uid))
		if self.cur.fetchone() is None:
			self.cur.execute("INSERT INTO users (id, location, language) VALUES ("+str(uid)+', \''+loc+'\', \'en\');')
			self.conn.commit()
			return False
		else:
			self.cur.execute('UPDATE users SET location=\''+loc+'\' WHERE id='+str(uid))
			self.conn.commit()
			return True
