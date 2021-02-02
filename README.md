# Mining dashboards

Grafana dashboards for cryptocurrency miners.

## Requirements

Dashboards rely on the following softwares:
 - [Telegraf](https://github.com/influxdata/telegraf) to gather metrics (input) and write to a datastore (output)
 - [InfluxDB](https://github.com/influxdata/influxdb) to store metrics on the long-term
 - [Grafana](https://github.com/grafana/grafana) to visualize metrics

This stack is also known as the **TIG** stack.

## Quickstart

The easiest way to test is to use [Docker](https://www.docker.com/). Ensure you have `docker` and
`docker-compose` binary installed.

Write your miner address, grafana and influxdb credentials:

```
vi docker/environment
```

Then start containers:

```
docker-compose up -d
```

## Going further

You should secure [InfluxDB](https://docs.influxdata.com/influxdb/v1.7/administration/security/) by using encryption for
communication. The stack doesn't require Docker.

## Disclaimer

Telegraf is able to make API call on thrid-party services. Please read terms of service before going further. The
repository owner cannot be responsible of any abuse.
