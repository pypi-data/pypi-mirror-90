import click

from spell.cli.utils import get_project_by_name, tabulate_rows, with_emoji, prettify_time
from spell.cli.exceptions import api_client_exception_handler


@click.group(
    name="project",
    short_help="Manage Spell Projects",
    help="Create, List, Archive and manage Projects on Spell",
    hidden=True,
)
@click.pass_context
def project(ctx):
    pass


@project.command(name="create", short_help="Create a new Project")
@click.option(
    "-n", "--name", "name", prompt="Enter a name for the project", help="Name of the project"
)
@click.option("-d", "--description", "description", help="Optional description of the project")
@click.pass_context
def create(ctx, name, description):
    proj_req = {
        "name": name,
        "description": description,
    }
    client = ctx.obj["client"]
    with api_client_exception_handler():
        client.create_project(proj_req)
    click.echo(with_emoji("💫", f"Created project '{name}'", ctx.obj["utf8"]))


@project.command(name="list", short_help="List all Projects")
@click.option(
    "--archived",
    "show_archived",
    is_flag=True,
    help="Flag to list archived projects. Default lists only unarchived projects.",
)
@click.pass_context
def list(ctx, show_archived):
    client = ctx.obj["client"]
    with api_client_exception_handler():
        projects = client.list_projects(show_archived)

    def create_row(proj):
        tup = (
            proj.name,
            proj.description,
            proj.creator.user_name,
            prettify_time(proj.created_at),
        )
        if show_archived:
            tup = (*tup, prettify_time(proj.archived_at))
        return tup

    headers = ["NAME", "DESCRIPTION", "CREATOR", "CREATED AT"]
    if show_archived:
        headers = [*headers, "ARCHIVED AT"]
    tabulate_rows(
        [create_row(proj) for proj in projects], headers=headers,
    )


@project.command(name="get", short_help="Get a Project by Name")
@click.argument("name")
@click.pass_context
def get(ctx, name):
    client = ctx.obj["client"]
    proj = get_project_by_name(client, name)

    # TODO(Benno): Have it list out all the included runs below the project details
    with api_client_exception_handler():
        proj = client.get_project(proj.id)

    def create_row(proj):
        return (
            proj.name,
            proj.description,
            proj.creator.user_name,
            proj.created_at,
        )

    tabulate_rows(
        [create_row(proj)], headers=["NAME", "DESCRIPTION", "CREATOR", "CREATED AT"],
    )


@project.command(name="add-runs", short_help="Add runs to a project")
@click.argument("project-name")
@click.argument("run-ids", type=int, nargs=-1)
@click.pass_context
def addRuns(ctx, project_name, run_ids):
    client = ctx.obj["client"]
    proj = get_project_by_name(client, project_name)
    with api_client_exception_handler():
        client.add_runs(proj.id, run_ids)
    run_str = ", ".join([str(r) for r in run_ids])
    click.echo(f"Successfully added runs {run_str} to project '{project_name}'!")


@project.command(name="remove-runs", short_help="Move runs from this project back to uncategorized")
@click.argument("project-name")
@click.argument("run-ids", type=int, nargs=-1)
@click.pass_context
def removeRuns(ctx, project_name, run_ids):
    client = ctx.obj["client"]
    proj = get_project_by_name(client, project_name)
    with api_client_exception_handler():
        client.remove_runs(proj.id, run_ids)
    run_str = ", ".join([str(r) for r in run_ids])
    click.echo(f"Successfully removed runs {run_str} from project '{project_name}'!")
