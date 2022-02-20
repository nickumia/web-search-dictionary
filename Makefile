
build:
	docker build -t websearchdict:dev .

lint:
	docker run --rm -v "$(shell pwd)":/boc websearchdict:dev bash -c "cd /boc && flake8 . --count --show-source --statistics"

run:
	docker run --rm -v "$(shell pwd)":/boc websearchdict:dev bash -c "python $(FILE)"

test:
	docker run --rm -v "$(shell pwd)":/boc websearchdict:dev bash -c "coverage run --source=websearchdict -m pytest --disable-pytest-warnings $(FILE) && coverage report --omit=\"tests/*\""
