# Heroku Log Lights

_Heroku Log Lights is a visualisation of [Heroku][heroku] router logs for a LED matrix._

![HLL Demo](demo.gif)

This little tool allows you to monitor all your applications router logs in real time.
All requests are displayed in a logarithmic scale. 2xx responses are green, 3xx are blue, 4xx yellow & 5xx are red. The longer a request takes the more the color shifts to red. If a request hits the top, it ran for 30s and Heroku throws a H12 (request timeout).

It sounds simple but it provides you with incredible feedback about your applications health.

## Manual

![Read the manual](https://cdn.meme.am/cache/instances/folder246/57635246.jpg)

**Everything is green:**
That's great, but you should think about cache control and ETags.
(2xx response)

**Everything is purple:**
That's the heroku way! But maybe your CDN isn't working.
(3xx response)

**Everything is yellow:**
Upsy daisy, the latest version of your Android or Angular App is sending wrong requests to your backend...
(4xx response)

**Everything is red:**
Run and hide! You have about 10min until your boss comes storming the office and heads are rolling.
(5xx response)

## Makers Guide

### Parts

![LEDs everywhere](https://img.memesuper.com/0e7aae6b9766c895a845cae2fbb0aff9_3466791-led-memes_400-304.jpeg)

* [RGB LED Matrix](http://a.co/89lfm33)
* [Raspberry Pi](https://www.raspberrypi.org)
* [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345) (optional)
* power supply (5V and ~5A per 32x32 pixel)
 * [for the Adafrouit HAT](https://www.amazon.com/XINY-100V-240V-Switching-Interface-Surveillance/dp/B01JI373AY/)
 * or [this one](www.amazon.com/Pasow-Strip-Switching-Supply-Adapter/dp/B015C6DU6M/)

### Assembly

![Mac Gyver defusal](https://s-media-cache-ak0.pinimg.com/736x/c7/fb/61/c7fb612016dbc8f632b0b4349081247b.jpg)

[Henner Zeller][hzeller]
not only wrote the library that powers LED matrixes on the Pi, but also wrote a very detailed [documentation][rpi-rgb-led-matrix] that should help you assemble all the parts.

Once you have the [demo](https://github.com/hzeller/rpi-rgb-led-matrix#lets-do-it) running and all pixels are in the right place, come back and continue with the setup.

### Setup

![Star Trek helm](http://vignette4.wikia.nocookie.net/memoryalpha/images/9/94/Galaxy_mission_ops.jpg/revision/latest/scale-to-width-down/800?cb=20120226203320&path-prefix=en)

You are almost done. All we need now is Python 3 because we are using asyncio (duh).

#### Install dependencies
```shell
sudo apt-get install git python3-dev python3-pillow python3-pip -y
```

#### Build an install package
```shell
cd /tmp
git clone --recursive https://github.com/codingjoe/heroku-log-lights.git
make
sudo make install
```

#### Run HLL

To access the router logs of your Heroku application, you will need an API token.
You can ether install the [heroku toolbelt][heroku-toolbelt]
or obtain the [API AUTH token][heroku-token] from the heroku website.

Via heroku toolbelt:

```shell
heroku-log-lights -a YOUR_APP_NAME -t `heroku auth:token`
```

or via token:

```shell
export HEROKU_API_TOKEN=YOUR_SECRET_TOKEN
heroku-log-lights -a YOUR_APP_NAME
```

That's it, you are ready to roll! Enjoy

![Knight Rider approved](http://sm.ign.com/ign_de/screenshot/default/knight-rider_u17w.jpg)

[heroku]: https://www.heroku.com/
[heroku-toolbelt]: https://toolbelt.heroku.com/
[heroku-token]: https://devcenter.heroku.com/articles/platform-api-quickstart#authentication
[hzeller]: https://github.com/hzeller
[rpi-rgb-led-matrix]: https://github.com/hzeller/rpi-rgb-led-matrix
