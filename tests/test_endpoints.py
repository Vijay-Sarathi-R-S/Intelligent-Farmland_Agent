import json
import pytest

from run import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_healthz(client):
    rv = client.get('/healthz')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get('status') == 'ok'


def test_create_field_and_analyze(monkeypatch, client):
    # Create a field
    payload = {
        "name": "Test Field",
        "latitude": 42.0,
        "longitude": -93.0,
        "acres": 10,
        "crop_type": "Wheat"
    }
    rv = client.post('/api/fields', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['success'] is True
    field = data['field']

    # Monkeypatch satellite and weather to simulate API failure and success
    import services.satellite as satm

    def fake_get_veg(lat, lon):
        return {"source": "mock", "mean_ndvi": 0.5}

    monkeypatch.setattr(satm.SatelliteService, 'get_vegetation_data', lambda self, a, b: fake_get_veg(a, b))

    import services.weather as wxm

    monkeypatch.setattr(wxm.WeatherService, 'get_risk_metrics', lambda self, a, b: {"risk_level": "low", "source": "mock"})

    # Run analysis
    rv2 = client.post(f"/api/fields/{field['id']}/analyze")
    assert rv2.status_code == 200
    result = rv2.get_json()
    assert result['success'] is True
    assert 'analysis' in result
