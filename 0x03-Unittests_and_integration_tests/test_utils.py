#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""
import unittest
from unittest import mock
from parameterized import parameterized
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # KeyError message should be the missing key
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize decorator caches function results."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with unittest.mock.patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            test_obj = TestClass()
            # First call should call the method
            result1 = test_obj.a_property
            # Second call should use cached result
            result2 = test_obj.a_property
            
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # Method should only be called once due to memoization
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
