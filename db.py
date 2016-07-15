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
