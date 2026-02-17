from services.ai_validation import validate_analysis_output


def test_validate_good_output():
    good = {
        "vegetation_health": "Healthy",
        "ndvi_value": 0.7,
        "ai_insights": "All good"
    }
    res = validate_analysis_output(good)
    assert res['valid'] is True


def test_validate_bad_output():
    bad = {
        "vegetation_health": 123,
        "ndvi_value": 5,
    }
    res = validate_analysis_output(bad)
    assert res['valid'] is False
    assert any('ndvi_value out of range' in e or 'vegetation_health' in e for e in res['errors'])
