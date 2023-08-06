import sys

import click


import dada_settings
from dada_utils import dates
from dada_types.base import SerializableObject


class DadaLogger(SerializableObject):

    # An opionated, configurable moon logger for click.

    def __init__(
        self,
        name="dada",
        date_format="%-H:%M:%S",
        log_file=sys.stderr,
        out_file=sys.stdout,
        emoji=True,
        color=True,
        level=dada_settings.LOG_LEVEL,
    ):
        self.name = name
        self.date_format = date_format
        self.log_file = log_file
        self.out_file = out_file
        self.emoji = emoji
        self.color = color
        self.level = level

    @property
    def level_emoji(self):
        """"""
        if not self.emoji:
            return {}
        return {"debug": "🚧", "info": "ℹ", "warn": "⚠", "error": "❗️"}

    @property
    def level_color(self):
        """"""
        if not self.color:
            return {}
        return {
            "debug": "magenta",
            "info": "green",
            "warn": "yellow",
            "error": "red",
        }

    @property
    def out_color(self):
        """"""
        if not self.color:
            return None
        return "cyan"

    @property
    def line_emoji(self):
        """"""
        if not self.emoji:
            return {}
        return {
            0: "🌘",
            1: "🌑",
            2: "🌒",
            3: "🌓",
            4: "🌔",
            5: "🌕",
            6: "🌖",
            7: "🌗",
        }

    def format_log_msg(self, msg, level):
        """
        format a log message
        """
        self.internal_incr_counter("msg")
        cnt = self.internal_counters.get("msg")
        n_line_emoji = len(self.line_emoji.keys())
        if n_line_emoji > 0:
            line_emoji = self.line_emoji.get(cnt % n_line_emoji, "")
        else:
            line_emoji = ""
        level_emoji = self.level_emoji.get(level, "")
        return f"{line_emoji} {self.name} ({dates.now().strftime(self.date_format)}) {level_emoji} {msg}".strip()

    def debug(self, msg):
        """
        A debug message
        """
        if self.level == "debug":
            click.secho(
                self.format_log_msg(msg, "debug"),
                file=self.log_file,
                fg=self.level_color.get("debug"),
            )

    def info(self, msg):
        """
        An info message
        """
        if self.level in ["debug", "info"]:
            click.secho(
                self.format_log_msg(msg, "info"),
                file=self.log_file,
                fg=self.level_color.get("info"),
            )

    def warn(self, msg):
        """
        A warning message
        """
        if self.level in ["debug", "info", "warn"]:
            click.secho(
                self.format_log_msg(msg, "warn"),
                file=self.log_file,
                fg=self.level_color.get("warn"),
            )

    def error(self, msg):
        """
        An error message
        """
        click.secho(
            self.format_log_msg(msg, "error"),
            file=self.log_file,
            fg=self.level_color.get("error"),
        )

    # printing to stdout

    def stdout(self, val):
        """
        Print results to stdout
        """
        click.secho(val, file=self.out_file, fg=self.out_color)
