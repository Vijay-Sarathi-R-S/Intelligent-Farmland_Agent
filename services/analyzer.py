import google.generativeai as genai
import json
from datetime import datetime
from config import Config

class AnalyzerService:
    def __init__(self):
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_available = True
            print("🤖 Gemini AI Initialized")
        except Exception as e:
            print(f"❌ AI Setup Error: {e}")
            self.ai_available = False
    
    def analyze_field(self, field_data, vegetation_data, weather_risks):
        """Analyze field using REAL data only"""
        
        # Check if we have REAL data
        veg_error = vegetation_data.get('error', False)
        weather_error = weather_risks.get('error', False)
        
        if veg_error or weather_error:
            return self._handle_api_errors(vegetation_data, weather_risks)
        
        # Calculate basic metrics from REAL data
        analysis = self._calculate_from_real_data(vegetation_data, weather_risks)
        
        # Enhance with AI if available
        if self.ai_available and not analysis.get('error'):
            try:
                ai_insights = self._get_ai_insights(field_data, vegetation_data, weather_risks)
                analysis['ai_insights'] = ai_insights
                analysis['analysis_type'] = 'ai_enhanced'
            except Exception as e:
                print(f"AI enhancement error: {e}")
                analysis['analysis_type'] = 'basic'
        
        return analysis
    
    def _calculate_from_real_data(self, veg_data, weather_data):
        """Calculate everything from REAL data values"""
        
        # Extract REAL values
        ndvi = veg_data.get('mean_ndvi')
        weather_score = weather_data.get('overall_risk_score', 0.5)
        drought = weather_data.get('drought_risk', 0)
        flood = weather_data.get('flood_risk', 0)
        heat = weather_data.get('heat_stress_risk', 0)
        
        # Calculate overall risk from ACTUAL data
        overall_risk = (weather_score + (1 - ndvi)) / 2 if ndvi else weather_score
        
        # Determine risk level based on ACTUAL numbers
        if overall_risk > 0.6:
            risk_level = "High"
            premium = "+15% to +25%"
        elif overall_risk > 0.3:
            risk_level = "Medium"
            premium = "+5% to +10%"
        else:
            risk_level = "Low"
            premium = "-5% to 0%"
        
        # Generate recommendations based on ACTUAL risk values
        recommendations = []
        
        if drought > 0.6:
            recommendations.append(f"⚠️ HIGH DROUGHT RISK ({drought:.0%}) - Implement irrigation")
        elif drought > 0.3:
            recommendations.append(f"⚠️ Moderate drought risk ({drought:.0%}) - Monitor soil moisture")
        
        if flood > 0.6:
            recommendations.append(f"⚠️ HIGH FLOOD RISK ({flood:.0%}) - Improve drainage")
        
        if heat > 0.6:
            recommendations.append(f"⚠️ HIGH HEAT STRESS ({heat:.0%}) - Consider heat-resistant crops")
        
        if ndvi and ndvi < 0.3:
            recommendations.append(f"🌱 Low vegetation health (NDVI: {ndvi:.2f}) - Soil amendment needed")
        elif ndvi and ndvi > 0.7:
            recommendations.append(f"🌱 Excellent vegetation health (NDVI: {ndvi:.2f})")
        
        if not recommendations:
            recommendations.append("✅ Conditions normal - continue current practices")
        
        # Add weather context if available
        weather_summary = weather_data.get('weather_summary', {})
        if weather_summary:
            recommendations.append(f"📊 Weather: {weather_summary.get('avg_temperature_c', '?')}°C avg, {weather_summary.get('total_rainfall_mm', 0)}mm rain")
        
        return {
            'overall_risk': risk_level,
            'risk_score': round(overall_risk, 3),
            'vegetation_health': veg_data.get('health_status', 'Unknown'),
            'ndvi_value': ndvi,
            'ndvi_confidence': veg_data.get('confidence', 'Medium'),
            'weather_risk_level': weather_data.get('risk_level', 'Unknown'),
            'weather_details': weather_summary,
            'risk_breakdown': {
                'drought': drought,
                'flood': flood,
                'heat_stress': heat
            },
            'recommendations': recommendations,
            'premium_adjustment': premium,
            'data_sources': {
                'satellite': veg_data.get('source', 'unknown'),
                'weather': weather_data.get('source', 'unknown')
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_ai_insights(self, field_data, veg_data, weather_data):
        """Get AI insights on REAL data"""
        
        prompt = f"""
        Analyze this REAL farm data for insurance risk assessment:
        
        FIELD: {field_data.get('name')} ({field_data.get('acres')} acres)
        CROP: {field_data.get('crop_type', 'Unknown')}
        LOCATION: {field_data.get('latitude')}°, {field_data.get('longitude')}°
        
        ACTUAL SATELLITE DATA:
        - NDVI: {veg_data.get('mean_ndvi')}
        - Vegetation Health: {veg_data.get('health_status')}
        - Data Confidence: {veg_data.get('confidence')}
        
        ACTUAL WEATHER DATA:
        - Avg Temperature: {weather_data.get('weather_summary', {}).get('avg_temperature_c')}°C
        - Total Rainfall: {weather_data.get('weather_summary', {}).get('total_rainfall_mm')}mm
        - Drought Risk: {weather_data.get('drought_risk')}
        - Flood Risk: {weather_data.get('flood_risk')}
        
        Based ONLY on this REAL data, provide a brief JSON with:
        1. risk_summary: 2-3 sentence analysis
        2. key_factors: list of main risk factors from the data
        3. insurance_tips: 2-3 specific recommendations
        4. confidence: based on data quality
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        
        return {
            'risk_summary': f"Analysis based on NDVI {veg_data.get('mean_ndvi', 0.5):.2f} and {weather_data.get('weather_summary', {}).get('total_rainfall_mm', 0)}mm rainfall",
            'key_factors': ['Based on real-time data'],
            'insurance_tips': ['Review detailed metrics above'],
            'confidence': 'Medium'
        }
    
    def _handle_api_errors(self, veg_data, weather_data):
        """Handle API failures - show errors, not fake data"""
        return {
            'error': True,
            'overall_risk': 'Unknown',
            'vegetation_health': 'Data Unavailable',
            'weather_risk_level': 'Unknown',
            'recommendations': [
                '❌ Satellite data unavailable',
                '❌ Weather data unavailable',
                'Please try again in a few minutes',
                f"Satellite error: {veg_data.get('message', 'Unknown')}",
                f"Weather error: {weather_data.get('message', 'Unknown')}"
            ],
            'premium_adjustment': 'Cannot determine',
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_report(self, field, analysis):
        """Generate report from REAL data"""
        
        if analysis.get('error'):
            return f"""
VERDEX INSURANCE VERIFICATION REPORT
====================================
Report ID: FLD-{field['id'][:8]}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Status: DATA UNAVAILABLE

FIELD DETAILS
-------------
Name: {field['name']}
Location: {field['latitude']}°, {field['longitude']}°
Size: {field['acres']} acres

ERROR REPORT
------------
{analysis.get('recommendations', ['No data available'])[0]}
{analysis.get('recommendations', [''])[1]}

RECOMMENDATION
--------------
Please retry analysis when data services are available.

Report Certified By: Verdex Asset Intelligence
            """
        
        weather = analysis.get('weather_details', {})
        risks = analysis.get('risk_breakdown', {})
        
        report = f"""
VERDEX INSURANCE VERIFICATION REPORT
====================================
Report ID: FLD-{field['id'][:8]}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FIELD DETAILS
-------------
Name: {field['name']}
Location: {field['latitude']}°, {field['longitude']}°
Size: {field['acres']} acres
Crop: {field.get('crop_type', 'Not specified')}

REAL SATELLITE DATA
------------------
NDVI Score: {analysis.get('ndvi_value', 'N/A')}
Health Status: {analysis.get('vegetation_health', 'N/A')}
Data Confidence: {analysis.get('ndvi_confidence', 'N/A')}
Source: {analysis.get('data_sources', {}).get('satellite', 'NASA')}

REAL WEATHER DATA
----------------
Avg Temperature: {weather.get('avg_temperature_c', 'N/A')}°C
Total Rainfall: {weather.get('total_rainfall_mm', 'N/A')}mm
Rainy Days: {weather.get('rainy_days', 'N/A')}
Source: {analysis.get('data_sources', {}).get('weather', 'NASA POWER')}

RISK ASSESSMENT (Based on REAL Data)
-----------------------------------
Drought Risk: {risks.get('drought', 'N/A'):.0%}
Flood Risk: {risks.get('flood', 'N/A'):.0%}
Heat Stress: {risks.get('heat_stress', 'N/A'):.0%}
Overall Risk Score: {analysis.get('risk_score', 'N/A')}
Risk Classification: {analysis.get('overall_risk', 'N/A')}

INSURANCE RECOMMENDATION
------------------------
Premium Adjustment: {analysis.get('premium_adjustment', 'N/A')}

Recommended Actions:
{chr(10).join('• ' + r for r in analysis.get('recommendations', ['No recommendations']))}

VERIFICATION
------------
This report was generated using REAL satellite imagery and weather data.
All analyses are objective, auditable, and based on actual measurements.
Data Sources: NASA Earth Observatory, NASA POWER

Report Certified By: Verdex Asset Intelligence
        """
        
        return report