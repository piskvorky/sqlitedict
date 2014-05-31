test-all:
	@ rm -d -f tests/db/*
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase 

test-all-with-coverage:
	@ rm -d -f tests/db/*
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase --with-coverage 	