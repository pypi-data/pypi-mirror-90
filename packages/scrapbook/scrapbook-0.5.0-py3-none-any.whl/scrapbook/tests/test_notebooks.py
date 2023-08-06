#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import pytest
import collections
import json

import pandas as pd

from pandas.util.testing import assert_frame_equal
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell, new_output

from . import get_notebook_path, get_notebook_dir
from .. import read_notebook, utils
from ..models import Notebook
from ..exceptions import ScrapbookException

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


@pytest.fixture(scope='session', autouse=True)
def kernel_mock():
    """Mocks the kernel to capture warnings during testing"""
    with mock.patch.object(utils, 'is_kernel') as _fixture:
        yield _fixture


class AnyDict(object):
    def __eq__(self, other):
        return isinstance(other, dict)


@pytest.fixture
def notebook_result():
    path = get_notebook_path("collection/result1.ipynb")
    return read_notebook(path)


@pytest.fixture
def notebook_backwards_result():
    path = get_notebook_path("record.ipynb")
    return read_notebook(path)


def test_bad_path():
    with pytest.raises(FileNotFoundError):
        Notebook("not/a/valid/path.ipynb")


def test_bad_ext():
    with pytest.raises(Warning):
        Notebook("not/a/valid/extension.py")


@mock.patch("papermill.iorw.papermill_io.read")
def test_good_ext_for_url(mock_read):
    sample_output = {
        "cells": [
            {"cell_type": "code", "execution_count": 1, "metadata": {}, "outputs": [], "source": []}
        ]
    }

    mock_read.return_value = json.dumps(sample_output)

    params = "?sig=some-unique-secret-token"
    url = "abs://mystorage.blob.core.windows.net/my-actual-notebook.ipynb" + params

    Notebook(url)

    mock_read.assert_called_once()


def test_bad_ext_for_url():
    with pytest.raises(Warning):
        params = "?sig=some-unique-secret-token"
        url = "abs://mystorage.blob.core.windows.net/my-actual-notebook.txt" + params
        Notebook(url)


def test_filename(notebook_result):
    assert notebook_result.filename == "result1.ipynb"


def test_directory(notebook_result):
    assert notebook_result.directory == get_notebook_dir("collection/result1.ipynb")


def test_parameters(notebook_result):
    assert notebook_result.parameters == dict(foo=1, bar="hello")


def test_data_scraps(notebook_result):
    assert notebook_result.scraps.data_dict == {
        "dict": {"a": 1, "b": 2},
        "list": [1, 2, 3],
        "number": 1,
        "one": 1,
    }


def test_display_scraps(notebook_result):
    assert notebook_result.scraps.display_dict == {
        "output": {
            "data": {"text/plain": "'Hello World!'"},
            "metadata": {"scrapbook": {"name": "output", "data": False, "display": True}},
            "output_type": "display_data",
        },
        "one_only": {
            "data": {"text/plain": "'Just here!'"},
            "metadata": {"scrapbook": {"name": "one_only", "data": False, "display": True}},
            "output_type": "display_data",
        },
    }


def test_scraps_collection_dataframe(notebook_result):
    expected_df = pd.DataFrame(
        [
            ("one", 1, "json", None),
            ("number", 1, "json", None),
            ("list", [1, 2, 3], "json", None),
            ("dict", {"a": 1, "b": 2}, "json", None),
            ("output", None, "display", AnyDict()),
            ("one_only", None, "display", AnyDict()),
        ],
        columns=["name", "data", "encoder", "display"],
    )
    assert_frame_equal(notebook_result.scraps.dataframe, expected_df)


def test_record_scraps_collection_dataframe(notebook_backwards_result):
    expected_df = pd.DataFrame(
        [
            ("hello", "world", "json", None),
            ("number", 123, "json", None),
            ("some_list", [1, 3, 5], "json", None),
            ("some_dict", {"a": 1, "b": 2}, "json", None),
            ("some_display", None, "display", AnyDict()),
        ],
        columns=["name", "data", "encoder", "display"],
    )
    print(notebook_backwards_result.scraps.dataframe)
    assert_frame_equal(notebook_backwards_result.scraps.dataframe, expected_df)


@mock.patch("IPython.display.display")
def test_reglue_display(mock_display, notebook_result):
    notebook_result.reglue("output")
    mock_display.assert_called_once_with(
        {"text/plain": "'Hello World!'"},
        metadata={"scrapbook": {"name": "output", "data": False, "display": True}},
        raw=True,
    )


@mock.patch("IPython.display.display")
def test_reglue_scrap(mock_display, notebook_result):
    notebook_result.reglue("one")
    mock_display.assert_called_once_with(
        {
            "application/scrapbook.scrap.json+json": {
                "name": "one",
                "data": 1,
                "encoder": "json",
                "version": 1,
            }
        },
        metadata={"scrapbook": {"name": "one", "data": True, "display": False}},
        raw=True,
    )


@mock.patch("IPython.display.display")
def test_reglue_display_unattached(mock_display, notebook_result):
    notebook_result.reglue("output", unattached=True)
    mock_display.assert_called_once_with({"text/plain": "'Hello World!'"}, metadata={}, raw=True)


