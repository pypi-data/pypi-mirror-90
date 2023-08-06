# Prodigy Teams CLI

The Command Line Interface program for **Prodigy Teams**.

## Prerequisites

Before using Prodigy Teams CLI you need to have a **Prodigy Teams** account.

You also need a deployed broker cluster.

You will also need Python 3.6+ in your system.

## Install

Make sure you have a Python version 3.6 or above:

```console
$ python --version

# or

$ python3.6 --version

# or

$ python3.7 --version

# etc
```

Install with Python (using the same `python` version 3.6 or above, as selected above):

```console
$ python -m pip install prodigy-teams-cli
```

Then in your terminal you will have a `ptc` program/command:

```console
$ ptc --help

Usage: ptc [OPTIONS] COMMAND [ARGS]...

  Prodigy Teams Command Line Interface.

  More info at https://prodi.gy/

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  login     Login to your Prodigy Teams.
  packages  Sub-commands to interact with packages (including models).
  projects  Sub-commands to interact with projects.
  sources   Sub-commands for sources.
  tasks     Sub-commands to interact with tasks.
```

If you want to have completion in your terminal (for Bash, Zsh, Fish, or PowerShell) run:

```console
$ ptc --install-completion

bash completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

After that, re-start your terminal, and you will have completion for all the subcommands and options when you hit <kbd>TAB</kbd>.

## Extensive docs

## `ptc`

Prodigy Teams Command Line Interface.

More info at https://prodi.gy/

**Usage**:

```console
$ ptc [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `login`: Login to your Prodigy Teams.
* `packages`: Sub-commands to interact with packages...
* `projects`: Sub-commands to interact with projects.
* `sources`: Sub-commands for sources.
* `tasks`: Sub-commands to interact with tasks.

## `ptc login`

Login to your Prodigy Teams.

You normally don't need to call this manually.
It will automatically authenticate when needed.

**Usage**:

```console
$ ptc login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `ptc packages`

Sub-commands to interact with packages (including models).

**Usage**:

```console
$ ptc packages [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a package from the local filesystem.
* `delete`: Delete a package.
* `download`: Download a package to the current directory.
* `list`: List all the packages including built-ins.
* `list-package`: List all the binary files for a package.

### `ptc packages add`

Add a package from the local filesystem.

It should be a valid file in your local file system,
it will also be validated and indexed by your broker's Python Package Index.

**Usage**:

```console
$ ptc packages add [OPTIONS] PACKAGE
```

**Options**:

* `--allowoverwrite / --no-allowoverwrite`
* `--help`: Show this message and exit.

### `ptc packages delete`

Delete a package.

**Usage**:

```console
$ ptc packages delete [OPTIONS] PACKAGE
```

**Options**:

* `--force / --no-force`: Force deletion without confirmation
* `--help`: Show this message and exit.

### `ptc packages download`

Download a package to the current directory.

**Usage**:

```console
$ ptc packages download [OPTIONS] PACKAGE FILENAME
```

**Options**:

* `--help`: Show this message and exit.

### `ptc packages list`

List all the packages including built-ins.

**Usage**:

```console
$ ptc packages list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `ptc packages list-package`

List all the binary files for a package.

**Usage**:

```console
$ ptc packages list-package [OPTIONS] PACKAGE
```

**Options**:

* `--help`: Show this message and exit.

## `ptc projects`

Sub-commands to interact with projects.

**Usage**:

```console
$ ptc projects [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all the projects.

### `ptc projects list`

List all the projects.

**Usage**:

```console
$ ptc projects list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `ptc sources`

Sub-commands for sources.

**Usage**:

```console
$ ptc sources [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add a source from local filesystem.
* `delete`: Delete a source.
* `list`: List all the sources.

### `ptc sources add`

Add a source from local filesystem.

It should be a valid file in your local system,
it will be uploaded to your cluster.

**Usage**:

```console
$ ptc sources add [OPTIONS] SOURCE
```

**Options**:

* `--allowoverwrite / --no-allowoverwrite`
* `--help`: Show this message and exit.

### `ptc sources delete`

Delete a source.

**Usage**:

```console
$ ptc sources delete [OPTIONS] SOURCE
```

**Options**:

* `--force / --no-force`: Force deletion without confirmation
* `--help`: Show this message and exit.

### `ptc sources list`

List all the sources.

**Usage**:

```console
$ ptc sources list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `ptc tasks`

Sub-commands to interact with tasks.

**Usage**:

```console
$ ptc tasks [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all the tasks.

### `ptc tasks list`

List all the tasks.

**Usage**:

```console
$ ptc tasks list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
