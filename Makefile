
build:
	docker build -t wsd:dev .

lint:
	docker run --rm -v "$(shell pwd)":/boc wsd:dev bash -c "cd /boc && flake8 . --count --show-source --statistics"

test:
	docker run --rm -v "$(shell pwd)":/boc wsd:dev bash -c "coverage run --source=wsd -m pytest --disable-pytest-warnings && coverage report --omit=\"tests/*\""
