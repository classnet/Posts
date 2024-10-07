#
#  Copyright (c) 2016, The OpenThread Authors.
#  All rights reserved.
import sqlite3
conn = sqlite3.connect('s.db')
c = conn.cursor()
print(c.fetchall())
conn.close()
print("Hello World")



