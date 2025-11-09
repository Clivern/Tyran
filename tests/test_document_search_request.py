from app.model.search import DocumentSearchRequest


def test_document_search_request_accepts_valid_payload() -> None:
    payload = DocumentSearchRequest(text="foo", category="runbook", limit=3)

    assert payload.text == "foo"
    assert payload.category == "runbook"
    assert payload.limit == 3
