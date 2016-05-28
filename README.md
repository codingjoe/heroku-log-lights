# Heroku Log Lights

_Heroku Log Lights is a visualisation of [Heroku][heroku] router logs for an LED matrix._

### Getting Started

Simply install the PyPi package using `pip`.

```shell
pip install heroku-log-lights
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
