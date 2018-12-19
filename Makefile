venv: venv/bin/activate

SHELL := /bin/bash

.PHONY: install check env-setup

install:
	pip3 install -r requirement.txt

check:
	@python --version

env-setup:
	@virtualenv -p python3 env
	@chmod +x env/bin/*
