"""
External API integration services for medical data
"""
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MedicalDataService:
    """
    Service for integrating with external medical databases
    (Example integration - can be replaced with real APIs)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.example-medical-db.com/v1"
    
    def get_reference_ranges(self, test_name: str, age: int, gender: str) -> Optional[Dict[str, Any]]:
        """
        Get reference ranges for a medical test
        
        Args:
            test_name: Name of the medical test (e.g., 'glucose', 'cholesterol')
            age: Patient age in years
            gender: Patient gender ('male' or 'female')
        
        Returns:
            Dict with reference ranges or None if not found
        """
        try:
            # Example API call (would need real API)
            # response = requests.get(
            #     f"{self.base_url}/reference-ranges/{test_name}",
            #     params={"age": age, "gender": gender},
            #     headers={"Authorization": f"Bearer {self.api_key}"}
            # )
            # return response.json()
            
            # Mock data for demonstration
            reference_data = {
                'bmi': {
                    'underweight': {'max': 18.5},
                    'normal': {'min': 18.5, 'max': 24.9},
                    'overweight': {'min': 25.0, 'max': 29.9},
                    'obese': {'min': 30.0}
                },
                'glucose': {
                    'normal': {'min': 70, 'max': 100},
                    'prediabetes': {'min': 100, 'max': 125},
                    'diabetes': {'min': 126}
                }
            }
            
            return reference_data.get(test_name.lower())
        except Exception as e:
            logger.error(f"Error fetching reference ranges: {e}")
            return None
    
    def search_icd10_codes(self, query: str) -> List[Dict[str, str]]:
        """
        Search ICD-10 diagnostic codes
        
        Args:
            query: Search query string
        
        Returns:
            List of matching ICD-10 codes
        """
        try:
            # Mock data for demonstration
            icd10_database = [
                {'code': 'E66.0', 'description': 'Obesity due to excess calories'},
                {'code': 'E66.9', 'description': 'Obesity, unspecified'},
                {'code': 'I10', 'description': 'Essential (primary) hypertension'},
                {'code': 'E11.9', 'description': 'Type 2 diabetes mellitus without complications'},
            ]
            
            results = [
                item for item in icd10_database
                if query.lower() in item['description'].lower() or query.upper() in item['code']
            ]
            
            return results[:10]  # Return top 10 matches
        except Exception as e:
            logger.error(f"Error searching ICD-10 codes: {e}")
            return []


class AnalyticsService:
    """
    Service for sending usage analytics to external services
    (Google Analytics, Mixpanel, etc.)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def track_event(
        self,
        event_name: str,
        user_id: Optional[int] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Track user event
        
        Args:
            event_name: Name of the event (e.g., 'calculation_performed')
            user_id: User ID
            properties: Additional event properties
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            event_data = {
                'event': event_name,
                'user_id': user_id,
                'properties': properties or {},
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Example: Send to analytics service
            # response = requests.post(
            #     "https://api.analytics-service.com/events",
            #     json=event_data,
            #     headers={"Authorization": f"Bearer {self.api_key}"}
            # )
            # return response.status_code == 200
            
            logger.info(f"Analytics event tracked: {event_name}")
            return True
        except Exception as e:
            logger.error(f"Error tracking analytics event: {e}")
            return False
    
    def track_calculation(
        self,
        calculator_name: str,
        calculator_category: str,
        user_id: Optional[int] = None
    ) -> bool:
        """Track calculation event"""
        return self.track_event(
            'calculation_performed',
            user_id=user_id,
            properties={
                'calculator_name': calculator_name,
                'calculator_category': calculator_category
            }
        )


class PushNotificationService:
    """
    Service for sending push notifications
    (Firebase Cloud Messaging, OneSignal, etc.)
    """
    
    def __init__(self, server_key: Optional[str] = None):
        self.server_key = server_key
        self.enabled = bool(server_key)
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"
    
    def send_notification(
        self,
        user_token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send push notification to user device
        
        Args:
            user_token: FCM device token
            title: Notification title
            body: Notification body
            data: Additional data payload
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            payload = {
                'to': user_token,
                'notification': {
                    'title': title,
                    'body': body,
                    'sound': 'default'
                },
                'data': data or {}
            }
            
            headers = {
                'Authorization': f'key={self.server_key}',
                'Content-Type': 'application/json'
            }
            
            # response = requests.post(self.fcm_url, json=payload, headers=headers)
            # return response.status_code == 200
            
            logger.info(f"Push notification sent: {title}")
            return True
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
            return False
    
    def send_reminder(
        self,
        user_token: str,
        calculator_name: str,
        scheduled_time: datetime
    ) -> bool:
        """Send calculation reminder"""
        return self.send_notification(
            user_token,
            title="Напоминание о расчете",
            body=f"Пора выполнить расчет: {calculator_name}",
            data={
                'type': 'reminder',
                'calculator_name': calculator_name,
                'scheduled_time': scheduled_time.isoformat()
            }
        )


# Initialize services (in production, load from environment variables)
medical_data_service = MedicalDataService()
analytics_service = AnalyticsService()
push_notification_service = PushNotificationService()
