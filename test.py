from services.satellite import SatelliteService
from services.weather import WeatherService

sat = SatelliteService()
weather = WeatherService()

# Test Iowa
print("\n🌽 Testing Iowa Farmland...")
veg = sat.get_vegetation_data(42.0347, -93.62)
wx = weather.get_risk_metrics(42.0347, -93.62)
print(f"Satellite: {veg.get('source', 'failed')} - NDVI: {veg.get('mean_ndvi')}")
print(f"Weather: {wx.get('source', 'failed')} - Risk: {wx.get('risk_level')}")

# Test Sahara
print("\n🏜️ Testing Sahara Desert...")
veg = sat.get_vegetation_data(23.4162, 25.6628)
wx = weather.get_risk_metrics(23.4162, 25.6628)
print(f"Satellite: {veg.get('source', 'failed')} - NDVI: {veg.get('mean_ndvi')}")
print(f"Weather: {wx.get('source', 'failed')} - Risk: {wx.get('risk_level')}")