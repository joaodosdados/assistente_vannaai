from app.routers.chat import detect_intent, extract_ids


def test_detect_status_intent():
    assert detect_intent("qual a situação do processo 123?") == "status_processo"
    assert detect_intent("como está meu processo 456") == "status_processo"


def test_extract_ids():
    assert extract_ids("qual a situação do processo 123?")[0] == "123"
