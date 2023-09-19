graphs:
	python3 src/visualise.py

results: measurements.txt
	python3 src/results.py

pingTrace: hosts
	python3 src/measurements.py

hosts:
	python3 IP_hostReader.py

clean: cleanCSV cleanPics

cleanPics:
	rm -r 'South Africa'/*.png Namibia/*.png Tanzania/*.png Morocco/*.png Senegal/*.png Malawi/*.png *.png

cleanCSV:
	rm -r 'South Africa'/*.csv Namibia/*.csv Tanzania/*.csv Morocco/*.csv Senegal/*.csv Malawi/*.csv *.csv

cleanResults:
	rm -r 'South Africa' Namibia Tanzania Morocco Senegal Malawi
