#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected repos_url."""
        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo list."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected result is just the repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Ensure mocks were called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )
