test-all:
	@ echo '- removing old data'
	@ rm -f -R tests/db/
	@ echo '- creating new tests/db/ (required for tests)'
	@ mkdir -p tests/db
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase  -l DEBUG

test-all-with-coverage:
	@ echo '- removing old data'
	@ rm -f -R tests/db/
	@ echo '- creating new tests/db/ (required for tests)'
	@ mkdir -p tests/db
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase --with-coverage -l DEBUG
