#!/usr/bin/env python

"""Tests for `ipify_me` package."""


from ipify_me import core
from ipify_me import cli
import unittest
import sys
import re
from click.testing import CliRunner

# from ipify_me import ipify_me

sys.path.append('../')


class TestIpify_me(unittest.TestCase):
    """Tests for `ipify_me` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test the Get IP function."""
        result = core.get_ipify_ip()
        assert bool(re.match(
            '(([2]([0-4][0-9]|[5][0-5])|[0-1]?[0-9]?[0-9])[.]){3}' +
            '(([2]([0-4][0-9]|[5][0-5])|[0-1]?[0-9]?[0-9]))',
            result)) is True

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Your external IP' in result.output
