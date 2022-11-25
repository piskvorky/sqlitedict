import tempfile

from sqlitedict import SqliteDict


def insert():
    with tempfile.NamedTemporaryFile() as tmp:
        for j in range(100):
            with SqliteDict(tmp.name) as d:
                d["tmp"] = j
                d.commit()


def test(benchmark):
    benchmark(insert)
