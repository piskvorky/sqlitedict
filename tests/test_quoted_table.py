import pytest

from sqlitedict import SqliteDict


@pytest.mark.parametrize('tablename', ['ordinary', 'with"quote', '""'])
def test_read_only_quoted_table(tmp_path, tablename):
    filename = str(tmp_path / 'quoted.sqlite')
    with SqliteDict(filename, tablename=tablename, autocommit=True) as db:
        db['key'] = 'value'

    with SqliteDict(filename, tablename=tablename, flag='r') as db:
        assert db['key'] == 'value'
        assert list(db.items()) == [('key', 'value')]

        with pytest.raises(RuntimeError, match='read-only'):
            db['key'] = 'changed'
