# Foottrial

<p align="center">
 <img src="./docs/statics/usecase_system.svg">
</p>


## Table of content

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
- [Running Test](#running-the-tests)
- [Developing](#developing)
- [Contributing](#contributing)
- [versioning](#versioning)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

For setting up the project we need first to install the following
requirements.

### Prerequisites

This is a list of applications that need to be installed previously to enjoy all the goodies of this configuration.

* [Python 2.7.x](http://python.org/download/)
* [PostgreSQL 9.4](http://www.postgresql.org/download/)
* [RabbitMQ 3.5.4](https://www.rabbitmq.com)
* [NodeJs 0.12.7](https://nodejs.org/)
* [Ruby 2.2.2](https://www.ruby-lang.org/en/installation/#package-management-systems)
* [Compass 1.0.1](http://compass-style.org/install/)
* [Gulp 3.9.0](https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md)
* [Browserify](http://browserify.org/#install)


### Installing

First, we need to synchronize the database.

```bash
$ cd src
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

Then, we run a local development server doing this.

```bash
$ python manage.py runserver
```

To load initial data just run the following command:

```bash
$ python manage.py loaddata messages.json hospitals.json
```

**Run Task queue processes**

Use celery we need to create a RabbitMQ user, a virtual host and allow that user access to that virtual host:

```bash
$ sudo rabbitmqctl add_user myuser mypassword
$ sudo rabbitmqctl add_vhost myvhost
$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```

Then we set up a BROKER_URL env var and run celery to the same level of manage.py

```bash
$ export BROKER_URL='amqp://myuser:mypassword@localhost:5672/myvhost'
$ celery -A foottrial worker -l info
```

**Run the scheduler**

  ```bash
  $ celery -A foottrial beat
  ```

## Running the tests

Execute test Behave

```
make test
```

## Authors

* **Oscar Giraldo** - *Initial work* - [oskargicast](https://github.com/oskargicast)
* **Jorge Estrada** - *Initial work* - [jorgenro1](https://github.com/jorgenro1)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
