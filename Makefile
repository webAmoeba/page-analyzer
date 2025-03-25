install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

build:
	uv build

i:
	uv tool install .

uninstall:
	uv tool uninstall hexlet-code
	uv clean

re: uninstall i
