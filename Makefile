FAPI         ?= fastapi
PIP          ?= pip
PYCODESTYLE  ?= pycodestyle
PYTEST       ?= pytest


help: Makefile
	@echo
	@echo " Choose a command run in Tyran:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo


## config: Install dependencies.
.PHONY: config
config:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.test.txt
	$(PIP) install -r requirements.txt


## lint-pycodestyle: PyCode Style Lint
.PHONY: lint-pycodestyle
lint-pycodestyle:
	@echo "\n>> ============= Pycodestyle Linting ============= <<"
	@find app -type f -name \*.py | while read file; do echo "$$file" && $(PYCODESTYLE) --config=./pycodestyle --first "$$file" || exit 1; done


## lint: Lint The Code.
.PHONY: lint
lint: lint-pycodestyle
	@echo "\n>> ============= All linting cases passed! ============= <<"


## run: Run Fast API application
.PHONY: run
run:
	@echo "\n>> ============= Run the Server ============= <<"
	$(FAPI) dev app/main.py


## outdated-pkg: Show outdated python packages
.PHONY: lint outdated-pkg
outdated-pkg:
	@echo "\n>> ============= List Outdated Packages ============= <<"
	$(PIP) list --outdated


## test: Run test cases
.PHONY: test
test:
	TEST_RUN=true $(PYTEST) -v


## ci: Run all CI tests.
.PHONY: ci
ci: lint test outdated-pkg
	@echo "\n>> ============= All quality checks passed ============= <<"


.PHONY: help
