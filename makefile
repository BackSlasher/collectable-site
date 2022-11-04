.PHONY: omelettes

omelettes:
	python scripts/harvest-neopets-omelettes.py > data/omelettes.json
