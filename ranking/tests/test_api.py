"""Tests for the FastAPI ranking endpoint."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from ranking.serving.api import RankRequest, app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestRankEndpoint:
    def test_rank_returns_200_with_valid_request(self, client: TestClient) -> None:
        # TODO: Test that a valid ranking request returns 200 with ranked results
        # Requires the ranker to be initialized; mock get_ranker for unit testing
        request = {
            "query": "python tutorial",
            "candidates": [
                {
                    "doc_id": "doc_1",
                    "title": "Python Tutorial",
                    "body": "Learn python programming",
                    "url": "https://example.com/python",
                },
                {
                    "doc_id": "doc_2",
                    "title": "Java Guide",
                    "body": "Java programming basics",
                    "url": "https://example.com/java",
                },
            ],
            "top_k": 2,
        }
        # TODO: Mock the ranker and assert response structure
        # response = client.post("/rank", json=request)
        # assert response.status_code == 200
        # data = response.json()
        # assert len(data["results"]) <= 2
        # assert data["query"] == "python tutorial"
        pytest.skip("Requires ranker initialization — mock get_ranker to enable")

    def test_rank_empty_candidates_returns_422(self, client: TestClient) -> None:
        # TODO: Test that an empty candidates list returns a validation error
        request = {
            "query": "python tutorial",
            "candidates": [],
            "top_k": 5,
        }
        response = client.post("/rank", json=request)
        assert response.status_code == 422

    def test_rank_results_are_sorted_by_score(self, client: TestClient) -> None:
        # TODO: Test that returned results have descending scores
        # Requires ranker mock — verify results[i].score >= results[i+1].score
        pytest.skip("Requires ranker initialization — mock get_ranker to enable")

    def test_rank_top_k_limits_results(self, client: TestClient) -> None:
        # TODO: Test that top_k parameter limits the number of returned results
        pytest.skip("Requires ranker initialization — mock get_ranker to enable")


class TestBatchRankEndpoint:
    def test_batch_returns_one_response_per_request(self, client: TestClient) -> None:
        # TODO: Test that batch endpoint returns same number of responses as requests
        pytest.skip("Requires ranker initialization — mock get_ranker to enable")


class TestRequestValidation:
    def test_missing_query_returns_422(self, client: TestClient) -> None:
        # TODO: Test that missing query field returns validation error
        request = {
            "candidates": [
                {
                    "doc_id": "doc_1",
                    "title": "Test",
                    "body": "test body",
                    "url": "https://example.com",
                }
            ]
        }
        response = client.post("/rank", json=request)
        assert response.status_code == 422

    def test_invalid_top_k_returns_422(self, client: TestClient) -> None:
        # TODO: Test that top_k=0 or negative values return validation error
        request = {
            "query": "test",
            "candidates": [
                {
                    "doc_id": "doc_1",
                    "title": "Test",
                    "body": "test body",
                    "url": "https://example.com",
                }
            ],
            "top_k": 0,
        }
        response = client.post("/rank", json=request)
        assert response.status_code == 422
