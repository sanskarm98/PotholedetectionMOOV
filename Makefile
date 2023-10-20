# Variables
PYTHON = python
REQUIREMENTS_FILE = requirements.txt
OUTPUT_FOLDER = output

# Target: default (all)
all: setup run

# Target: setup (install dependencies and create output folder)
setup:
	$(PYTHON) -m pip install -r $(REQUIREMENTS_FILE)
	mkdir -p $(OUTPUT_FOLDER)

# Target: run the Python code
run:
	$(PYTHON) sampledetection.py

# Target: clean generated files and output folder
clean:
	$(RM) -r $(OUTPUT_FOLDER)
	# Add commands to clean any other generated files or artifacts here, if any
	# For example: rm -f *.o output.txt

# Target: help (display Makefile targets)
help:
	@echo "Available targets:"
	@echo "  make setup      : Install dependencies and create output folder"
	@echo "  make run        : Run the Python script"
	@echo "  make clean      : Clean generated files and output folder"
	@echo "  make help       : Display this help message"

# PHONY targets (targets that are not files)
.PHONY: all setup run clean help
