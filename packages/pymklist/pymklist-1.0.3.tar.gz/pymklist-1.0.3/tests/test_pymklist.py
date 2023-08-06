#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pymklist` package."""
import os
import zipfile

import pytest

from click.testing import CliRunner

from mklist import cli

import mock


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cwd_mock():
    with mock.patch('os.getcwd') as ctx:
        yield ctx


@pytest.fixture
def exists_mock():
    with mock.patch('os.path.exists') as ctx:
        yield ctx


def test_cli_not_valid_ldraw(cwd_mock, exists_mock, runner):
    cwd_mock.side_effect = lambda: 'invalid_dir'
    exists_mock.side_effect = lambda s: False

    result = runner.invoke(cli.main)
    assert result.exit_code == 1
    assert 'mklist' in result.output


def glob_side_effect(*args, **kwargs):
    return []


@mock.patch('mklist.cli.generate_parts_lst')
@mock.patch('glob.glob', side_effect=glob_side_effect)
def test_cli_in_valid_ldraw_dir(glob_mock, generate_parts_lst_mock,
                                cwd_mock, exists_mock, runner):
    cwd_mock.side_effect = lambda: 'ldraw'

    def exists_mock_side_effect(s):
        if s == 'parts.lst':
            return False
        return True

    exists_mock.side_effect = exists_mock_side_effect

    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not generate_parts_lst_mock.called

    result = runner.invoke(cli.main, ['--description'])
    assert result.exit_code == 0
    assert generate_parts_lst_mock.called

    result = runner.invoke(cli.main, ['--number'])
    assert result.exit_code == 0
    assert generate_parts_lst_mock.called


def test_cli_in_ldraw_dir_without_parts_dir_no(cwd_mock,
                                               exists_mock,
                                               runner):
    cwd_mock.side_effect = lambda: 'ldraw'
    exists_mock.side_effect = lambda s: False

    result = runner.invoke(cli.main)
    assert result.exit_code == 1


def mocked_retrieve(*args, **kwargs):
    return os.path.join('tests', 'test_data', 'complete.zip'), ''


def test_cli_has_help(runner):
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit' in help_result.output
