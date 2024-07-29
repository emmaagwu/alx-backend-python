#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class in client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Ensure get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")

        # Ensure the result is as expected
        self.assertEqual(result, expected_payload)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url."""
        mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")

        # Test that _public_repos_url returns the expected value
        self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos")
        mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
