import os
import urllib.parse
import psycopg2
from psycopg2.extras import DictCursor

class DataBase():

	def __init__(self):
		urllib.parse.uses_netloc.append("postgres")
		self.url = urllib.parse.urlparse('postgres://uzqaehuvapxouf:Zq17yP0GuqXOxaU17WAHFz8CIL@ec2-50-19-244-148.compute-1.amazonaws.com:5432/d4937kdm1e2hlm')
		self.url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
		self.conn = psycopg2.connect(
		    database=self.url.path[1:],
		    user=self.url.username,
		    password=self.url.password,
		    host=self.url.hostname,
		    port=self.url.port
		)
		self.cur = self.conn.cursor(cursor_factory=DictCursor)

#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

#cur.close()
#conn.close()