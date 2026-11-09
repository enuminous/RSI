.PHONY: test demo replay verify

test:
	python -m unittest discover -s tests -v

demo:
	python -m rsi run --out runs/local

verify:
	python -m rsi verify examples/frozen_demo --check-source

replay:
	python -m rsi replay examples/frozen_demo
