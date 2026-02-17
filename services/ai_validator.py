# AI Output Validation & Safeguards Module
# services/ai_validator.py

import logging
from typing import Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class AIOutputValidator:
    """
    Validates AI-generated responses to prevent hallucinations and ensure
    output is within reasonable bounds for agricultural data.
    """
    
    # Define valid ranges for different metrics
    VALID_RANGES = {
        'ndvi': (-1.0, 1.0),  # Normalized Difference Vegetation Index
        'temperature': (-70, 70),  # Celsius
        'precipitation': (0, 500),  # mm
        'humidity': (0, 100),  # percentage
        'wind_speed': (0, 150),  # km/h
        'drought_risk': (0, 1),  # probability
        'health_score': (0, 100),  # percentage
        'confidence': (0, 1),  # probability
    }
    
    def __init__(self):
        self.validation_log = []
    
    def validate_field_analysis(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Validate complete field analysis response.
        
        Args:
            response: AI-generated field analysis
            
        Returns:
            Validated response or None if invalid
        """
        if not response:
            logger.warning("Empty response provided for validation")
            return None
        
        # Check all numeric fields are within bounds
        for field, (min_val, max_val) in self.VALID_RANGES.items():
            if field in response:
                value = response.get(field)
                if value is not None:
                    if not (min_val <= value <= max_val):
                        logger.warning(
                            f"❌ Hallucination detected: {field}={value} "
                            f"not in range [{min_val}, {max_val}]"
                        )
                        self._log_violation(field, value, (min_val, max_val))
                        return None
        
        # Validate logical consistency
        if not self._check_logical_consistency(response):
            logger.warning("❌ Logical consistency check failed")
            return None
        
        # Check response has required fields
        required_fields = ['health_status', 'recommendations']
        if not all(field in response for field in required_fields):
            logger.warning(f"❌ Missing required fields: {required_fields}")
            return None
        
        # Mark as validated
        response['_validated'] = True
        response['_validation_timestamp'] = datetime.now().isoformat()
        
        logger.info("✅ AI response passed validation")
        return response
    
    def validate_ndvi(self, ndvi_value: float) -> bool:
        """
        Validate NDVI (Normalized Difference Vegetation Index) value.
        
        NDVI ranges:
        - < 0.0: Water bodies
        - 0.0-0.3: Bare soil or urban
        - 0.3-0.6: Sparse vegetation
        - 0.6-1.0: Dense vegetation
        
        Args:
            ndvi_value: NDVI value to validate
            
        Returns:
            True if valid, False otherwise
        """
        min_val, max_val = self.VALID_RANGES['ndvi']
        
        if not (min_val <= ndvi_value <= max_val):
            logger.warning(f"❌ Invalid NDVI: {ndvi_value}")
            return False
        
        logger.info(f"✅ Valid NDVI: {ndvi_value}")
        return True
    
    def validate_health_status(self, ndvi: float) -> str:
        """
        Determine realistic health status based on NDVI.
        
        Args:
            ndvi: NDVI value
            
        Returns:
            Health status string
        """
        if ndvi < 0.3:
            return "Poor"
        elif ndvi < 0.5:
            return "Fair"
        elif ndvi < 0.7:
            return "Good"
        else:
            return "Excellent"
    
    def _check_logical_consistency(self, response: Dict[str, Any]) -> bool:
        """
        Check if different fields in response are logically consistent.
        
        Example: If health_score is 90, then recommendations should not
        suggest complete crop failure.
        """
        health_score = response.get('health_score', 50)
        health_status = response.get('health_status', 'Unknown')
        ndvi = response.get('ndvi', 0)
        recommendations = response.get('recommendations', '')
        
        # Check consistency: health_score should correlate with NDVI
        if health_score > 80 and ndvi < 0.3:
            logger.warning("❌ Inconsistency: high score but low NDVI")
            self._log_violation('logical_consistency', 
                              f"score={health_score}, ndvi={ndvi}",
                              None)
            return False
        
        # Check: if poor health, recommendations should suggest intervention
        if health_status == 'Poor' and not any(word in recommendations.lower() 
                                               for word in ['urgent', 'immediately', 'critical']):
            logger.warning("❌ Inconsistency: poor status but recommendation lacks urgency")
            return False
        
        return True
    
    def _log_violation(self, field: str, value: Any, expected_range: Optional[tuple]) -> None:
        """Log validation violation for audit trail."""
        violation = {
            'timestamp': datetime.now().isoformat(),
            'field': field,
            'value': value,
            'expected_range': expected_range,
            'severity': 'HIGH'
        }
        self.validation_log.append(violation)
        logger.error(f"🚨 Violation: {json.dumps(violation)}")
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Get validation violations report."""
        return {
            'total_validations': len(self.validation_log),
            'violations': self.validation_log,
            'last_violation': self.validation_log[-1] if self.validation_log else None
        }
    
    @classmethod
    def detect_prompt_injection(cls, prompt: str) -> bool:
        """
        Detect common prompt injection attack patterns.
        
        Args:
            prompt: User input to check
            
        Returns:
            True if injection detected, False otherwise
        """
        dangerous_patterns = [
            'DROP', 'DELETE', 'UNION', 'SELECT',  # SQL injection
            '<!--', '-->', '/*', '*/',  # Comment injection
            'exec(', 'eval(', '__import__',  # Code execution
            'system(', 'os.system',  # System commands
        ]
        
        prompt_upper = prompt.upper()
        for pattern in dangerous_patterns:
            if pattern in prompt_upper:
                logger.warning(f"🚨 Prompt injection attempt detected: {pattern}")
                return True
        
        return False
    
    @classmethod
    def sanitize_prompt(cls, user_input: str) -> str:
        """
        Sanitize user input to prevent prompt injection.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Sanitized input safe for AI processing
        """
        # Remove dangerous patterns (but keep intent)
        dangerous_patterns = {
            'DROP': 'REMOVE',
            'DELETE': 'ERASE',
            'UNION': 'COMBINE',
            '<!--': '',
            '-->': '',
            '/*': '',
            '*/': ''
        }
        
        sanitized = user_input
        for dangerous, replacement in dangerous_patterns.items():
            sanitized = sanitized.replace(dangerous, replacement)
        
        # Limit input length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            logger.warning(f"Input truncated to {max_length} characters")
        
        return sanitized.strip()


class ConfidenceScorer:
    """Score confidence in AI responses based on multiple factors."""
    
    def __init__(self, validator: AIOutputValidator):
        self.validator = validator
    
    def score_analysis(self, ai_response: Dict, source_data: Dict) -> float:
        """
        Calculate confidence score (0-1) for AI response.
        
        Factors:
        - Agreement with source data (satellite, weather APIs)
        - Logical consistency
        - Validation pass
        - Historical pattern match
        
        Args:
            ai_response: AI-generated analysis
            source_data: Data from satellite/weather APIs
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.0
        
        # Factor 1: Validation pass (40%)
        if ai_response.get('_validated'):
            confidence += 0.4
        
        # Factor 2: Agreement with source data (30%)
        if self._check_source_agreement(ai_response, source_data):
            confidence += 0.3
        
        # Factor 3: Logical consistency (20%)
        if self.validator._check_logical_consistency(ai_response):
            confidence += 0.2
        
        # Factor 4: Bounded reasonable values (10%)
        if self._check_all_fields_reasonable(ai_response):
            confidence += 0.1
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _check_source_agreement(self, ai_response: Dict, source_data: Dict) -> bool:
        """Check if AI response agrees with source data within tolerance."""
        # NDVI tolerance: ±0.15
        ai_ndvi = ai_response.get('ndvi', 0)
        source_ndvi = source_data.get('mean_ndvi', 0)
        
        if abs(ai_ndvi - source_ndvi) > 0.15:
            logger.warning(f"⚠️ NDVI disagreement: AI={ai_ndvi}, Source={source_ndvi}")
            return False
        
        return True
    
    def _check_all_fields_reasonable(self, response: Dict) -> bool:
        """Check if all numeric fields are reasonable."""
        for field, (min_val, max_val) in AIOutputValidator.VALID_RANGES.items():
            if field in response:
                value = response.get(field)
                if value is not None:
                    if not (min_val <= value <= max_val):
                        return False
        return True


# Example usage in analyzer.py
if __name__ == "__main__":
    validator = AIOutputValidator()
    
    # Test valid response
    valid_response = {
        'ndvi': 0.65,
        'temperature': 25.5,
        'health_score': 85,
        'health_status': 'Good',
        'recommendations': 'Irrigation system perform optimally. Monitor for pest activity.'
    }
    
    result = validator.validate_field_analysis(valid_response)
    print(f"Valid response test: {'✅ PASS' if result else '❌ FAIL'}")
    
    # Test hallucination (invalid NDVI)
    hallucinated_response = {
        'ndvi': 2.5,  # Invalid: > 1
        'temperature': 200,  # Invalid: unrealistic
        'health_score': 50,
        'health_status': 'Unknown',
        'recommendations': 'Data error'
    }
    
    result = validator.validate_field_analysis(hallucinated_response)
    print(f"Hallucination test: {'❌ DETECTED' if not result else 'MISS'}")
    
    # Test prompt injection
    injection_attempt = "DROP TABLE fields; --"
    is_injection = validator.detect_prompt_injection(injection_attempt)
    print(f"Injection detection: {'✅ DETECTED' if is_injection else 'MISS'}")
