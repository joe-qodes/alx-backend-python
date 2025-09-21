#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Unit tests for the GithubOrgClient class."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value from org payload."""
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)
