.PHONY: dev e2e fmt install lint test fmt-ci lint-ci install-dev

dev:
	@export $$(xargs < .env) > /dev/null &&\
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

e2e:
	docker build -t cypress-axe -f ./e2e/Dockerfile . &&\
	docker run -it \
	--network host \
	-v $$PWD/e2e:/e2e  \
	-w /e2e \
	--entrypoint=cypress \
	cypress-axe run

fmt:
	black . $(ARGS) --target-version py311

install:
	pip3 install --user -r requirements.txt

install-dev:
	pip3 install --user -r requirements_dev.txt

lint:
	flake8 .

test:
	coverage run -m pytest -s -vv --last-failed --new-first tests &&\
	coverage report -m

lint-ci:
	flake8 .

fmt-ci:
	black --check . --target-version py311