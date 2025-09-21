from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class MockResponse:
    """Mock response object to simulate requests.get().json()."""
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos,
        }
    ]
)
class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get and set side_effect to return fixture payloads."""
        super().setUpClass()  # Ensures base class setup is called
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            if url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests."""
        cls.get_patcher.stop()
        super().tearDownClass()  # Ensures base class teardown is called

    def test_public_repos(self):
        """Integration test for public_repos without license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
