setup:
	python3 -m venv ~/.msds-434-final

install:
	pip install -r requirements.txt

test:
	python -m pytest -vv main_test.py

lint:
	pylint --disable=R,C main.py
	# C conventional related checks
	# R refactoring related checks
	# W various warnings
	# E errors, for probable bugs in the code
	# F fatal, if an error occured which prevented pylint

all:	install lint test