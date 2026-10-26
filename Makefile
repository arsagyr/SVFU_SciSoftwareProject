all:
	python3 main.py
web:
	flask --app app run --debug
deactivate:
	deactivate
install:
	pip install -r requirements.txt