from app.services.youtube import extract_video_id


def test_valid_watch_url():
    assert extract_video_id("https://www.youtube.com/watch?v=Gfr50f6ZBvo&t=30s") == "Gfr50f6ZBvo"


def test_valid_short_url():
    assert extract_video_id("https://youtu.be/Gfr50f6ZBvo") == "Gfr50f6ZBvo"


def test_invalid_url_raises():
    try:
        extract_video_id("https://example.com")
        assert False, "Expected ValueError"
    except ValueError:
        pass
