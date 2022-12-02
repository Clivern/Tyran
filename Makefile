UV           ?= uv


export TEST_RUN=true


help: Makefile
	@echo
	@echo " Choose a command run in Tyran:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo


## config: Install dependencies.
.PHONY: config
config:
	$(UV) sync


## lint: Lint The Code.
.PHONY: lint
lint:
	@echo "\n>> ============= All linting cases passed! ============= <<"
	$(UV) run ruff check


## run: Run Fast API application
.PHONY: run
run:
	@echo "\n>> ============= Run the Server ============= <<"
	$(UV) run fastapi dev app/main.py


## test: Run test cases
.PHONY: test
test:
	export TEST_RUN=true
	$(UV) run pytest -v


## ci: Run all CI tests.
.PHONY: ci
ci: lint test
	@echo "\n>> ============= All quality checks passed ============= <<"


.PHONY: help
