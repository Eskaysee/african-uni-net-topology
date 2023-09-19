graphs:
	python3 visualise.py

results: measurements.txt
	python3 results.py

pingTrace: hosts
	python3 measurements.py

hosts:
	python3 IP_hostReader.py

clean:
	rm -r results
