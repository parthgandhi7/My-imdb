from app.services.agent import parse_intent


def test_parse_intent_extracts_provider_and_year():
    intent = parse_intent("A light Bollywood rom-com from 2025 on Netflix")
    assert 2025 in intent.years
    assert intent.provider == "netflix"
    assert "Romance" in intent.genres


def test_parse_intent_newer_defaults_recent_years():
    intent = parse_intent("I want a light movie like Stree but newer")
    assert len(intent.years) == 2
    assert intent.mood == "lighthearted"
