"""Regression tests for direct MCP connector payload routing."""

from __future__ import annotations

from perplexity_web_mcp.http import _prepare_direct_mcp_payload


def test_github_direct_connector_uses_web_mention_shape() -> None:
    payload = {
        "params": {
            "sources": ["github_mcp_direct"],
            "search_focus": "internet",
            "is_incognito": True,
            "use_schematized_api": False,
            "send_back_text_in_streaming_api": True,
        },
        "query_str": "lista mis repos",
    }

    normalized = _prepare_direct_mcp_payload(payload)

    assert normalized["params"]["sources"] == ["web"]
    assert normalized["params"]["mentions"] == [
        {
            "id": "github_mcp_direct",
            "url": "",
            "type": "sources",
        }
    ]
    assert normalized["params"]["is_incognito"] is False
    assert normalized["params"]["use_schematized_api"] is True
    assert normalized["params"]["send_back_text_in_streaming_api"] is False
    assert "workflow_steps" in normalized["params"]["supported_block_use_cases"]
    assert "workflow_widgets" in normalized["params"]["supported_block_use_cases"]
    assert normalized["params"]["skip_search_enabled"] is True
    assert normalized["params"]["should_ask_for_mcp_tool_confirmation"] is True
    assert normalized["params"]["supports_tool_approval_modal"] is True
    assert normalized["query_str"] == "@GitHub lista mis repos"

    # The transport normalization must not mutate the caller's payload.
    assert payload["params"]["sources"] == ["github_mcp_direct"]
    assert payload["params"]["is_incognito"] is True
    assert payload["params"]["use_schematized_api"] is False
    assert payload["params"]["send_back_text_in_streaming_api"] is True
    assert "mentions" not in payload["params"]
    assert payload["query_str"] == "lista mis repos"


def test_existing_github_mention_is_not_duplicated() -> None:
    mention = {"id": "github_mcp_direct", "url": "", "type": "sources"}
    payload = {
        "params": {
            "sources": ["web", "github_mcp_direct"],
            "mentions": [mention],
        },
        "query_str": "@GitHub lista mis repos",
    }

    normalized = _prepare_direct_mcp_payload(payload)

    assert normalized["params"]["sources"] == ["web"]
    assert normalized["params"]["mentions"] == [mention]
    assert normalized["query_str"] == "@GitHub lista mis repos"


def test_retrieval_connector_source_behavior_is_unchanged() -> None:
    payload = {
        "params": {"sources": ["pitchbook_mcp_cashmere"]},
        "query_str": "company funding",
    }

    normalized = _prepare_direct_mcp_payload(payload)

    assert normalized is payload
    assert normalized["params"]["sources"] == ["pitchbook_mcp_cashmere"]
    assert "mentions" not in normalized["params"]


def test_builtin_web_source_behavior_is_unchanged() -> None:
    payload = {
        "params": {"sources": ["web"]},
        "query_str": "latest news",
    }

    normalized = _prepare_direct_mcp_payload(payload)

    assert normalized is payload
    assert normalized == payload
