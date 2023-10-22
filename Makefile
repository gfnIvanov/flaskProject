include .env
include .flaskenv

.PHONY: run install

PYTHON = venv/bin/python
PIP = venv/bin/pip
FLASK = venv/bin/flask
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_EXISTS := $(shell which venv/bin/python)

check_venv:
ifneq ($(PYTHON),$(VENV_EXISTS))
	$(error Virtualenv is not created)
endif

# run app
run: check_venv
	@echo ">>> App running on port" $(FLASK_RUN_PORT)
ifeq (dev,$(MODE))
	$(FLASK) run --debug
else
	$(FLASK) run
endif

# database commands
create_tables: check_venv
	$(FLASK) create_tables

migrate: check_venv
ifeq (,$(msg))
	$(FLASK) db migrate && $(FLASK) db upgrade
else
	$(FLASK) db migrate -m $(msg) && $(FLASK) db upgrade
endif

# dependency control
install:
	$(PIP) install $(req)

req_in_file:
	$(PIP) freeze > requirements.txt
