# Analytics

> [!NOTE]
> The analytics front end will likely change in the future to show more information about the miner state.

The analytics site allows you to see the progress of the miner over time. Each time you gain or lose channel points
that information will be recorded in a file in the `analytics` directory. You can then view this in a graph by visiting
the miner's analytics page at `localhost:5000` (assuming you chose port 5000 in your configuration).

To run the analytics server place the following before running the miner in your configuration file:

```python3
twitch_miner.analytics(host="0.0.0.0", port=5000, refresh=5, days_ago=7)
```

This assumes your miner is called `twitch_miner`.

`host` is the IP address to which to bind the analytics server. Normally, this is either `"0.0.0.0"` if running in a
Docker container, or `"127.0.0.1"` if running locally.

`port` is the port to which to bind the analytics server. This can be any reasonable port number, we default to `5000`.

`refresh` is the amount of minutes to wait in between polling for new changes. Currently not implemented, the server
will instead check every 5 minutes.

`days_ago` is the amount of previous days worth of data that the charts will show by default.
