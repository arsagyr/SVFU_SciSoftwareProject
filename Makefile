all:
	python3 main.py
web:
	flask --app app run --debug
deactivate:
	deactivate
install:
	python3 -m pip install -r requirements.txt