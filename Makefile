# Virtual environment setup
VENV_DIR = venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

.PHONY: all clean run

all: $(VENV_ACTIVATE)

# Create virtual environment
$(VENV_ACTIVATE):
	python3 -m venv $(VENV_DIR) && \
		. $(VENV_ACTIVATE) && \
		pip install --upgrade pip && \
		pip install -r requirements.txt

# Run the script
run: $(VENV_ACTIVATE)
	. $(VENV_ACTIVATE) && \
	python3 YOLO_detection.py

# Clean up
clean:
	rm -rf $(VENV_DIR)

