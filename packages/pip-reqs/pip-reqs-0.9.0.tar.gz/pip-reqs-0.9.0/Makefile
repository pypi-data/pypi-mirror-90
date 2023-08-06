ptest:
	tox -e $$(tox -l | grep test | paste -s -d,) -p all
	tox -e lint
	tox -e coverage

test:
	tox

lint:
	docker run --rm --env-file=../.lint -v $(PWD):/app divio/lint /bin/lint
