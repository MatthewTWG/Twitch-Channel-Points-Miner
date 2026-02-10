# Getting Started

As an overview, to get started you should:

1. Get the latest version, see [here](#getting-the-miner).
2. Write your configuration file, see [here](#configuration).
3. Run the miner, see [here](#running-the-miner).

## Getting The Miner

There are several options for getting the miner. The recommended option is to run the miner in docker by using
the [docker hub image](https://hub.docker.com/r/mpforce1/twitch-channel-points-miner). If you choose this method you can
skip the rest of this section.

If you prefer to not use docker hub please see the [advanced usage](advanced-usage.md#getting-the-miner) guide for more
information.

## Configuration

> [!NOTE]
> The following shows the basic usage which should be suitable for most users, see [here](advanced-usage.md) for
> advanced usage

> [!NOTE]
> In the future, we'll be adding the ability to configure using an easier to read/write format.

Configuration is done via the `run.py` file.

The simplest way to get started is to make a copy of
the [minimal run](/minimal-run.py) file, call the copy `run.py`, and change the necessary fields in the copy to suit
your needs.

> [!CAUTION]
> When modifying the contents of your `run.py` file the whitespace (newlines, spaces) should be kept as is to avoid
> python errors.

### Mine Streamers You Follow

Early in the file, there are a couple of lines you need to modify:

```python3
username="your-twitch-username",
password="write-your-secure-psw",
```

Please exchange the contents of each pair of quotes with their respective values: your Twitch username and password. If
you do not replace both of these the miner will output an error and not start.

Once this runs it will load all of your followers and mine them using the default configuration. By default, the
followers will be mined in the order you followed them ascending, so oldest follows first.

### Mine Any Streamers

If you want to mine streamers other than your followers, or you want to mine them in a specific order, then you can
define the list manually. Near the end of the file, there are a couple of lines you have to modify:

```python3
streamers=[],
followers=True,
```

Fill in the square bracket with a comma separated list of streamer usernames you want to mine. Each username should be
in a pair of quotes. You can also disable the followers by changing `True` to `False` on the next line. For example:

```python3
streamers=["streamer1", "streamer2", "streamer3"],
followers=False,
```

This will mine streamers with the usernames `streamer1`, `streamer2`, and `streamer3`. Priority goes from left to right
in the order they're defined in the list. This means that if all 3 streamers are online at the same time it'll
prioritise mining `streamer1` and `streamer2` because they appear earlier in the list than `streamer3` and the miner can
only mine 2 channels at once.

## Running The Miner

> [!IMPORTANT]
> Remember to create a `run.py` file before attempting to run the miner.

> [!IMPORTANT]
> In order for your `cookies`, `logs`, and `analytics` to be properly persisted you must allow the miner user and
> group (997:997) read/write access.

> [!IMPORTANT]
> Please see [here](advanced-usage.md#running-the-miner) for other run options.

You can run by
using [a docker compose file](https://docs.docker.com/compose/gettingstarted/#step-2-define-services-in-a-compose-file).
The miner comes with [one](/compose.yaml) you can use. 

It defines a service called `miner` that runs the `mpforce1/twitch-channel-points-miner:latest` docker image. It opens
and exposes port `5000` which allows you to visit the analytics site in your browser by visiting
`http://localhost:5000/`. It also mounts all the possible volumes you might want to mount, although only `run.py` is
actually required.

You can get the miner started by run the following in the same directory as the compose file:

```sh
docker compose up
```

Which will run while outputting the application's logs to the current console. If you want to run in the background,
simply append ` -d` to the above command:

```sh
docker compose up -d
```

## Common Issues

### Permission Denied

When running the miner in docker you may see permission errors when the miner attempts to write to a mounted volume.
They look like this:

```PermissionError: [Errno 13] Permission denied```

This is fairly common when working with docker, the miner [Dockerfile](/Dockerfile) specifies an explicit user (`997`)
and group (`997`) to help secure your local file system against malicious actors. This differs from the original project
which allowed you to run with your local user, this is insecure because it gives a compromised container potentially
greater access to your host file system.

You may see this error because you haven't given ownership of the mounted directories (`logs`, `analytics`, `cookies`)
to the miner user/group. In order to give them ownership you can run the following:

```sh
sudo chown -R 997:997 logs analytics cookies
sudo chmod -R ug+rw logs analytics cookies
```

1. The first command changes ownership of the directories (and their contents, `-R` for recursive) to the docker miner
   user (`997`) and group (`997`).
2. The second command adds read (`r`) and write (`w`) permissions to the owning user (`u`) and group (`g`).

Most users will have to append `sudo ` to the start of those commands as non-root users cannot change file permissions.
If you're currently running as `su` then you don't have to. If you're still unable to run them it likely means your
current user doesn't have permission to use `sudo`. 
