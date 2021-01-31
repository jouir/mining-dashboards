# Mining dashboards

Grafana dashboards for cryptocurrency miners.

## Requirements

Dashboards rely on the following softwares:
 - [Telegraf](https://github.com/influxdata/telegraf) to gather metrics (input) and write to a datastore (output)
 - [InfluxDB](https://github.com/influxdata/influxdb) to store metrics on the long-term
 - [Grafana](https://github.com/grafana/grafana) to visualize metrics

This stack is also known as the **TIG** stack.

## Disclaimer

Telegraf is able to make API call on thrid-party services. Please read terms of service before going further. The
repository owner cannot be responsible of any abuse.
