#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""
import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    def test_org(self):
        """Test that GithubOrgClient.org returns the expected value."""
        test_cases = ["google", "abc"]

        for org_name in test_cases:
            with self.subTest(org=org_name):
                expected = {"login": org_name}
                with patch("client.get_json", return_value=expected) as mock_get_json:
                    client = GithubOrgClient(org_name)
                    self.assertEqual(client.org, expected)
                    mock_get_json.assert_called_once_with(
                        f"https://api.github.com/orgs/{org_name}"
                    )


if __name__ == "__main__":
    unittest.main()
