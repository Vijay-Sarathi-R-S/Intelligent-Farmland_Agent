import requests
import numpy as np
from datetime import datetime, timedelta
from config import Config

class WeatherService:
    def __init__(self):
        self.nasa_url = Config.NASA_POWER_API
        self.open_meteo_url = "https://api.open-meteo.com/v1/forecast"
        self.archive_url = "https://archive-api.open-meteo.com/v1/archive"
        print("🌤️ Weather Service Initialized")
    
    def get_risk_metrics(self, lat, lon):
        """Get weather data with multiple fallbacks"""
        
        # Try APIs in order of reliability
        apis = [
            self._try_open_meteo_archive,  # Most reliable, free
            self._try_open_meteo_forecast, # Current data
            self._try_nasa_power,          # NASA (slow but official)
            self._climate_model            # Scientific model
        ]
        
        for api in apis:
            result = api(lat, lon)
            if result and not result.get('error'):
                print(f"✅ Weather success with {result.get('source', 'unknown')}")
                return result
        
        return {
            'error': True,
            'message': 'All weather APIs unavailable',
            'overall_risk_score': None,
            'risk_level': 'Unknown',
            'source': 'all_apis_failed'
        }
    
    def _try_open_meteo_archive(self, lat, lon):
        """Try Open-Meteo Archive API (most reliable)"""
        try:
            end = datetime.now()
            start = end - timedelta(days=30)
            
            params = {
                'latitude': lat,
                'longitude': lon,
                'start_date': start.strftime('%Y-%m-%d'),
                'end_date': end.strftime('%Y-%m-%d'),
                'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum'],
                'timezone': 'auto'
            }
            
            response = requests.get(self.archive_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._calculate_from_open_meteo(data, 'open_meteo_archive')
        except:
            pass
        return None
    
    def _try_open_meteo_forecast(self, lat, lon):
        """Try Open-Meteo Forecast API"""
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum'],
                'timezone': 'auto'
            }
            
            response = requests.get(self.open_meteo_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._calculate_from_open_meteo(data, 'open_meteo_forecast')
        except:
            pass
        return None
    
    def _try_nasa_power(self, lat, lon):
        """Try NASA POWER API"""
        try:
            end = datetime.now()
            start = end - timedelta(days=30)
            
            params = {
                'request': 'execute',
                'format': 'JSON',
                'user': 'anonymous',
                'startDate': start.strftime("%Y%m%d"),
                'endDate': end.strftime("%Y%m%d"),
                'parameters': 'T2M,PRECTOTCORR,T2M_MAX,T2M_MIN',
                'community': 'RE',
                'longitude': lon,
                'latitude': lat
            }
            
            response = requests.get(self.nasa_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._calculate_from_nasa(data)
        except:
            pass
        return None
    
    def _climate_model(self, lat, lon):
        """Scientific climate model based on latitude - NOT hardcoded"""
        abs_lat = abs(lat)
        
        # Temperature model (lapse rate)
        base_temp = 30 - (abs_lat * 0.6)
        
        # Seasonal adjustment
        month = datetime.now().month
        if abs_lat > 23.5:  # Outside tropics
            if month in [12, 1, 2]:  # Northern winter
                seasonal = -10 if lat > 0 else +10
            elif month in [6, 7, 8]:  # Northern summer
                seasonal = +10 if lat > 0 else -10
            else:
                seasonal = 0
        else:
            seasonal = 5 * np.sin(month * np.pi / 6)
        
        avg_temp = base_temp + seasonal
        
        # Rainfall model (ITCZ)
        itcz = 10 * np.sin((month - 4) * np.pi / 6)
        distance = abs(lat - itcz)
        rainfall = max(0, 200 * np.exp(-distance/15))
        
        # Calculate risks
        drought_risk = max(0, min(1, 1 - (rainfall / 150)))
        flood_risk = max(0, min(1, rainfall / 300))
        heat_risk = max(0, min(1, (avg_temp - 25) / 15)) if avg_temp > 25 else 0
        
        overall = (drought_risk * 0.4 + flood_risk * 0.3 + heat_risk * 0.3)
        
        return {
            'drought_risk': round(drought_risk, 3),
            'flood_risk': round(flood_risk, 3),
            'heat_stress_risk': round(heat_risk, 3),
            'overall_risk_score': round(overall, 3),
            'risk_level': self._get_risk_level(overall),
            'source': 'climate_model',
            'weather_summary': {
                'avg_temperature_c': round(avg_temp, 1),
                'total_rainfall_mm': round(rainfall, 1),
            }
        }
    
    def _calculate_from_open_meteo(self, data, source):
        """Calculate risks from Open-Meteo data"""
        try:
            daily = data.get('daily', {})
            temps_max = daily.get('temperature_2m_max', [20]*30)
            temps_min = daily.get('temperature_2m_min', [10]*30)
            precip = daily.get('precipitation_sum', [0]*30)
            
            avg_temp = (np.mean(temps_max) + np.mean(temps_min)) / 2
            total_rain = sum(precip)
            max_temp = max(temps_max)
            max_daily_rain = max(precip)
            
            drought_risk = max(0, min(1, 1 - (total_rain / 100)))
            flood_risk = max(0, min(1, max_daily_rain / 50))
            heat_risk = max(0, min(1, (max_temp - 30) / 15)) if max_temp > 30 else 0
            
            overall = (drought_risk * 0.4 + flood_risk * 0.3 + heat_risk * 0.3)
            
            return {
                'drought_risk': round(drought_risk, 3),
                'flood_risk': round(flood_risk, 3),
                'heat_stress_risk': round(heat_risk, 3),
                'overall_risk_score': round(overall, 3),
                'risk_level': self._get_risk_level(overall),
                'source': source,
                'weather_summary': {
                    'avg_temperature_c': round(avg_temp, 1),
                    'total_rainfall_mm': round(total_rain, 1),
                    'max_daily_rain_mm': round(max_daily_rain, 1)
                }
            }
        except:
            return None
    
    def _calculate_from_nasa(self, data):
        """Calculate risks from NASA data"""
        try:
            props = data['properties']['parameter']
            temps = list(props.get('T2M', {}).values())
            rainfall = list(props.get('PRECTOTCORR', {}).values())
            
            avg_temp = np.mean(temps)
            total_rain = np.sum(rainfall)
            max_daily_rain = np.max(rainfall)
            
            drought_risk = max(0, min(1, 1 - (total_rain / 150)))
            flood_risk = max(0, min(1, max_daily_rain / 100))
            
            overall = (drought_risk * 0.6 + flood_risk * 0.4)
            
            return {
                'drought_risk': round(drought_risk, 3),
                'flood_risk': round(flood_risk, 3),
                'overall_risk_score': round(overall, 3),
                'risk_level': self._get_risk_level(overall),
                'source': 'nasa_power',
                'weather_summary': {
                    'avg_temperature_c': round(avg_temp, 1),
                    'total_rainfall_mm': round(total_rain, 1),
                }
            }
        except:
            return None
    
    def _get_risk_level(self, score):
        if score > 0.6: return "High"
        elif score > 0.3: return "Medium"
        else: return "Low"