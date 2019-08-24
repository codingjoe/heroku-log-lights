PYTHON     ?= $(shell command -v python3)
PIP	       ?= $(shell command -v pip3)
LED_MATRIX_LIB_DIR = rpi-rgb-led-matrix
HARDWARE_DESC = adafruit-hat

all:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) build-python

install:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) install-python
	$(PIP) install -e .

clean:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) clean
	rm -rf heroku_loglights.egg-info

