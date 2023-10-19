include .env

.PHONY: dev install

ENGINE = venv/bin/python
ENGINE_SETUP = venv/bin/pip
FLASK = venv/bin/flask
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_EXISTS := $(shell which venv/bin/python)

check_venv:
ifneq ($(ENGINE),$(VENV_EXISTS))
	$(error Virtualenv is not created)
endif

dev: check_venv
ifeq (dev,$(MODE))
	$(FLASK) run --debug
else
	$(FLASK) run
endif

install:
	$(ENGINE_SETUP) install $(req)

req_in_file:
	$(ENGINE_SETUP) freeze > requirements.txt
