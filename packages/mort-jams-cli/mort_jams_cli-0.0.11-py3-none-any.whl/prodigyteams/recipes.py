import json
import tarfile
from pathlib import Path
from zipfile import ZipFile

import typer

from . import packages
from .utils import dicts_to_table, get_broker_pip_credentials, normalize_module, printer

# TODO: Test all this if this approach works correctly

app = typer.Typer()


@app.callback()
def recipes():
    """
    Sub-commands for recipes.
    """


@app.command()
def new(
    name: Path = typer.Argument(
        ..., help="Recipes package name, e.g. custom_recipes", exists=False
    ),
    version: str = typer.Option(
        "0.1.0", help="The version of the Python package with the recipes"
    ),
    description: str = typer.Option("", help="Python package description"),
    author: str = typer.Option("", help="Python package author"),
    email: str = typer.Option("", help="Python package author email"),
    url: str = typer.Option("", help="Python package URL"),
    licence: str = typer.Option("", help="Python package license"),
):
    """
    Generate a new Prodigy Teams Recipe directory with a custom package.
    """
    package_name = normalize_module(name.name)
    package_path = name / package_name
    package_path.mkdir(parents=True)
    setup_path = name / "setup.py"
    setup_path.write_text(TEMPLATE_SETUP, encoding="utf-8")
    init_path = package_path / "__init__.py"
    init_path.write_text(TEMPLATE_INIT, encoding="utf-8")
    recipes_path = package_path / "recipes.py"
    recipes_path.write_text(TEMPLATE_RECIPES, encoding="utf-8")
    readme_path = name / "README.md"
    readme_path.write_text(TEMPLATE_README, encoding="utf-8")
    dev_requirements_path = name / "dev-requirements.txt"
    dev_requirements_path.write_text(TEMPLATE_DEV_REQUIREMENTS, encoding="utf-8")
    gitignore_path = name / ".gitignore"
    gitignore_path.write_text(TEMPLATE_GITIGNORE, encoding="utf-8")
    auth_requirements_path = name / "auth-requirements.txt"
    credentials = get_broker_pip_credentials()
    username = credentials["username"]
    password = credentials["password"]
    hostname = credentials["hostname"]
    auth_requirements_content = TEMPLATE_AUTH_REQUIREMENTS.format(
        username=username, password=password, hostname=hostname
    )
    auth_requirements_path.write_text(auth_requirements_content, encoding="utf-8")
    meta_path = package_path / "meta.json"
    meta_data = {
        "name": package_name,
        "version": version,
        "description": description,
        "author": author,
        "email": email,
        "url": url,
        "license": licence,
        "type": "prodigy_teams_recipes",
        "prodigy_teams_recipes": {},
    }
    meta_path.write_text(json.dumps(meta_data, indent=4), encoding="utf-8")
    printer.good(f"Successfully created project {name.name}")
    printer.divider("README")
    printer.info("You can now read and follow the generated README.md file")


@app.command()
def verify(
    package: Path = typer.Argument(
        ..., help="The recipes package file to verify", exists=True, dir_okay=False
    )
):
    """
    Verify a Prodigy Teams Recipe built Python package before upload.
    """
    if not (package.name.endswith("tar.gz") or package.name.endswith(".whl")):
        printer.fail(
            "It seems this is not a Python package, it should end in .tar.gz or .whl"
        )
        raise typer.Abort()
    file_name = ""
    meta_json = None
    valid_meta = False
    if package.name.endswith(".whl"):
        with ZipFile(package) as zip_file:
            for file_name in zip_file.namelist():
                if file_name.endswith("/meta.json"):
                    meta_bytes = zip_file.read(file_name)
                    meta_json = json.loads(meta_bytes.decode("utf-8"))
                    if not isinstance(meta_json, dict):
                        continue
                    if meta_json.get("type") == "prodigy_teams_recipes":
                        valid_meta = True
                        break
    elif package.name.endswith(".tar.gz"):
        with tarfile.open(package) as tar:
            for file_name in tar.getnames():
                if file_name.endswith("/meta.json"):
                    io_bytes = tar.extractfile(file_name)
                    assert io_bytes
                    meta_json = json.load(io_bytes)
                    if not isinstance(meta_json, dict):
                        continue
                    if meta_json.get("type") == "prodigy_teams_recipes":
                        valid_meta = True
                        break
    if not (valid_meta and meta_json):
        printer.fail("No valid meta.json found in packaage")
        raise typer.Exit(1)
    printer.good(f"Found valid meta.json in package: {file_name}")
    recipes_data = meta_json.get("prodigy_teams_recipes", {})
    if not isinstance(recipes_data, dict):
        printer.fail("Invalid meta.json key prodigy_teams_recipes")
        raise typer.Exit(1)
    if not recipes_data:
        printer.fail(
            "No custom recipes found, make sure you install prodigy_teams_recipes and prodigy in your venv, and then make sure you run python setup.py sdist bdist_wheel"
        )
        raise typer.Exit(1)
    recipes_info = []
    valid_recipes = True
    for key, data in recipes_data.items():
        entry_point = data.get("entry_point")
        recipe_schema = data.get("recipe_schema")
        recipes_info.append(
            {
                "name": key,
                "entry_point": entry_point,
                "contains schema": bool(recipe_schema),
            }
        )
        if not entry_point or not recipe_schema:
            valid_recipes = False
    headers, rows = dicts_to_table(recipes_info)
    printer.good("Custom recipes found!")
    printer.table(rows, header=headers, divider=True, max_col=3000)
    if not valid_recipes:
        printer.fail("One or more recipes are not valid")
        raise typer.Exit(1)
    printer.good("Valid recipes package!")


