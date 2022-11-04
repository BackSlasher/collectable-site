.PHONY: omelettes server

omelettes:
	python scripts/harvest-neopets-omelettes.py 'https://items.jellyneo.net/search/?scat[]=22' \
		--output-csv data/omelettes.csv \
		--output-json data/omelettes.json \
		--image-directory images/omelettes

server:
	python3 -m http.server
