from services.satellite import increment_satellite_count

def test_satellite_access_counter():
    count = increment_satellite_count()
    print("\nTotal Satellite API Access Count:", count)
    assert count >= 1
