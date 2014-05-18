test-all:
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase 

test-all-with-coverage:
	@ nosetests --cover-package=sqlitedict --verbosity=1 --cover-erase --with-coverage 	