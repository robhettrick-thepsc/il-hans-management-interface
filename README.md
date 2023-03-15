# Hospital Activity Notification Service Management Interface

The Hospital Activity Notification Service forwards relevant internal
messages from hospital systemsm to domiciliary care providers, to let
them know when their clients have been admitted.  It is a pilot
project over a limited period to assess the benefits of providing this
information in a timely way.

This project provides the lookup service between the patient's NHS
number, as provided by the hospital, and the domiciliary care
provider's email address, so that the message can be forwarded to the
right place.

It is a [Django](https://djangoproject.com) application.

The pilot is being run by the [NHS Innovation
Lab](https://transform.england.nhs.uk/innovation-lab/).

## Usage

A `docker-compose.yml` file is provided.  Run `docker-compose up
--build` to run the application, start up a database, migrate the
database schema into place, and create a superuser account.

When running, the admin interface will be available at
http://localhost:8000/admin.  The username is `admin`, and the
password is `admin`.

No, those credentials don't work in production.  I've checked.

## Contribution

Contact [me](mailto:alex.young12@nhs.net) for further information if
you would like to contribute.
