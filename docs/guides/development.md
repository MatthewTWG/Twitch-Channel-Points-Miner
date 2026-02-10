# Development

> [!NOTE]
> We welcome most contributions to this project, please read [contributing](/docs/CONTRIBUTING.md) before getting started.

## Tools

Feel free to use whatever development tools you like! At a minimum you'll need `python >= 3.12` with all the
dependencies from the [pyproject.toml](/pyproject.toml) file installed. You'll need:

1. `Python 3.12`, you can try developing with later versions but this is the target version so you won't be able to use
   later features.
2. [uv](https://docs.astral.sh/uv/getting-started/installation/), this is the package manager used by the project.
   Once installed you can run `uv sync` to ensure your local python installation has the required packages installed.
3. While technically optional, ideally you'll run in [Docker](https://docs.docker.com/engine/install/) so you'll need
   that available too.

## Adding New Dependencies

Please use [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/#adding-dependencies) to add new dependencies,
rather than manually editing the `pyproject.toml` file, by running:

```sh
uv add [dependency name]
```

When adding dependencies that don't need to used in production (like `pytest`) please add them
as [development dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies) by running:

```sh
uv add --dev [dependency name]
```

You can also constrain dependencies to specific versions and platforms so please read the `uv` docs for more
information.

## Running

### Docker Compose

When developing for the application we recommend you run via the [develop compose](/develop-compose.yaml) file. This
will help ensure:

1. The running code is secured/isolated from your local filesystem
2. Your changes are run in a consistent environment.

### Locally

> [!WARNING]
> This is not recommend due to security considerations.

If you want to run your changes locally you can make a local `run.py` file and just run that with `python3 run.py` or
`python run.py` depending on your aliasing. You can run `python3 --version` or `python --version` to see which command
points to the right python version.

## Testing

> [!IMPORTANT]
> Please read the [pytest](https://docs.pytest.org/en/stable/) documentation before running/writing tests.

At a minimum you should run all [tests](/tests) using `pytest` before pushing your changes. This is to help ensure that
your changes don't cause a regression in miner behaviour.

If your changes alter the miner's behaviour then you should update all relevant test cases.

If your changes create new behaviour(s), please create new tests to cover the behaviour(s). When creating new test
files, please follow the filename conventions already in place. For example, if you create a file called
`TwitchChannelPointsMiner/classes/Feature.py` then tests for this should go in a new file called
`tests/classes/test_feature.py`.

Ideally, you should also run a long term live test. Depending on the scale of the change, this could be anywhere from a
few minutes to a week. For example, changing how logs are printed might only need to be tested until you see the logs
are printed as you expect. However, changing aspects of how the WebSockets work would require live testing until you can
verify things like reconnection works as expected, which might be hours to days (depending on how Twitch feels 😄).