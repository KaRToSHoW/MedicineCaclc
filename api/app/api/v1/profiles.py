"""
Profile API endpoints
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.core.firebase_auth import get_current_user_firebase
from app.core.firestore import get_firestore_client
from app.schemas import ProfileUpdate

router = APIRouter()


@router.get("/profiles/me")
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user_firebase)):
    """Get current user profile"""
    return current_user


@router.patch("/profiles/me")
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user_firebase)
):
    """Update current user profile"""
    db = get_firestore_client()
    users_ref = db.collection('users')
    user_doc_ref = users_ref.document(current_user['id'])
    
    # Prepare update data
    update_data = {}
    if profile_data.name is not None:
        update_data['name'] = profile_data.name
    
    if profile_data.email is not None:
        update_data['email'] = profile_data.email
    
    # Update Firestore document
    if update_data:
        user_doc_ref.update(update_data)
        
        # Get updated user data
        updated_doc = user_doc_ref.get()
        if updated_doc.exists:
            return updated_doc.to_dict()
    
    return current_user
