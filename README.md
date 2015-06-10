## Process ##

1. Install ZipKin and have it up and running
2. Install Scribe and have it up and running
3. Feed false data to Scribe, to see if Scribe SpanReciever inside ZipKin picks up data from Scribe.
4. On validationing above 3 steps. Replace false data generation layer with python varnish logger.


# Tracking Micro-Services via Varnish Cache #

## Scope ##

Track timing of micro-service requests by passing micro-service requests through a varnish server.


* [Configuring JDK](docs/Configuring JDK.md)
* [Scribe](docs/Scribe.md)
* [Varnish Logger](docs/Varnish Logger.md)
* [ZipKin](docs/ZipKin.md)

* [Collecting log data](docs/Collecting Data.md)
