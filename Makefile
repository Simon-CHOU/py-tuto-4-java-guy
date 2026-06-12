.PHONY: test lint format test-all

test:
	@for d in modules/*/; do \
		echo "=== Testing $$d ==="; \
		(cd "$$d" && python run_test.py complete) || exit 1; \
	done

lint:
	ruff check modules/

format:
	ruff format modules/

test-all: test lint
