import os
import shutil

import pytest
from _pytest.monkeypatch import MonkeyPatch
from click.testing import CliRunner

from bin import fpassx


@pytest.fixture
def setup_db(setup_test_env):
    db_file, _, _, origin_db_file = setup_test_env
    shutil.copyfile(origin_db_file, db_file)
    yield
    os.remove(db_file)


@pytest.fixture(scope="module")
def runner(setup_test_env):
    db_file, password, key_file, _ = setup_test_env

    monkeymodule = MonkeyPatch()
    monkeymodule.setenv("FUZEEPASS_DB", db_file)
    monkeymodule.setenv("FUZEEPASS_KEY", key_file)

    yield CliRunner(), password

    monkeymodule.undo()


def test_ls(setup_db, runner):
    cli, password = runner
    result = cli.invoke(fpassx.cli, ["--password", password, "ls"])
    assert result.exit_code == 0
    assert result.output.split("\n") == [
        "e:work/awssss",
        "e:work/cgp",
        "e:work/aws",
        "e:work/azure",
        "e:work/nopass",
        "e:work/coding/github",
        "e:work/coding/gitlab",
        "e:personal/twitter",
        "e:personal/spotify f",
        "e:personal/email/yahoo",
        "e:personal/email/gmail",
        "g:/",
        "g:work/",
        "g:work/coding/",
        "g:personal/",
        "g:personal/email/",
        "",
    ]


def test_ls2(setup_db, runner):
    cli, password = runner
    result = cli.invoke(fpassx.cli, ["ls"])
    assert result.exit_code == 1
    assert result.output == "[Error] Invalid password or keyfile\n"


@pytest.fixture(
    params=[
        (
            ("e:work/coding/github",),
            [
                "[Entry Info]",
                "path      : work/coding/github",
                "title     : github",
                "url       : https://github.com",
                "username  : gg",
                "notes     : gg1",
                "",
            ],
        ),
        (
            ("e:work/coding/github", "+p"),
            [
                "[Entry Info]",
                "path      : work/coding/github",
                "title     : github",
                "url       : https://github.com",
                "username  : gg",
                "password  : github1",
                "notes     : gg1",
                "",
            ],
        ),
        (("e:work/coding/github", "-op"), ["github1"]),
        (
            ("g:personal/email/",),
            [
                "[Group Info]",
                "path      : personal/email/",
                "name      : email",
                "notes     : email credentials",
                "",
            ],
        ),
        (
            ("g:personal/email/", "+p"),
            [
                "[Group Info]",
                "path      : personal/email/",
                "name      : email",
                "notes     : email credentials",
                "",
            ],
        ),
        (("g:personal/email/", "-op"), [""]),
    ]
)
def setup_show(request, setup_db):
    return request.param


def test_show(runner, setup_show):
    cli, password = runner
    options, expected_output = setup_show
    result = cli.invoke(fpassx.cli, ["-P", password, "show", "--uri", *options])
    assert result.exit_code == 0
    assert result.output.split("\n") == expected_output


@pytest.fixture(
    params=[
        (
            "update-entry",
            "e:personal/spotify f",
            ("-t", "spotify family", "-p", "123abc", "-n", "note something"),
            "e:personal/spotify family",
            [
                "[Entry Info]",
                "path      : personal/spotify family",
                "title     : spotify family",
                "url       : https://spotify.com",
                "username  : spt",
                "password  : 123abc",
                "notes     : note something",
                "",
            ],
        ),
        (
            "update-entry",
            "e:work/aws",
            ("--url", "https://aws.amazon.com/console/", "-p", "kamaxuta"),
            None,
            [
                "[Entry Info]",
                "path      : work/aws",
                "title     : aws",
                "url       : https://aws.amazon.com/console/",
                "username  : awsx",
                "password  : kamaxuta",
                "notes     : test2",
                "",
            ],
        ),
        (
            "update-group",
            "g:personal/",
            ("-n", "sample note"),
            None,
            [
                "[Group Info]",
                "path      : personal/",
                "name      : personal",
                "notes     : sample note",
                "",
            ],
        ),
        (
            "update-group",
            "g:personal/email",
            ("--name", "e-mail", "-n", "e-mail login info"),
            "g:personal/e-mail",
            [
                "[Group Info]",
                "path      : personal/e-mail/",
                "name      : e-mail",
                "notes     : e-mail login info",
                "",
            ],
        ),
    ]
)
def setup_update(request, setup_db):
    return request.param


