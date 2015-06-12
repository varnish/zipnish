## Solution Steps ##

1. Install ZipKin and have it up and running
2. Install Scribe and have it up and running
3. Feed false data to Scribe, to see if Scribe SpanReciever inside ZipKin picks up data from Scribe.
4. On validationing above 3 steps. Replace false data generation layer with python varnish logger.


## Tracking Micro-Services via Varnish Cache ##

Track timing of micro-service requests by passing micro-service requests through a varnish server.

* [Configuring JDK](docs/Configuring JDK.md)
* [ZipKin](docs/ZipKin.md)
* [Collecting log data](docs/Collecting Data.md)
* [Varnish Logger](docs/Varnish Logger.md)


#### Machine Used ####

Debian 8.1 / **specifically** Linux debian 3.16.0-4-amd64 #1 SMP Debian 3.16.7-ckt9-3~deb8u1 (2015-04-24) x86_64 GNU/Linux
