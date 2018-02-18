PYTHON     ?= $(shell which python3)
PIP	       ?= $(shell which pip3)
LED_MATRIX_LIB_DIR = rpi-rgb-led-matrix

all:
	PYTHON=$(PYTHON) $(MAKE) -C $(LED_MATRIX_LIB_DIR) build-python

install:
	PYTHON=$(PYTHON) $(MAKE) -C $(LED_MATRIX_LIB_DIR) install-python
	$(PIP) install .

clean:
	PYTHON=$(PYTHON) $(MAKE) -C $(LED_MATRIX_LIB_DIR) clean
	rm -rf heroku_loglights.egg-info

