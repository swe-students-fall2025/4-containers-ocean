# Tests basic emotion analysis behavior

from ml_client import analyze_emotion

def test_analyze_emotion_output():
    # Make sure the function returns a dict with expected keys
    result = analyze_emotion("I am happy today")
    assert isinstance(result, dict)
    assert "label" in result
    assert "score" in result