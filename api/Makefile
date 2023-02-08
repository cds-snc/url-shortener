.PHONY: dev fmt install lint test fmt-ci lint-ci install-dev

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

fmt:
	black . $(ARGS) --target-version py311

install:
	pip3 install --user -r requirements.txt

install-dev:
	pip3 install --user -r requirements_dev.txt

lint:
	flake8 .

test:
	coverage run -m pytest -s -vv tests &&\
	coverage report -m

lint-ci:
	flake8 .

fmt-ci:
	black --check . --target-version py311