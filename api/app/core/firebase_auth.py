"""
Firebase Authentication for Backend
Verifies Firebase ID tokens from frontend using Firebase Admin SDK
"""
import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

from app.core.firestore import FirestoreUser

# HTTP Bearer token
security = HTTPBearer()

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    if not firebase_admin._apps:
        # Path to service account JSON file
        cred_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            '..',
            'medcalc-71fb2-firebase-adminsdk-fbsvc-14a7ed45c0.json'
        )
        
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print(f"✅ Firebase Admin SDK initialized with service account")
        else:
            raise Exception(f"Service account file not found: {cred_path}")


async def get_current_user_firebase(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current authenticated user from Firebase token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        print(f"🔑 Received token (first 20 chars): {token[:20]}...")
        
        # Verify Firebase ID token using Admin SDK
        decoded_token = firebase_auth.verify_id_token(token)
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email')
        
        print(f"✅ Token verified - UID: {firebase_uid}, Email: {email}")
        
        if not firebase_uid:
            print("❌ No Firebase UID in token")
            raise credentials_exception
            
    except Exception as e:
        print(f"❌ Firebase token verification failed: {type(e).__name__}: {e}")
        raise credentials_exception
    
    # Get or create user in Firestore
    user = await FirestoreUser.get_by_email(email)
    
    if user is None:
        # Auto-create user from Firebase
        user = await FirestoreUser.create(
            email=email,
            name=email.split('@')[0],  # Use email prefix as default name
            firebase_uid=firebase_uid
        )
        print(f"✅ Auto-created user in Firestore: {email}")
    else:
        print(f"👤 Found existing user: {email}")
    
    return user
