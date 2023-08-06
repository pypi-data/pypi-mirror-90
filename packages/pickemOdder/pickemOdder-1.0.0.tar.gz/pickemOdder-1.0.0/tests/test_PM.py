#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pickemOdder` package."""


import unittest

from pickemOdder import pickemOdder


class TestPm(unittest.TestCase):
    """Tests for `pickemOdder` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        with open('tests/data/nfl-data.json') as fp:
            pickemOdder.get_normed_data(fp)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
