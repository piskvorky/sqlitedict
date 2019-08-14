import sqlitedict

d = sqlitedict.SqliteDict('tests/db/autocommit.sqlite', autocommit=True)

for i in range(1000):
    d[i] = i
