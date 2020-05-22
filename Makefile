PYTHON = python3
LED_MATRIX_LIB_DIR = rpi-rgb-led-matrix
HARDWARE_DESC = adafruit-hat

all:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) build-python

install:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) install-python
	$(PYTHON) setup.py install

clean:
	PYTHON=$(PYTHON) HARDWARE_DESC=$(HARDWARE_DESC) $(MAKE) -C $(LED_MATRIX_LIB_DIR) clean
	rm -rf heroku_loglights.egg-info

