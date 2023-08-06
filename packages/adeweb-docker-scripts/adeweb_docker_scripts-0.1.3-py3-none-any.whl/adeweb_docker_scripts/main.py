import humanize
import typer
from docker.models.containers import Container
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime
import docker
import subprocess

app = typer.Typer()


@app.command()
def ls():
    """
    List all active containers
    """
    console = Console()
    client = docker.from_env()
    containers = client.containers.list()
    _print_containers_table(console, containers)


@app.command()
def sh(
    name: str = typer.Argument(..., help="Approximate container name"),
    shell_path: str = typer.Argument("/bin/sh", help="shell path inside the container"),
):
    """
    Jump into container shellssss
    """
    console = Console()
    client = docker.from_env()
    containers = client.containers.list()
    found_containers = []
    for container in containers:
        if name in container.attrs["Name"]:
            found_containers.append(container)

    if len(found_containers) == 0:
        print("[bold red]Container not found[/bold red]")
        print("Running containers :")
        _print_containers_table(console, containers)
        input_name = Prompt.ask("Please specify which one you want :")
        sh(input_name, shell_path)
        return
    elif len(found_containers) > 1:
        print(f"[bold dark_orange]Multiple containers with similar name ({name}) : [/bold dark_orange]")
        _print_containers_table(console, found_containers)
        input_name = Prompt.ask("Please specify which one you want :", default=found_containers[0].attrs["Name"])
        sh(input_name, shell_path)
        return

    container: Container = found_containers[0]
    p = subprocess.Popen(["docker", "exec", "-it", container.attrs["Config"]["Hostname"], str(shell_path)])
    p.communicate()


def _print_containers_table(console: Console, containers: list):
    table = Table(show_header=True, header_style="bold")
    table.add_column("container ID", width=12)
    table.add_column("Image", width=45)
    table.add_column("Status", width=20)
    table.add_column("Name")

    for container in containers:
        table.add_row(
            container.attrs["Config"]["Hostname"],
            container.attrs["Config"]["Image"],
            "Up "
            + humanize.naturaldelta(
                datetime.now()
                - datetime.strptime(container.attrs["State"]["StartedAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
            ),
            container.attrs["Name"],
        )
    console.print(table)
