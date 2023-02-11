.PHONY: omelettes server

omelettes:
	mkdir -p docs/data/omelettes
	python scripts/harvest-neopets-omelettes.py  \
		--output-directory docs/data/omelettes/ \

server:
	cd docs && python3 -m http.server

publish:
	git subtree push --prefix docs origin gh-pages
