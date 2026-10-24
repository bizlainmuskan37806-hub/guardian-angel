
from fastapi.testclient import TestClient

from main import (
    app,
    detect_risk,
    calculate_risk,
    generate_ai_explanation,
    risk_explanations,
    risk_explanations_translated,
)

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Guardian Angel" in response.text


def test_high_risk_message():
    message = (
        "URGENT! Your account will be blocked. "
        "Send your OTP immediately."
    )

    warning_signs = detect_risk(message)
    score, level = calculate_risk(warning_signs)

    assert "urgent" in warning_signs
    assert "account will be blocked" in warning_signs
    assert "send your otp" in warning_signs
    assert score == 7
    assert level == "high"


def test_medium_risk_message():
    warning_signs = detect_risk("Please verify your account.")
    score, level = calculate_risk(warning_signs)

    assert "verify your account" in warning_signs
    assert score == 2
    assert level == "medium"


def test_low_risk_message():
    warning_signs = detect_risk(
        "Hello, would you like to have lunch tomorrow?"
    )
    score, level = calculate_risk(warning_signs)

    assert warning_signs == []
    assert score == 0
    assert level == "low"


def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={"message": "URGENT! Send your OTP immediately."},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["risk_level"] == "medium"
    assert data["risk_score"] == 4
    assert "urgent" in data["warning_signs"]
    assert "send your otp" in data["warning_signs"]


def test_empty_message_rejected():
    response = client.post(
        "/analyze",
        json={"message": ""},
    )
    assert response.status_code == 422


def test_message_with_only_spaces_rejected():
    response = client.post(
        "/analyze",
        json={"message": "   "},
    )
    assert response.status_code == 400


def test_all_14_warning_phrases_are_detected():
    assert len(risk_explanations) ==22

    for phrase in risk_explanations:
        assert phrase in detect_risk(phrase), (
            f"Warning phrase was not detected: {phrase}"
        )


def test_all_warning_phrases_have_risk_weights():
    for phrase in risk_explanations:
        score, level = calculate_risk([phrase])

        assert score > 0, f"Missing risk weight: {phrase}"
        assert level in ("low", "medium", "high")


def test_duplicate_warning_does_not_inflate_score():
    score_once, level_once = calculate_risk(["send your otp"])

    score_twice, level_twice = calculate_risk(
        ["send your otp", "send your otp"]
    )

    assert score_once == score_twice == 3
    assert level_once == level_twice == "medium"


def test_hindi_translations_cover_all_warning_phrases():
    for phrase in risk_explanations:
        assert phrase in risk_explanations_translated["Hindi"]
        assert risk_explanations_translated["Hindi"][phrase]


def test_punjabi_translations_cover_all_warning_phrases():
    for phrase in risk_explanations:
        assert phrase in risk_explanations_translated["Punjabi"]
        assert risk_explanations_translated["Punjabi"][phrase]


def test_api_returns_hindi_rule_based_explanations():
    response = client.post(
        "/analyze",
        json={
            "message": "Please send money.",
            "language": "Hindi",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "send money" in data["warning_signs"]
    assert data["explanations"] == [
        risk_explanations_translated["Hindi"]["send money"]
    ]


def test_api_returns_punjabi_rule_based_explanations():
    response = client.post(
        "/analyze",
        json={
            "message": "Please send money.",
            "language": "Punjabi",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "send money" in data["warning_signs"]
    assert data["explanations"] == [
        risk_explanations_translated["Punjabi"]["send money"]
    ]

def test_ai_rejects_advice_to_share_otp(monkeypatch):
    import main

    class FakeResponse:
        def read(self):
            import json
            return json.dumps({
                "response": (
                    "Send your OTP immediately to verify your account."
                )
            }).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    monkeypatch.setattr(
    main,
    "urlopen",
    lambda *args, **kwargs: FakeResponse(),
    )

    result = generate_ai_explanation(
        "URGENT! Send your OTP immediately.",
        ["urgent", "send your otp"],
        "English",
    )

    assert result is None


def test_ai_rejects_advice_to_share_password_reset_code(monkeypatch):
    import json
    import main

    class FakeResponse:
        def read(self):
            return json.dumps({
                "response": (
                    "Send your password reset code immediately."
                )
            }).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    monkeypatch.setattr(
        main,
        "urlopen",
        lambda *args, **kwargs: FakeResponse(),
    )

    result = generate_ai_explanation(
        "Your account needs verification.",
        ["verify your account"],
        "English",
    )

    assert result is None

