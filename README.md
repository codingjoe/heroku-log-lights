# Heroku Log Lights

_Heroku Log Lights is a visualisation of [Heroku][heroku] router logs for an LED matrix._

![HLL Demo](demo.gif)

## Getting Started

### Install dependencies
```shell
sudo apt-get install git python3-dev python3-pillow python3-pip -y
```

### Build an install package
```shell
cd /tmp
git clone --recursive https://github.com/codingjoe/heroku-log-lights.git
make
sudo make install
```

You ether need to install the [heroku toolbelt][heroku-toolbelt]
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

[heroku]: https://www.heroku.com/
[heroku-toolbelt]: https://toolbelt.heroku.com/
[heroku-token]: https://devcenter.heroku.com/articles/platform-api-quickstart#authentication
