LEVEL ?= 00

.PHONY: re clean solve black pylint 

default:
	make solve

# By default, runs the script to solve level00
# To run another level, set a value between 00 and 14 for LEVEL, i.e. `make LEVEL=02`
solve: level${LEVEL}/Ressources/level${LEVEL}.py $(DOCKER_FILES)
	@echo "Makefile: Running script to solve level ${LEVEL}"
	python3 $< SILENT=1

# Removes files created while running scripts solving the challenges
clean:
	rm -f level01/Ressources/passwd
	rm -f level02/Ressources/level02.pcap
	rm -f level07/Ressources/core
	find . -name "token" -type f -delete

re: 
	make clean
	make

black:
	find . -name *.py -not -path ".\/.*" -exec black {} \;

pylint:
	find . -name *.py -not -path ".\/.*" -exec pylint {} \;
