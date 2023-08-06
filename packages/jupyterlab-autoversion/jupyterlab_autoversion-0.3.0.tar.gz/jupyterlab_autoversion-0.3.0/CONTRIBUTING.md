# Contributing

If you want to contribute to this repository here are some helpful guidelines.

## Reporting bugs, feature requests, etc.

To report bugs, request new features or similar, please open an issue on the Github
repository.

A good bug report includes:

- Expected behavior
- Actual behavior
- Steps to reproduce (preferably as minimal as possible)
- Possibly any output from the browser console (typically available via Ctrl + Shift + J or via F12).

## Minor changes, typos etc.

Minor changes can be contributed by navigating to the relevant files on the Github repository,
and clicking the "edit file" icon. By following the instructions on the page you should be able to
create a pull-request proposing your changes. A repository maintainer will then review your changes,
and either merge them, propose some modifications to your changes, or reject them (with a reason for
the rejection).

## Setting up a development environment

If you want to help resolve an issue by making some changes that are larger than that covered by the above paragraph, it is recommended that you:

- Fork the repository on Github
- Clone your fork to your computer
- Run the following commands inside the cloned repository:
  - `pip install -e .[dev]` - This will install the Python package in development
    mode.
  - `jupyter labextension install .` - This will add the lab extension in development
    mode.
  - `jupyter serverextension enable --py jupyterlab_autoversion` - This will enable the server extension.

For convenience, you can use the scripts in our Makefile

```bash
# at the root of jupyterlab_autoversion repo
make dev_install
```

- Validate the install by running the tests:
  - `py.test` - This command will run the Python tests.
  - `yarn test` - This command will run the JS tests.

Once you have such a development setup, you should:

- Make the changes you consider necessary
- Run the tests to ensure that your changes does not break anything
- If you add new code, preferably write one or more tests for checking that your code works as expected.
- Commit your changes and publish the branch to your github repo.
- Open a pull-request (PR) back to the main repo on Github.


## Debug Python and Typescript code using vscode

vscode is able to debug both the Python and Typescript sections of this project, and can do so in a single run. However, vscode will first require a specific launch config before you can debug with it. You can create this launch config by first running

```bash
make init_debug
```

and then editing the resulting `.vscode/launch.json` and `.vscode/jupyterlab_venv.env` files as needed

# Releasing

To make a new release of jupyterlab_autoversion:

1. `bumpversion patch` (replacing `patch` with whatever is appropriate for the current release, e.g. `minor`, `major`, etc) - This will also create a git commit and tag.
2. `git push --follow-tags` - This will trigger python and npm package builds on azure, and upload to [our azure feed](https://dev.azure.com/tpaine154/jupyter/_packaging?_a=feed&feed=python-packages).
3. Check the resulting packages:
  - Install and test in a clean environment:
    - You can install for python with `pip install --index-url=https://pkgs.dev.azure.com/tpaine154/jupyter/_packaging/python-packages/pypi/simple/ jupyterlab_autoversion==<version> --extra-index-url=https://pypi.org/simple`, modifying as appropriate to use the wheel or the sdist, and to install the version you want to test.
    - Download the jupyterlab_autoversion npm package from [our azure feed](https://dev.azure.com/tpaine154/jupyter/_packaging?_a=feed&feed=python-packages) and then install with `jupyter labextension install /path/to/jupyterlab_autoversion-<version>.tgz` (replacing the filename with whatever you downloaded).
  - Inspect the sdist, wheel, and npm tgz to make sure they contain the right files, version numbers, etc.
4. Once satisfied, use `bumpversion` either to set or increment `release` to `final` (e.g.  `bumpversion release`), and then grab the resulting releases from azure and upload to pypi and npm.
