import shutil
import subprocess
import time
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional

import typer

from .utils import printer


@lru_cache()
def check_gcloud_exists():
    if shutil.which("gcloud") is None:
        gcloud_url = "https://cloud.google.com/sdk/docs/install"
        printer.fail("gcloud has to be installed first")
        printer.info(f"You can install it following the instructions at: {gcloud_url}")
        printer.info("Trying to open it in 5 seconds...")
        time.sleep(5)
        typer.launch(gcloud_url)
        raise typer.Abort()


def ensure_beta():
    check_gcloud_exists()
    printer.info("Ensuring gcloud beta is installed")
    result = subprocess.run(
        ["gcloud", "components", "install", "--quiet", "beta"],
    )
    if result.returncode != 0:
        printer.fail("There was an error installing gcloud beta")
        raise typer.Abort()
    printer.good("Done")


def get_client_email(*, service_account_name: str, project_name: str):
    client_email = f"{service_account_name}@{project_name}.iam.gserviceaccount.com"
    return client_email


app = typer.Typer()


@app.callback()
def gcp():
    """
    Sub-commands to manage Google Cloud Platform resources.

    You probably will only need the init sub-command.
    """


@app.command()
def init(
    name: Optional[str] = typer.Option(
        None, help="The name ID of the project to create in Google Cloud Platform"
    ),
    service_account_name: str = typer.Option(
        "prodigy-cluster-sa",
        help="The name of the service account to use",
    ),
):
    """
    Prepare everything to deploy a Prodigy Teams Cluster.
    """
    check_gcloud_exists()
    printer.info("Initializing...")
    project_name = create_project(name=name)
    create_service_account(
        project_name=project_name, service_account_name=service_account_name
    )
    add_service_account_member(
        project_name=project_name, service_account_name=service_account_name
    )
    setup_billing(project_name=project_name)
    enable_apis(project_name=project_name)
    create_credentials(
        project_name=project_name, service_account_name=service_account_name
    )


