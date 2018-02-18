PYTHON     ?= $(shell which python3)
PIP	       ?= $(shell which pip3)
LED_MATRIX_LIB_DIR = rpi-rgb-led-matrix

all:
	$(MAKE) -C $(LED_MATRIX_LIB_DIR) build-python

install:
	$(MAKE) -C $(LED_MATRIX_LIB_DIR) install-python
	$(PIP) install .

clean:
	$(MAKE) -C $(LED_MATRIX_LIB_DIR) clean
	rm -rf heroku_loglights.egg-info

