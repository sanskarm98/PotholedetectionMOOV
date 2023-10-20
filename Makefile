PYTHON = python

# Target: default (all)
all: setup run

# Target: setup (install dependencies)
setup:
	$(PYTHON) -m pip install ultralytics
	$(PYTHON) -m pip install opencv-python
	$(PYTHON) -m pip install geopy

# Target: run the Python code
run:
	$(PYTHON) sampledetection.py

# Target: clean generated files
clean:
	# Add commands to clean any generated files or artifacts here, if any
	# For example: rm -f *.o output.txt

# Target: help (display Makefile targets)
help:
	@echo "Available targets:"
	@echo "  make setup      : Install dependencies"
	@echo "  make run        : Run the Python script"
	@echo "  make clean      : Clean generated files"
	@echo "  make help       : Display this help message"

# PHONY targets (targets that are not files)
.PHONY: all setup run clean help