@app.command()
def create_project(
    name: Optional[str] = typer.Option(
        None,
        help="The name ID of the project to create in Google Cloud Platform, auto-generated if not provided",
    )
):
    """
    Create a Google Cloud project to use to deploy a Prodigy Teams cluster. Included in the init sub-command.
    """
    check_gcloud_exists()
    if name is None:
        now_seconds = int(datetime.now().timestamp())
        name = f"prodigy-{now_seconds}"
    printer.info(f"Creating Google Cloud project with ID: {name}")
    result = subprocess.run(
        [
            "gcloud",
            "projects",
            "create",
            name,
            "--name",
            "Prodigy Teams",
            "--enable-cloud-apis",
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error creating the Google Cloud project")
        raise typer.Abort()
    printer.good("Done")
    return name


@app.command()
def create_service_account(
    project_name: str = typer.Argument(
        ...,
        help="The Google Cloud project name ID that will have the Prodigy Teams cluster, needed to create the service account to manage it",
    ),
    service_account_name: str = typer.Option(
        "prodigy-cluster-sa",
        help="The name of the service account to use",
    ),
):
    """
    Create a service account that will be used to deploy the Prodigy Teams cluster.  Included in the init sub-command.
    """
    check_gcloud_exists()
    printer.info(f"Creating service account: {service_account_name}")
    result = subprocess.run(
        [
            "gcloud",
            "iam",
            "service-accounts",
            "create",
            service_account_name,
            "--display-name",
            "Prodigy Teams service account",
            "--project",
            project_name,
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error creating the service account")
        raise typer.Abort()
    printer.good("Done")
    return service_account_name


@app.command()
def add_service_account_member(
    project_name: str = typer.Argument(
        ...,
        help="The Google Cloud project name ID that will have the Prodigy Teams cluster",
    ),
    service_account_name: str = typer.Option(
        "prodigy-cluster-sa",
        help="The name of the service account to use",
    ),
):
    """
    Add a service account as the owner of the project.  Included in the init sub-command.

    This is needed to be able use the service account to deploy the Prodigy Teams cluster.
    """
    check_gcloud_exists()
    printer.info(
        f"Adding service account membership for: {service_account_name} to project: {project_name}"
    )
    client_email = get_client_email(
        service_account_name=service_account_name, project_name=project_name
    )
    result = subprocess.run(
        [
            "gcloud",
            "projects",
            "add-iam-policy-binding",
            project_name,
            "--member",
            f"serviceAccount:{client_email}",
            "--role",
            "roles/owner",
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error adding the service account membership")
        raise typer.Abort()
    printer.good("Done")
    return service_account_name


def get_billing_account():
    check_gcloud_exists()
    result = subprocess.run(
        [
            "gcloud",
            "beta",
            "billing",
            "accounts",
            "list",
            "--format",
            "value(ACCOUNT_ID)",
            "--limit=1",
        ],
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        printer.fail("There was an error getting billing accounts")
        typer.echo(result.stdout)
        typer.echo(result.stderr)
        raise typer.Abort()
    billing_account_id = result.stdout
    return billing_account_id


@app.command()
def setup_billing(
    project_name: str = typer.Argument(
        ...,
        help="The Google Cloud project name ID that will have the Prodigy Teams cluster",
    ),
):
    """
    Set up billing for the project. Included in the init sub-command.
    """
    check_gcloud_exists()
    printer.info(f"Setting up billing account for project {project_name}")
    ensure_beta()
    while True:
        billing_account_id = get_billing_account()
        if billing_account_id:
            break
        else:
            billing_url = (
                f"https://console.cloud.google.com/billing?project={project_name}"
            )
            printer.info(
                f"Before enabling the GCP APIs you have to enable billing for the project {project_name}"
            )
            printer.info(f"To do so visit {billing_url} and link a billing account")
            printer.info("Trying to open it in 5 seconds...")
            time.sleep(5)
            typer.launch(billing_url)
            typer.pause()
    printer.info(
        f"Enabling billing account id {billing_account_id} for project {project_name}"
    )
    result = subprocess.run(
        [
            "gcloud",
            "beta",
            "billing",
            "projects",
            "link",
            project_name,
            "--billing-account",
            billing_account_id,
        ],
        encoding="utf-8",
    )
    if result.returncode != 0:
        printer.fail("There was an error getting billing accounts")
        raise typer.Abort()
    printer.good("Done")


@app.command()
def enable_apis(
    project_name: str = typer.Argument(
        ...,
        help="The Google Cloud project name ID that will have the Prodigy Teams cluster",
    ),
):
    """
    Enable the required Google Cloud APIs to deploy the Prodigy Teams cluster. Included in the init sub-command.
    """
    check_gcloud_exists()
    printer.info(f"Enabling cloud APIs for project {project_name}")
    printer.info(f"Enabling cloudresourcemanager for project {project_name}")
    result = subprocess.run(
        [
            "gcloud",
            "services",
            "enable",
            "cloudresourcemanager.googleapis.com",
            "--project",
            project_name,
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error enabling cloudresourcemanager")
        raise typer.Abort()
    printer.good("Done")
    printer.info(f"Enabling sqladmin for project {project_name}")
    result = subprocess.run(
        [
            "gcloud",
            "services",
            "enable",
            "sqladmin.googleapis.com",
            "--project",
            project_name,
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error enabling sqladmin")
        raise typer.Abort()
    printer.good("Done")
    printer.info(f"Enabling compute for project {project_name}")
    result = subprocess.run(
        [
            "gcloud",
            "services",
            "enable",
            "compute.googleapis.com",
            "--project",
            project_name,
        ],
    )
    if result.returncode != 0:
        printer.fail("There was an error enabling compute")
        raise typer.Abort()
    printer.good("Done")


@app.command()
def create_credentials(
    project_name: str = typer.Argument(
        ...,
        help="The Google Cloud project name ID that will have the Prodigy Teams cluster",
    ),
    service_account_name: str = typer.Option(
        "prodigy-cluster-sa",
        help="The name of the service account to use",
    ),
):
    """
    Create credentials for the service account, to be used to deploy the Prodigy Teams cluster. Included in the init sub-command.
    """
    check_gcloud_exists()
    printer.info(
        f"Creating credentials.json file with role owner for service account: {service_account_name}"
    )
    client_email = get_client_email(
        service_account_name=service_account_name, project_name=project_name
    )
    result = subprocess.run(
        [
            "gcloud",
            "iam",
            "service-accounts",
            "keys",
            "create",
            "credentials.json",
            "--iam-account",
            client_email,
        ],
        encoding="utf-8",
    )
    if result.returncode != 0:
        printer.fail("There was an error getting creating the credentials")
        raise typer.Abort()
    credentials_path = Path("credentials.json")
    if not credentials_path.is_file():
        printer.fail("Credentials file not found")
    content = credentials_path.read_text("utf-8")
    printer.good("Done")
    printer.info(
        "Copy the content of the credentials.json file to the Prodigy Teams cluster creation wizard, or copy it from here:"
    )
    typer.echo(content)
