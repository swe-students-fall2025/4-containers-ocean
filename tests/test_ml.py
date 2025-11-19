from machine_learning_client.ml_client import predict_emotion

def test_predict_happy():
    # High pitch, high RMS => happy/excited
    assert predict_emotion(200, 0.02) == "happy/excited"

def test_predict_sad():
    # Low pitch, low RMS => sad
    assert predict_emotion(120, 0.005) == "sad"

def test_predict_neutral():
    # Everything else => neutral
    assert predict_emotion(160, 0.012) == "neutral"
