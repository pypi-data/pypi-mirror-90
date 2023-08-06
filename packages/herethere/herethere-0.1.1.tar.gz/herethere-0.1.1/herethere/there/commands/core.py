"""herethere.there.commands.core"""
import asyncio
from dataclasses import dataclass
from functools import wraps
import time
from typing import Callable, TextIO

import click

from herethere.there.client import Client


class EmptyCode(Exception):
    """Command was started without code."""


class NeedDisplay(Exception):
    """Background command was started without display."""

    def __init__(self, maxlen: int):
        self.maxlen = maxlen
        super().__init__("Display required.")


@dataclass
class ContextObject:
    """Context to pass to `there` group commands."""

    client: Client
    code: str
    stdout: TextIO = None
    stderr: TextIO = None
    background: bool = False

    def runcode(self):
        """Execute python code on the remote side."""
        if not self.code:
            raise EmptyCode("Code to execute is not specified.")
        # prepend with "\n" so error message line matches cell line number
        code = "# %%there ... \n" + self.code

        if self.background:
            asyncio.create_task(
                self.client.runcode_background(
                    code, stdout=self.stdout, stderr=self.stderr
                )
            )
        else:
            asyncio.run(
                self.client.runcode(code, stdout=self.stdout, stderr=self.stderr)
            )

    def shell(self):
        """Execute shell command on the remote side."""
        if not self.code:
            raise EmptyCode("Code to execute is not specified.")
        if self.stdout:
            asyncio.create_task(
                self.client.shell(self.code, stdout=self.stdout, stderr=self.stderr)
            )
        else:
            asyncio.run(self.client.shell(self.code))


@click.group(invoke_without_command=True)
@click.option(
    "-b", "--background", is_flag=True, default=False, help="Run in background"
)
@click.option(
    "-l",
    "--limit",
    default=24,
    type=click.IntRange(1, 1000),
    help="Number of lines to show when in background mode",
)
@click.option(
    "-d",
    "--delay",
    type=float,
    default=0,
    help="The time to wait in seconds before executing a command.",
)
@click.pass_context
def there_group(ctx, background, limit, delay):
    """Group of commands to run on remote side."""
    if background:
        if not all((ctx.obj.stdout, ctx.obj.stderr)):
            raise NeedDisplay(limit)
        ctx.obj.background = True
    if delay:
        time.sleep(delay)
    if ctx.invoked_subcommand is None:
        # Execute python code if no command specified
        ctx.obj.runcode()


@there_group.command()
@click.pass_context
def shell(ctx):
    """Execute shell command on remote side."""
    ctx.obj.shell()


@there_group.command()
@click.pass_context
@click.argument("localpaths", type=click.Path(exists=True), nargs=-1, required=True)
@click.argument("remotepath", nargs=1)
def upload(ctx, localpaths, remotepath):
    """Upload files and directories to `remotepath`."""
    if len(localpaths) == 1:
        localpaths = localpaths[0]
    asyncio.run(ctx.obj.client.upload(localpaths, remotepath))


def there_code_shortcut(
    handler: Callable[[str], str]
) -> Callable[[click.Context], None]:
    """Decorator to register %there subcommand to execute Python code."""

    @there_group.command(handler.__name__)
    @click.pass_context
    @wraps(handler)
    def _wrapper(ctx, *args, **kwargs):
        ctx.obj.code = handler(ctx.obj.code, *args, **kwargs)
        ctx.obj.runcode()

    _wrapper.__click_params__ = getattr(handler, "__click_params__", [])

    return _wrapper
