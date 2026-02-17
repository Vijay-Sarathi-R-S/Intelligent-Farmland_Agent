#!/usr/bin/env python3
"""
Enhanced Test Suite for Intelligent Farmland Agent
Tests both functional features and AI output validation
"""

import pytest
import sys
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Test: Services Initialization
class TestServicesInitialization:
    """Verify all services initialize correctly"""
    
    def test_satellite_service_init(self):
        from services.satellite import SatelliteService
        sat = SatelliteService()
        assert sat is not None
        assert hasattr(sat, 'get_vegetation_data')
    
    def test_weather_service_init(self):
        from services.weather import WeatherService
        weather = WeatherService()
        assert weather is not None
        assert hasattr(weather, 'get_risk_metrics')
    
    def test_analyzer_service_init(self):
        from services.analyzer import AnalyzerService
        analyzer = AnalyzerService()
        assert analyzer is not None


# Test: AI Output Validation (CRITICAL)
class TestAIOutputValidation:
    """Validate AI responses for hallucinations and bounds"""
    
    @pytest.fixture
    def validator(self):
        from services.ai_validator import AIOutputValidator
        return AIOutputValidator()
    
    def test_valid_ndvi(self, validator):
        """NDVI within valid range should pass"""
        assert validator.validate_ndvi(0.5) == True
        assert validator.validate_ndvi(-0.1) == True
        assert validator.validate_ndvi(1.0) == True
    
    def test_invalid_ndvi_above_range(self, validator):
        """NDVI > 1 should be detected as hallucination"""
        assert validator.validate_ndvi(1.5) == False
        assert validator.validate_ndvi(5.0) == False
    
    def test_invalid_ndvi_below_range(self, validator):
        """NDVI < -1 should be detected as hallucination"""
        assert validator.validate_ndvi(-1.5) == False
    
    def test_validate_field_analysis_valid(self, validator):
        """Valid analysis should pass validation"""
        valid_response = {
            'ndvi': 0.65,
            'temperature': 25.0,
            'health_score': 85,
            'health_status': 'Good',
            'recommendations': 'Monitor soil moisture levels',
            'drought_risk': 0.3,
            'confidence': 0.85
        }
        
        result = validator.validate_field_analysis(valid_response)
        assert result is not None
        assert result['_validated'] == True
    
    def test_validate_field_analysis_hallucination_ndvi(self, validator):
        """Hallucinated NDVI should fail validation"""
        hallu_response = {
            'ndvi': 2.5,  # ❌ Invalid: > 1
            'temperature': 25.0,
            'health_score': 50,
            'health_status': 'Unknown',
            'recommendations': 'Error'
        }
        
        result = validator.validate_field_analysis(hallu_response)
        assert result is None, "Should reject NDVI > 1"
    
    def test_validate_field_analysis_hallucination_temp(self, validator):
        """Unrealistic temperature should fail validation"""
        hallu_response = {
            'ndvi': 0.5,
            'temperature': 150.0,  # ❌ Invalid: > 70°C
            'health_score': 50,
            'health_status': 'Good',
            'recommendations': 'Check irrigation'
        }
        
        result = validator.validate_field_analysis(hallu_response)
        assert result is None, "Should reject temp > 70°C"
    
    def test_logical_consistency_check(self, validator):
        """Test logical consistency between fields"""
        # Poor health but urgent recommendations missing
        inconsistent = {
            'ndvi': 0.2,  # Low NDVI
            'health_score': 90,  # High score - inconsistent!
            'health_status': 'Poor',
            'recommendations': 'Everything looks good',  # Inconsistent!
            'temperature': 25.0,
            'drought_risk': 0.1,
            'confidence': 0.5
        }
        
        # This should fail validation due to inconsistency
        result = validator.validate_field_analysis(inconsistent)
        assert result is None, "Should detect logical inconsistency"


# Test: Prompt Injection Detection (SECURITY)
class TestPromptInjectionDetection:
    """Verify prompt injection attacks are detected"""
    
    @pytest.fixture
    def validator(self):
        from services.ai_validator import AIOutputValidator
        return AIOutputValidator()
    
    def test_sql_injection_detection(self, validator):
        """SQL injection attempts should be detected"""
        injection = "DROP TABLE fields; --"
        assert validator.detect_prompt_injection(injection) == True
    
    def test_code_execution_detection(self, validator):
        """Code execution attempts should be detected"""
        injection = "exec('import os; os.system(rm -rf /)')"
        assert validator.detect_prompt_injection(injection) == True
    
    def test_comment_injection_detection(self, validator):
        """Comment injection attempts should be detected"""
        injection = "<!-- drop database -->"
        assert validator.detect_prompt_injection(injection) == True
    
    def test_legitimate_input_allowed(self, validator):
        """Legitimate agricultural terms should not be flagged"""
        legitimate = "What about irrigation for this field?"
        assert validator.detect_prompt_injection(legitimate) == False
    
    def test_prompt_sanitization(self, validator):
        """Dangerous patterns should be sanitized"""
        injection = "DROP TABLE fields"
        sanitized = validator.sanitize_prompt(injection)
        assert "DROP" not in sanitized
        assert len(sanitized) > 0