@mock.patch("IPython.display.display")
def test_reglue_scrap_unattached(mock_display, notebook_result):
    notebook_result.reglue("one", unattached=True)
    mock_display.assert_called_once_with(
        {
            "application/scrapbook.scrap.json+json": {
                "name": "one",
                "data": 1,
                "encoder": "json",
                "version": 1,
            }
        },
        metadata={},
        raw=True,
    )


def test_missing_reglue(notebook_result):
    with pytest.raises(ScrapbookException):
        notebook_result.reglue("foo")


@mock.patch("IPython.display.display")
def test_missing_reglue_no_error(mock_display, notebook_result):
    notebook_result.reglue("foo", raise_on_missing=False)
    mock_display.assert_called_once_with("No scrap found with name 'foo' in this notebook")


@mock.patch("IPython.display.display")
def test_reglue_rename(mock_display, notebook_result):
    notebook_result.reglue("output", "new_output")
    mock_display.assert_called_once_with(
        {"text/plain": "'Hello World!'"},
        metadata={"scrapbook": {"name": "new_output", "data": False, "display": True}},
        raw=True,
    )


@pytest.fixture
def no_exec_result():
    path = get_notebook_path("result_no_exec.ipynb")
    return read_notebook(path)


def test_cell_timing(notebook_result):
    assert notebook_result.cell_timing == [0.0, 0.123]


def test_malformed_cell_timing(no_exec_result):
    assert no_exec_result.cell_timing == [None]


def test_execution_counts(notebook_result):
    assert notebook_result.execution_counts == [1, 2]


def test_malformed_execution_counts(no_exec_result):
    assert no_exec_result.execution_counts == [None]


def test_papermill_metrics(notebook_result):
    expected_df = pd.DataFrame(
        [
            ("result1.ipynb", "Out [1]", 0.000, "time (s)"),
            ("result1.ipynb", "Out [2]", 0.123, "time (s)"),
        ],
        columns=["filename", "cell", "value", "type"],
    )
    assert_frame_equal(notebook_result.papermill_metrics, expected_df)


def test_malformed_execution_metrics(no_exec_result):
    expected_df = pd.DataFrame([], columns=["filename", "cell", "value", "type"])
    assert_frame_equal(no_exec_result.papermill_metrics, expected_df)


def test_scrap_dataframe(notebook_result):
    expected_df = pd.DataFrame(
        [
            ("one", 1, "json", None, "result1.ipynb"),
            ("number", 1, "json", None, "result1.ipynb"),
            ("list", [1, 2, 3], "json", None, "result1.ipynb"),
            ("dict", {"a": 1, "b": 2}, "json", None, "result1.ipynb"),
            ("output", None, "display", AnyDict(), "result1.ipynb"),
            ("one_only", None, "display", AnyDict(), "result1.ipynb"),
        ],
        columns=["name", "data", "encoder", "display", "filename"],
    )
    assert_frame_equal(
        notebook_result.scrap_dataframe, expected_df, check_column_type=False,
    )


def test_papermill_dataframe(notebook_result):
    expected_df = pd.DataFrame(
        [
            ("bar", "hello", "parameter", "result1.ipynb"),
            ("foo", 1, "parameter", "result1.ipynb"),
            ("dict", {"a": 1, "b": 2}, "record", "result1.ipynb"),
            ("list", [1, 2, 3], "record", "result1.ipynb"),
            ("number", 1, "record", "result1.ipynb"),
            ("one", 1, "record", "result1.ipynb"),
        ],
        columns=["name", "value", "type", "filename"],
    )
    assert_frame_equal(notebook_result.papermill_dataframe, expected_df)


def test_no_cells():
    nb = Notebook(new_notebook(cells=[]))
    assert nb.scraps == collections.OrderedDict()


def test_no_outputs():
    nb = Notebook(new_notebook(cells=[new_code_cell("test", outputs=[])]))
    assert nb.scraps == collections.OrderedDict()


def test_empty_metadata():
    output = new_output(output_type="display_data", data={}, metadata={})
    raw_nb = new_notebook(cells=[new_code_cell("test", outputs=[output])])
    nb = Notebook(raw_nb)
    assert nb.scraps == collections.OrderedDict()


def test_metadata_but_empty_content():
    output = new_output(output_type="display_data", metadata={"scrapbook": {}})
    raw_nb = new_notebook(cells=[new_code_cell("test", outputs=[output])])
    nb = Notebook(raw_nb)
    assert nb.scraps == collections.OrderedDict()


def test_markdown():
    nb = Notebook(new_notebook(cells=[new_markdown_cell("this is a test.")]))
    assert nb.scraps == collections.OrderedDict()


@mock.patch("scrapbook.utils.is_kernel")
def test_reglue_warning(kernel_mock, notebook_result):
    kernel_mock.return_value = False
    with pytest.warns(UserWarning):
        notebook_result.reglue('number')


@mock.patch("scrapbook.utils.is_kernel")
def test_reglue_kernel_no_warning(kernel_mock, notebook_result, recwarn):
    kernel_mock.return_value = True
    notebook_result.reglue('number')
    assert len(recwarn) == 0
