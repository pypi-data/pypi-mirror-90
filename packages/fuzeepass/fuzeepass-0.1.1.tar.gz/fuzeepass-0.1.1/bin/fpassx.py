#!/usr/bin/env python
import sys

import click
from pykeepass.exceptions import CredentialsError

from fuzeepass.passx import FuzeePass
from fuzeepass import __version__


pass_fuzeepass = click.make_pass_decorator(FuzeePass, ensure=True)


def get_stdin(ctx, param, value):
    if not value and not click.get_text_stream("stdin").isatty():
        return click.get_text_stream("stdin").read().strip()
    else:
        return value


@click.group(
    context_settings={
        "ignore_unknown_options": True,
        "help_option_names": ["-h", "--help"],
    }
)
@click.option(
    "-D",
    "--database",
    envvar="FUZEEPASS_DB",
    help="Path to .kdb(x) file. Use FUZEEPASS_DB env if database is not set",
)
@click.option(
    "-K",
    "--key-file",
    envvar="FUZEEPASS_KEY",
    help="Path to keyfile. Skip if there is no keyfile associated with the db file. "
    "Use FUZEEPASS_KEY env if key-file is not set",
)
@click.option("-P", "--password", callback=get_stdin, help="(default: read from stdin)")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, database, key_file, password):
    """
    fpassx is a command line interface to KeePassX database files
    """
    try:
        ctx.obj = FuzeePass(database, password, key_file)
    except CredentialsError:
        sys.stderr.write("[Error] Invalid password or keyfile\n")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stderr.write("Keyboard interrupted\n")
        sys.exit(130)
    except AttributeError:
        pass


@cli.command()
@pass_fuzeepass
def ls(fp):
    """
    list all uri for entries (e:) and groups (g:)
    """
    fp.ls()


@cli.command()
@click.option(
    "--uri",
    required=True,
    help="show detail for group or entry by uri",
)
@click.option(
    "+p",
    "--include-password",
    is_flag=True,
    default=False,
    help="Include password in return message.",
)
@click.option(
    "-op",
    "--only-password",
    is_flag=True,
    default=False,
    help="Show password only. Return nothing if no password",
)
@pass_fuzeepass
def show(fp, uri, include_password, only_password):
    """
    show details information for a specific uri
    """
    fp.get(uri, include_password, only_password)


@cli.command()
@click.option(
    "--uri",
    required=True,
    help="entry uri (e:)",
)
@click.option("-t", "--title")
@click.option("--url")
@click.option("-u", "--username")
@click.option("-p", "--password")
@click.option("-n", "--notes")
@pass_fuzeepass
def update_entry(fp, uri, title, url, username, password, notes):
    if not uri.startswith("e:"):
        sys.stderr.write(f"[Error] {uri} is not an entry uri\n")
        sys.exit(128)

    if not any([title, url, username, password, notes]):  # all is None
        sys.stderr.write("[Error] missing input attribute\n")
        sys.exit(128)

    fp.set(uri, title=title, url=url, username=username, password=password, notes=notes)


@cli.command()
@click.option(
    "--uri",
    required=True,
    help="group uri (g:)",
)
@click.option("--name")
@click.option("-n", "--notes")
@pass_fuzeepass
def update_group(fp, uri, name, notes):
    if not uri.startswith("g:"):
        sys.stderr.write(f"[Error] {uri} is not a group uri\n")
        sys.exit(128)

    if not any([name, notes]):  # all is None
        sys.stderr.write("[Error] missing input attribute\n")
        sys.exit(128)

    fp.set(uri, name=name, notes=notes)


@cli.command()
@click.option(
    "--group-uri",
    required=True,
    help="base group to create the new entry on",
)
@click.option("-t", "--title", required=True)
@click.option("--url")
@click.option("-u", "--username", required=True)
@click.option("-p", "--password", required=True)
@click.option("-n", "--notes")
@pass_fuzeepass
def create_entry(fp, group_uri, title, url, username, password, notes):
    if not group_uri.startswith("g:"):
        sys.stderr.write(f"[Error] {group_uri} is not a group uri\n")
        sys.exit(128)

    fp.create_entry(
        group_uri,
        title=title,
        url=url,
        username=username,
        password=password,
        notes=notes,
    )


@cli.command()
@click.option(
    "--group-uri",
    required=True,
    help="base group to create the new group on",
)
@click.option("--name", required=True)
@click.option("-n", "--notes")
@pass_fuzeepass
def create_group(fp, group_uri, name, notes):
    if not group_uri.startswith("g:"):
        sys.stderr.write(f"[Error] {group_uri} is not a group uri\n")
        sys.exit(128)

    fp.create_group(group_uri, group_name=name, notes=notes)


@cli.command()
@click.option(
    "--uri",
    required=True,
    help="uri of a group (g:) or an entry (e:)",
)
@pass_fuzeepass
def delete(fp, uri):
    """
    delete a group or an entry by uri
    """
    fp.delete(uri)


if __name__ == "__main__":
    try:
        cli()
    except TypeError:
        sys.stderr.write("[Error] Not authenticated yet\n")
        sys.exit(128)
