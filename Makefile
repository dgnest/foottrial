# Makefile for FootTrial.

# Configuration.
SHELL = /bin/bash
ROOT_DIR = $(shell pwd)
BIN_DIR = $(ROOT_DIR)/bin
DATA_DIR = $(ROOT_DIR)/var
SCRIPT_DIR = $(ROOT_DIR)/script

WGET = wget

# Bin scripts
CELERY = $(shell) $(SCRIPT_DIR)/celery.sh
CLEAN = $(shell) $(SCRIPT_DIR)/clean.sh
CLEAN_MIGRATIONS = $(shell) $(SCRIPT_DIR)/clean_migrations.sh
INSTALL = $(shell) $(SCRIPT_DIR)/install.sh
SETUP = $(shell) $(SCRIPT_DIR)/setup.sh
TEST = $(shell) $(SCRIPT_DIR)/test.sh
PM = $(shell) $(SCRIPT_DIR)/pm.sh
POPULATE = $(shell) $(SCRIPT_DIR)/populate.sh
POPULATE_TEST = $(shell) $(SCRIPT_DIR)/populate_test.sh
GVM = $(shell) $(SCRIPT_DIR)/gvm.sh
GRIP = $(shell) $(SCRIPT_DIR)/grip.sh
PYENV = $(shell) $(SCRIPT_DIR)/pyenv.sh
PLUGINS_VAGRANT = $(shell) $(SCRIPT_DIR)/plugins_vagrant.sh
RUNSERVER = $(shell) $(SCRIPT_DIR)/runserver.sh
TRANSLATE = $(shell) $(SCRIPT_DIR)/translate.sh
SYNC = $(shell) $(SCRIPT_DIR)/sync.sh

install:
	$(INSTALL)


pm:
	echo "${action}"
	@if [ "${action}" == '' ]; then \
        echo "Error: Variables not set correctly"; exit 2; \
	fi
	$(PM) "${action}"


populate:
	$(POPULATE)


populate_test:
	$(POPULATE_TEST)


plugins_vagrant:
	$(PLUGINS_VAGRANT)


clean:
	$(CLEAN)


clean_migrations: clean
	$(CLEAN_MIGRATIONS)


celery:
	$(CELERY)

environment:
		$(PYENV)
		$(GVM)

grip:
	$(GRIP)


setup:
	$(SETUP)

runserver:
	@if [ "${env}" == '' ]; then \
        echo "Error: Variables not set correctly"; exit 2; \
	fi
	$(RUNSERVER) "${env}"