@app.command()
def add(package: typer.FileBinaryRead, allowoverwrite: bool = False):
    """
    Add/upload a recipe package from the local filesystem.

    It should be a valid file in your local file system,
    it will also be validated and indexed by your broker's Python Package Index.
    """
    package_path = Path(package.name)
    verify(package=package_path)
    packages.add(package=package, allowoverwrite=allowoverwrite)


TEMPLATE_SETUP = """
#!/usr/bin/env python3
import importlib
import json
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist


def update_meta(*, package_name: str, meta: dict, meta_path: Path):
    try:
        importlib.import_module(package_name)
        from prodigy_teams_recipes.decorator import get_custom_meta

        custom_meta = get_custom_meta()
        meta.update(custom_meta)
        meta_path.write_text(json.dumps(meta, indent=4), encoding="utf-8")
    except ModuleNotFoundError:
        message = (
            "prodigy_teams_recipes not available, make sure you install it "
            "from your cluster before building the package"
        )
        print(message)
        raise RuntimeError(message)


def get_meta_path():
    root = Path(__file__).parent.resolve()
    meta_path = None
    for sub_path in root.iterdir():
        if sub_path.is_dir():
            meta_path = sub_path / "meta.json"
            if meta_path.is_file():
                break
    assert meta_path
    return meta_path


def get_meta():
    meta_path = get_meta_path()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return meta


def get_entrypoints():
    meta = get_meta()
    recipes: dict = meta["prodigy_teams_recipes"]
    recipe_entry_points = []
    for recipe_name, recipe_data in recipes.items():
        recipe_entry_point = recipe_data["entry_point"]
        recipe_entry_points.append(f"{recipe_name} = {recipe_entry_point}")
    return {"prodigy_teams_recipes": recipe_entry_points}


def setup_package():
    meta_path = get_meta_path()
    meta = get_meta()
    package_name = meta["name"]
    # Custom sdist and bdist_wheel commands that auto-generate the required meta.json
    # and update the entry_points
    class CustomSdist(sdist):
        def run(self):
            update_meta(package_name=package_name, meta=meta, meta_path=meta_path)
            entry_points = get_entrypoints()
            self.distribution.entry_points = entry_points
            sdist.run(self)

    try:
        from wheel.bdist_wheel import bdist_wheel

        class CustomBdistWheel(bdist_wheel):
            def run(self):
                update_meta(package_name=package_name, meta=meta, meta_path=meta_path)
                entry_points = get_entrypoints()
                self.distribution.entry_points = entry_points
                bdist_wheel.run(self)

    except (ModuleNotFoundError, ImportError):
        from setuptools import Command

        message = "Coudn't find wheel package, make sure you install it with: pip install -U wheel"
        print(message)

        class CustomBdistWheel(sdist):
            def run(self) -> None:
                print(message)
                raise RuntimeError(message)

    setup(
        name=package_name,
        description=meta.get("description"),
        author=meta.get("author"),
        author_email=meta.get("email"),
        url=meta.get("url"),
        version=meta["version"],
        license=meta.get("license"),
        packages=find_packages(),
        package_data={package_name: ["meta.json"]},
        install_requires=["prodigy_teams_recipes>=0.0.5<0.0.6"],
        zip_safe=False,
        cmdclass={"sdist": CustomSdist, "bdist_wheel": CustomBdistWheel},
    )


if __name__ == "__main__":
    setup_package()
""".lstrip()


