#!/usr/bin/env python3
"""
Unittests and integration tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the expected value
        and that get_json is called once with the right argument.
        """
        test_payload = {"org": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the expected URL
        based on the org payload.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=test_payload
        ):
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repo names
        and that get_json and _public_repos_url are called once.
        """
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = test_repos

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos"
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns the correct boolean value
        depending on the repo license key.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": [repo["name"] for repo in TEST_PAYLOAD[0][1]],
        "apache2_repos": [
            repo["name"] for repo in TEST_PAYLOAD[0][1]
            if repo.get("license", {}).get("key") == "apache-2.0"
        ]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        payloads = {
            cls.org_payload["url"]: cls.org_payload,
            cls.org_payload["repos_url"]: cls.repos_payload
        }

        def get_payload(url):
            return payloads[url]

        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = get_payload

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    @patch("client.requests.get")
    def test_public_repos_with_license(self, mock_get):
        """Test public_repos filters repos by license"""
        # Mock org response
        mock_org_resp = MagicMock()
        mock_org_resp.json.return_value = org_payload

        # Mock repos response
        mock_repos_resp = MagicMock()
        mock_repos_resp.json.return_value = repos_payload