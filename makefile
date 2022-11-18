.PHONY: omelettes server

omelettes:
	python scripts/harvest-neopets-omelettes.py 'https://items.jellyneo.net/search/?scat[]=22' \
		--output-csv html/data/omelettes.csv \
		--output-json html/data/omelettes.json \
		--image-directory html/images/omelettes

server:
	cd html && python3 -m http.server

publish:
	git subtree push --prefix html origin gh-pages
