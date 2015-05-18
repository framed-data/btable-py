# -*- coding: utf-8 -*-

import pkg_resources
import tempfile
import btable


def fixture(fname):
    return pkg_resources.resource_filename(
        'btable',
        'data/{}'.format(fname))


def test_row_count():
    bt = btable.BTable(fixture('table.btable'))
    assert sum(1 for x in bt.rows()) == 5000


def test_unicode_label():
    bt = btable.BTable(fixture('unicode.btable'))
    assert bt.labels[0] == u"通"


def test_write():
    tf = tempfile.NamedTemporaryFile()
    labels = ["one", "two", "three"]
    rows = [[0.0, 1.0, 0.0], [2.0, 0.0, 3.0], [0.0, 4.0, 5.0]]
    bt = btable.write(tf.name, labels, rows)
    bt = btable.BTable(tf.name)
    assert bt.labels == labels
    assert [r for r in bt.rows()] == rows
