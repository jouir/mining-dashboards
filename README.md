# Mining dashboards

Grafana dashboards for cryptocurrency miners.

## Requirements

Dashboards rely on the following softwares:
 - [Telegraf](https://github.com/influxdata/telegraf) to gather metrics (input) and write to a datastore (output)
 - [InfluxDB](https://github.com/influxdata/influxdb) to store metrics on the long-term
 - [Grafana](https://github.com/grafana/grafana) to visualize metrics

This stack is also known as the **TIG** stack.

## Quickstart

**Testing purpose only**.

This guide uses [Docker](https://www.docker.com/). Ensure you have `docker`, `docker-compose` and `openssl` binaries
installed.

Write your miner address, grafana and influxdb credentials:

```
vi docker/environment
```

Generate a self-signed certificate:

```
openssl req -x509 -nodes -newkey rsa:2048 -keyout docker/ssl/influxdb.key -out docker/ssl/influxdb.crt -days 365
```

Press enter to every question.

Then start containers:

```
docker-compose up -d
```

## Disclaimer

Telegraf is able to make API call on thrid-party services. Please read terms of service before going further. The
repository owner cannot be responsible of any abuse.
