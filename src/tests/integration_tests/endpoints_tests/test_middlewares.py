# pylint: disable=unused-argument
import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# ─── CorrelationIdMiddleware ──────────────────────────────────────────────────

def test_correlation_id_generated_when_not_provided():
    """Should be generated when not provided."""
    response = client.get("/health")
    assert response.status_code == 200
    correlation_id = response.headers.get("x-request-id")
    assert correlation_id is not None
    # Valida que é um UUID válido
    uuid.UUID(correlation_id)


def test_correlation_id_reused_when_provided():
    """Should reuse the X-Request-ID sent by the client."""
    custom_id = "meu-id-customizado-123"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("x-request-id") == custom_id


def test_correlation_id_present_in_all_responses():
    """Should include X-Request-ID in any endpoint."""
    response = client.get("/health")
    assert "x-request-id" in response.headers


def test_correlation_id_is_unique_per_request():
    """Each request without a header should generate a different ID."""
    response_1 = client.get("/health")
    response_2 = client.get("/health")
    id_1 = response_1.headers.get("x-request-id")
    id_2 = response_2.headers.get("x-request-id")
    assert id_1 != id_2


# ─── LoggingMiddleware ────────────────────────────────────────────────────────

def test_logging_middleware_logs_incoming_request():
    """Should log the incoming request with method and path."""
    with patch("src.middlewares.logging_middleware.logger") as mock_logger:
        client.get("/health")
        calls = [str(c) for c in mock_logger.info.call_args_list]
        assert any("Incoming request" in c for c in calls)


def test_logging_middleware_logs_completed_request():
    """Should log the completed request with status_code and duration_ms."""
    with patch("src.middlewares.logging_middleware.logger") as mock_logger:
        client.get("/health")
        calls = [str(c) for c in mock_logger.info.call_args_list]
        assert any("Request completed" in c for c in calls)


def test_logging_middleware_includes_correlation_id_in_log():
    """Should include the correlation_id in the log."""
    custom_id = "test-correlation-log"
    with patch("src.middlewares.logging_middleware.logger") as mock_logger:
        client.get("/health", headers={"X-Request-ID": custom_id})
        all_extra = [
            call.kwargs.get("extra", {})
            for call in mock_logger.info.call_args_list
        ]
        assert any(e.get("correlation_id") == custom_id for e in all_extra)


def test_logging_middleware_includes_method_and_path():
    """Should include the correct method and path in the log."""
    with patch("src.middlewares.logging_middleware.logger") as mock_logger:
        client.get("/health")
        all_extra = [
            call.kwargs.get("extra", {})
            for call in mock_logger.info.call_args_list
        ]
        assert any(
            e.get("method") == "GET" and e.get("path") == "/health"
            for e in all_extra
        )


def test_logging_middleware_includes_status_code_and_duration():
    """Should include status_code and duration_ms in the log."""
    with patch("src.middlewares.logging_middleware.logger") as mock_logger:
        client.get("/health")
        all_extra = [
            call.kwargs.get("extra", {})
            for call in mock_logger.info.call_args_list
        ]
        completed = [e for e in all_extra if "status_code" in e]
        assert len(completed) > 0
        assert completed[0]["status_code"] == 200
        assert "duration_ms" in completed[0]