def test_update(runner, setup_update):
    cli, password = runner
    command, uri, options, new_uri, expected_output = setup_update
    if new_uri is None:
        new_uri = uri
    update_result = cli.invoke(
        fpassx.cli, ["-P", password, command, "--uri", uri, *options]
    )
    assert update_result.exit_code == 0

    result = cli.invoke(fpassx.cli, ["-P", password, "show", "--uri", new_uri, "+p"])
    assert result.exit_code == 0
    assert result.output.split("\n") == expected_output


@pytest.fixture(
    params=[
        (
            "update-entry",
            "g:personal/",
            ("-t", "spotify family", "-p", "123abc", "-n", "note something"),
            128,
            "[Error] g:personal/ is not an entry uri\n",
        ),
        (
            "update-entry",
            "e:work/aws",
            (),
            128,
            "[Error] missing input attribute\n",
        ),
        (
            "update-group",
            "e:work/aws",
            ("-n", "sample note"),
            128,
            "[Error] e:work/aws is not a group uri\n",
        ),
        (
            "update-group",
            "g:personal/email",
            (),
            128,
            "[Error] missing input attribute\n",
        ),
    ]
)
def setup_update2(request, setup_db):
    return request.param


def test_update2(runner, setup_update2):
    cli, password = runner
    command, uri, options, exit_code, msg = setup_update2
    result = cli.invoke(fpassx.cli, ["-P", password, command, "--uri", uri, *options])
    assert result.exit_code == exit_code
    assert result.output == msg


@pytest.fixture(
    params=[
        (
            "create-group",
            "g:personal/",
            ("--name", "bank", "-n", "Internet banking acc"),
            "g:personal/bank",
            [
                "[Group Info]",
                "path      : personal/bank/",
                "name      : bank",
                "notes     : Internet banking acc",
                "",
            ],
        ),
        (
            "create-entry",
            "g:personal/",
            (
                "-t",
                "chase",
                "-u",
                "c01",
                "-p",
                "123456",
                "--url",
                "https://www.chase.com",
            ),
            "e:personal/chase",
            [
                "[Entry Info]",
                "path      : personal/chase",
                "title     : chase",
                "url       : https://www.chase.com",
                "username  : c01",
                "password  : 123456",
                "notes     : ",
                "",
            ],
        ),
    ]
)
def setup_create(request, setup_db):
    return request.param


def test_create(runner, setup_create):
    cli, password = runner
    command, group_uri, options, uri, expected_output = setup_create
    create_result = cli.invoke(
        fpassx.cli, ["-P", password, command, "--group-uri", group_uri, *options]
    )
    assert create_result.exit_code == 0

    result = cli.invoke(fpassx.cli, ["-P", password, "show", "--uri", uri, "+p"])
    assert result.exit_code == 0
    assert result.output.split("\n") == expected_output


@pytest.fixture(
    params=[
        (
            "create-entry",
            "e:personal/",
            (
                "-t",
                "chase",
                "-u",
                "c01",
                "-p",
                "123456",
                "--url",
                "https://www.chase.com",
            ),
            128,
            "[Error] e:personal/ is not a group uri\n",
        ),
        (
            "create-group",
            "e:work/aws",
            ("--name", "abc", "-n", "sample note"),
            128,
            "[Error] e:work/aws is not a group uri\n",
        ),
    ]
)
def setup_create2(request, setup_db):
    return request.param


def test_create2(runner, setup_create2):
    cli, password = runner
    command, group_uri, options, exit_code, msg = setup_create2
    result = cli.invoke(
        fpassx.cli, ["-P", password, command, "--group-uri", group_uri, *options]
    )
    assert result.exit_code == exit_code
    assert result.output == msg


def test_delete(runner, setup_db):
    cli, password = runner
    d1 = cli.invoke(fpassx.cli, ["-P", password, "delete", "--uri", "g:work/coding/"])
    assert d1.exit_code == 0

    d2 = cli.invoke(
        fpassx.cli, ["-P", password, "delete", "--uri", "e:personal/email/yahoo"]
    )
    assert d2.exit_code == 0

    result = cli.invoke(fpassx.cli, ["-P", password, "ls"])
    assert result.exit_code == 0
    assert result.output.split("\n") == [
        "e:work/awssss",
        "e:work/cgp",
        "e:work/aws",
        "e:work/azure",
        "e:work/nopass",
        "e:personal/twitter",
        "e:personal/spotify f",
        "e:personal/email/gmail",
        "g:/",
        "g:work/",
        "g:personal/",
        "g:personal/email/",
        "",
    ]
