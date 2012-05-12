PROJ := dreamssh
LIB := dreamssh
GITHUB_REPO := github.com:dreamhost/$(PROJ).git
PKG_NAME := $(PROJ)
TMP_FILE ?= /tmp/MSG
VIRT_DIR ?= .venv

keygen:
	@python -c "from dreamssh import scripts;scripts.KeyGen()"

run:
	twistd -n dreamssh

daemon:
	twistd dreamssh

shell:
	@python -c "from dreamssh import scripts;scripts.ConnectToShell()"

stop:
	@python -c "from dreamssh import scripts;scripts.StopDaemon()"

run-test:
	make daemon && make shell && make stop

banner:
	python -c "from $(LIB) import config; print config.ssh.banner;"

generate-config:
	rm -rf ~/.$(PROJ)/config.ini
	python -c "from $(LIB) import config; config.writeDefaults();"

log-concise:
	git log --oneline

log-verbose:
	git log --format=fuller

log-authors:
	git log --format='%aN %aE' --date=short

log-authors-date:
	git log --format='%ad %aN %aE' --date=short

log-changes:
	git log --format='%ad %n* %B %N%n' --date=short

clean:
	sudo rm -rfv dist/ MANIFEST *.egg-info
	rm -rfv _trial_temp/ MANIFEST CHECK_THIS_BEFORE_UPLOAD.txt twistd.log
	find ./ -name "*~" -exec rm -v {} \;
	sudo find ./ -name "*.py[co]" -exec rm -v {} \;
	find . -name "*.sw[op]" -exec rm -v {} \;

push:
	git push --all git@$(GITHUB_REPO)

push-tags:
	git push --tags git@$(GITHUB_REPO)

push-all: push push-tags
.PHONY: push-all

stat:
	@echo
	@echo "### Git info ###"
	@echo
	git info
	echo
	@echo "### Git working branch status ###"
	@echo
	@git status -s
	@echo
	@echo "### Git branches ###"
	@echo
	@git branch
	@echo

status: stat
.PHONY: status

todo:
	git grep -n -i -2 XXX
	git grep -n -i -2 TODO
.PHONY: todo

build-docs:
	cd docs/sphinx; make html

check-docs: files = "README.rst"
check-docs:
	@echo "noop"

check-examples: files = "examples/*.py"
check-examples:
	@echo "noop"

check-dist:
	@echo "Need to fill this in ..."

check: build check-docs check-examples
	trial $(LIB)

check-integration:
# placeholder for integration tests
.PHONY: check-integration

version:
	@echo $(VERSION)

virtual-build: SUB_DIR ?= test-build
virtual-build: DIR ?= $(VIRT_DIR)/$(SUB_DIR)
virtual-build: clean build
	mkdir -p $(VIRT_DIR)
	-test -d $(DIR) || virtualenv $(DIR)
	@. $(DIR)/bin/activate
	-test -e $(DIR)/bin/twistd || $(DIR)/bin/pip install twisted
	-test -e $(DIR)/bin/rst2html.py || $(DIR)/bin/pip install docutils
	$(DIR)/bin/pip uninstall -vy $(PKG_NAME)
	rm -rf $(DIR)/lib/python2.7/site-packages/$(PKG_NAME)*
	$(DIR)/bin/easy_install-2.7 ./dist/$(PKG_NAME)*

clean-virt: clean
	rm -rf $(VIRT_DIR)

virtual-build-clean: clean-virt build virtual-build
.PHONY: virtual-build-clean

build:
	python setup.py build
	python setup.py sdist

install:
	sudo pip install .

uninstall:
	sudo pip uninstall dreamssh

register: clean
	python setup.py register

upload: clean check
	python setup.py sdist upload --show-response