TEMPLATE_RECIPES = """
from mort_jams import UISchemaConfig
from prodigy.components.loaders import get_stream
from prodigy_teams_recipes import fields
from prodigy_teams_recipes.db import DB
from prodigy_teams_recipes.decorator import resolve_source, teams_recipe
from prodigy_teams_recipes.schemas import Recipe


class CustomRecipe(Recipe):
    class Config:
        title = "A Sample Custom Recipe"
        ui = UISchemaConfig(
            order=[
                "type",
                "input",
                "name",
                "label",
                "model",
                "*",
            ],
        )

    input: fields.InputType = fields.input
    label: fields.LabelType = fields.label
    model: fields.ModelType = fields.model


@teams_recipe("custom_recipe")
def custom_recipe(recipe: CustomRecipe):
    source, loader = resolve_source(recipe.input)
    stream = get_stream(source, loader=loader, rehash=True, dedup=True)
    return {
        "db": DB,
        "dataset": recipe.dataset,
        "stream": stream,
        "view_id": "classification",
    }
""".lstrip()


TEMPLATE_INIT = """
from . import recipes
""".lstrip()

TEMPLATE_README = """
# Prodigy Teams Recipes

This project contains a Python package with custom Prodigy Teams recipes.

## Python environment

You can now create a new Python environment for this project, for example with:

```console
$ python3 -m venv env
```

Make sure you are using Python 3.6 or above.

Then you will be able to activate this environment with:

```console
$ source ./env/bin/activate
```

...or equivalent, depending on your system.

Then, after activating your environment, you should upgrade the `pip` version:

```console
$ python -m pip install --upgrade pip
```

## Install dependencies

After activating the environment and upgrading `pip`, you can now install the development dependencies that are needed to build the Python package:

```console
$ python -m pip install --upgrade -r dev-requirements.txt -r auth-requirements.txt
```

`dev-requirements.txt` includes:

```
setuptools
wheel
prodigy-teams-recipes
```

The package `prodigy-teams-recipes` is needed to generate the file called `meta.json` while building your custom recipe's package.

`auth-requirements.txt` is used to configure the authentication to your cluster's PyPI so that `pip` can install `prodigy-teams-recipes` from it.

## Edit

You can edit the custom recipes in `recipes.py`.

If you add other Python modules (files) make sure you import them from `__init__.py`.

## Build

Once you have your Prodigy Teams recipes ready, you can create a Python "distributable" package with:

```console
$ python setup.py sdist bdist_wheel
```

This will update the required `meta.json` file right before building the package.

## Upload

After building the package you can upload it to your Prodigy Teams cluster with:

```console
$ ptc recipes add ./dist/your_custom_recipe-0.1.0-py3-none-any.whl

✔ Found valid meta.json in package: your_custom_recipe/meta.json
✔ Custom recipes found!

name            entry_point                       contains schema
-------------   -------------------------------   ---------------
custom_recipe   your_custom_recipe.recipes:custom_recipe   True

✔ Valid recipes package!
Uploading package file dist/your_custom_recipe-0.1.0-py3-none-any.whl.
Package successfully added.
```

## Verify

You can also verify the built package without uploading it with:

```console
$ ptc recipes verify ./dist/your_custom_recipe-0.1.0-py3-none-any.whl

✔ Found valid meta.json in package: my_recipe/meta.json
✔ Custom recipes found!

name            entry_point                       contains schema
-------------   -------------------------------   ---------------
custom_recipe   my_recipe.recipes:custom_recipe   True

✔ Valid recipes package!
```
""".lstrip()


TEMPLATE_DEV_REQUIREMENTS = """
setuptools
wheel
prodigy-teams-recipes
""".lstrip()


TEMPLATE_AUTH_REQUIREMENTS = """
--extra-index-url https://{username}:{password}@{hostname}/api/pip/
""".lstrip()


TEMPLATE_GITIGNORE = """
*.egg-info
__pycache__
*.pyc
env
build
dist
auth-requirements.txt
""".lstrip()
