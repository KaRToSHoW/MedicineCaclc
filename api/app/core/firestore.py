"""
Firestore Database Client
Replaces PostgreSQL with Firestore for data storage
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from firebase_admin import firestore


def get_firestore_client():
    """Get Firestore client (call after Firebase Admin SDK is initialized)"""
    return firestore.client()


# Collections
USERS_COLLECTION = "users"
CALCULATION_RESULTS_COLLECTION = "calculation_results"


class FirestoreUser:
    """User operations in Firestore"""
    
    @staticmethod
    async def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        db = get_firestore_client()
        users_ref = db.collection(USERS_COLLECTION)
        query = users_ref.where("email", "==", email).limit(1)
        docs = query.stream()
        
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        
        return None
    
    @staticmethod
    async def get_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        db = get_firestore_client()
        doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            return user_data
        
        return None
    
    @staticmethod
    async def create(email: str, name: str, firebase_uid: str) -> Dict[str, Any]:
        """Create new user"""
        db = get_firestore_client()
        user_data = {
            "email": email,
            "name": name,
            "firebase_uid": firebase_uid,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        
        # Add user to Firestore
        doc_ref = db.collection(USERS_COLLECTION).document()
        doc_ref.set(user_data)
        
        # Return created user with ID
        user_data['id'] = doc_ref.id
        return user_data


class FirestoreCalculationResult:
    """Calculation result operations in Firestore"""
    
    @staticmethod
    async def create(
        user_id: str,
        calculator_name: str,
        calculator_name_ru: Optional[str],
        input_data: Dict[str, Any],
        result_value: float,
        interpretation: Optional[str]
    ) -> Dict[str, Any]:
        """Create new calculation result"""
        db = get_firestore_client()
        result_data = {
            "user_id": user_id,
            "calculator_name": calculator_name,
            "calculator_name_ru": calculator_name_ru,
            "input_data": input_data,
            "result_value": result_value,
            "interpretation": interpretation,
            "performed_at": firestore.SERVER_TIMESTAMP
        }
        
        # Add to Firestore
        doc_ref = db.collection(CALCULATION_RESULTS_COLLECTION).document()
        doc_ref.set(result_data)
        
        # Return created result with ID
        result_data['id'] = doc_ref.id
        result_data['performed_at'] = datetime.utcnow()
        return result_data
    
    @staticmethod
    async def get_by_user(user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all calculation results for user"""
        db = get_firestore_client()
        results_ref = db.collection(CALCULATION_RESULTS_COLLECTION)
        # Simple query without order_by to avoid composite index requirement
        query = results_ref.where("user_id", "==", user_id).limit(limit)
        docs = query.stream()
        
        results = []
        for doc in docs:
            result_data = doc.to_dict()
            result_data['id'] = doc.id
            # Convert Firestore timestamp to ISO string if present
            if 'performed_at' in result_data and result_data['performed_at']:
                try:
                    result_data['performed_at'] = result_data['performed_at'].isoformat()
                except:
                    pass
            results.append(result_data)
        
        # Sort in Python after fetching (avoid Firestore composite index)
        results.sort(key=lambda x: x.get('performed_at', ''), reverse=True)
        
        return results
    
    @staticmethod
    async def get_by_id(result_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get specific calculation result"""
        db = get_firestore_client()
        doc_ref = db.collection(CALCULATION_RESULTS_COLLECTION).document(result_id)
        doc = doc_ref.get()
        
        if doc.exists:
            result_data = doc.to_dict()
            result_data['id'] = doc.id
            
            # Verify ownership
            if result_data.get('user_id') == user_id:
                return result_data
        
        return None
    
    @staticmethod
    async def delete(result_id: str, user_id: str) -> bool:
        """Delete calculation result"""
        db = get_firestore_client()
        doc_ref = db.collection(CALCULATION_RESULTS_COLLECTION).document(result_id)
        doc = doc_ref.get()
        
        if doc.exists:
            result_data = doc.to_dict()
            
            # Verify ownership
            if result_data.get('user_id') == user_id:
                doc_ref.delete()
                return True
        
        return False

