.PHONY: omelettes server

omelettes:
	python scripts/harvest-neopets-omelettes.py 'https://items.jellyneo.net/search/?scat[]=22' \
		--output-csv docs/data/omelettes.csv \
		--output-json docs/data/omelettes.json \
		--image-directory docs/images/omelettes

server:
	cd docs && python3 -m http.server

publish:
	git subtree push --prefix docs origin gh-pages
