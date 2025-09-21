#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
import utils


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL."""
        known_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        
        with patch.object(GithubOrgClient, 'org', 
                         new_callable=PropertyMock, 
                         return_value=known_payload) as mock_org:
            client = GithubOrgClient("google")
            result = client._public_repos_url
            
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
            mock_org.assert_called_once()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()