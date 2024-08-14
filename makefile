#  MovieLens Database Application Makefile

all: main.py datatier.py objecttier.py
	python3 main.py

clean:
	rm -f *.pyc