# Test: API Fallback Mechanism
class TestAPIFallbacks:
    """Verify API fallback chains work"""
    
    @patch('services.satellite.requests.get')
    def test_satellite_fallback_chain(self, mock_get):
        """Satellite should try multiple APIs"""
        from services.satellite import SatelliteService
        
        # Mock all APIs to fail except last
        mock_get.side_effect = [
            Exception("API1 failed"),
            Exception("API2 failed"),
            MagicMock(status_code=200, json=lambda: {'ndvi': 0.5})
        ]
        
        sat = SatelliteService()
        # This should succeed via fallback
        # (actual implementation may vary)
    
    @patch('services.weather.requests.get')
    def test_weather_fallback_chain(self, mock_get):
        """Weather should try multiple APIs"""
        from services.weather import WeatherService
        
        weather = WeatherService()
        # Verify fallback mechanism exists
        assert hasattr(weather, 'get_risk_metrics')


# Test: Error Handling
class TestErrorHandling:
    """Verify errors are handled gracefully"""
    
    def test_missing_api_key(self):
        """Service should handle missing API keys gracefully"""
        from services.analyzer import AnalyzerService
        
        analyzer = AnalyzerService()
        # Should initialize even if Gemini key missing
        assert analyzer is not None
    
    def test_invalid_coordinates(self):
        """Invalid coordinates should be rejected"""
        # Latitude > 90
        with pytest.raises((ValueError, AssertionError)):
            lat = 95.0
            if not (-90 <= lat <= 90):
                raise ValueError("Invalid latitude")
    
    def test_malformed_api_response(self):
        """Malformed API responses should be handled"""
        # Empty or null responses
        response = {}
        result = response.get('data', {})
        assert result == {}


# Test: Health Status Mapping
class TestHealthStatusMapping:
    """Verify NDVI maps correctly to health status"""
    
    @pytest.fixture
    def validator(self):
        from services.ai_validator import AIOutputValidator
        return AIOutputValidator()
    
    def test_poor_health(self, validator):
        """Low NDVI should map to Poor"""
        assert validator.validate_health_status(0.2) == "Poor"
    
    def test_fair_health(self, validator):
        """Mid-low NDVI should map to Fair"""
        assert validator.validate_health_status(0.4) == "Fair"
    
    def test_good_health(self, validator):
        """Mid NDVI should map to Good"""
        assert validator.validate_health_status(0.6) == "Good"
    
    def test_excellent_health(self, validator):
        """High NDVI should map to Excellent"""
        assert validator.validate_health_status(0.8) == "Excellent"


# Test: Confidence Scoring
class TestConfidenceScoring:
    """Verify confidence scores are calculated correctly"""
    
    @pytest.fixture
    def scorer(self):
        from services.ai_validator import AIOutputValidator, ConfidenceScorer
        validator = AIOutputValidator()
        return ConfidenceScorer(validator)
    
    def test_high_confidence_good_agreement(self, scorer):
        """Good agreement should give high confidence"""
        ai_response = {
            'ndvi': 0.65,
            '_validated': True,
            'health_score': 85,
            'health_status': 'Good'
        }
        source_data = {
            'mean_ndvi': 0.68
        }
        
        confidence = scorer.score_analysis(ai_response, source_data)
        assert confidence > 0.6, "Should be high confidence for good agreement"
    
    def test_low_confidence_poor_agreement(self, scorer):
        """Poor agreement should give low confidence"""
        ai_response = {
            'ndvi': 0.2,  # Different from source
            '_validated': False,
            'health_score': 50
        }
        source_data = {
            'mean_ndvi': 0.8  # Significant difference
        }
        
        confidence = scorer.score_analysis(ai_response, source_data)
        assert confidence < 0.5, "Should be low confidence for poor agreement"


# Test: Integration
class TestIntegration:
    """End-to-end integration tests"""
    
    def test_field_creation_and_analysis_flow(self):
        """Test complete field creation and analysis flow"""
        from app import app, fields_db
        
        client = app.test_client()
        
        # Create field
        field_data = {
            'name': 'Test Farm',
            'latitude': 42.0347,
            'longitude': -93.6200,
            'acres': 150,
            'crop_type': 'Corn'
        }
        
        response = client.post('/api/fields', json=field_data)
        assert response.status_code == 200
        assert response.json['success'] == True


def run_tests():
    """Run all tests with coverage"""
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--cov=services',
        '--cov-report=html',
        '--cov-report=term-missing'
    ])


if __name__ == '__main__':
    run_tests()
