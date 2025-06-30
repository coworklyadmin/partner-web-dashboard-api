"""Post-related API routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from firebase_admin import firestore

from ..models.post import CommunityPost, PostUpdate
from ..services.auth import verify_firebase_token
from ..services.firestore import get_firestore_client, doc_to_dict

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/")
async def create_post(post: CommunityPost, uid: str = Depends(verify_firebase_token)):
    """Create a new community post"""
    try:
        # Prepare post data
        post_data = post.dict(exclude={'id'}, by_alias=True)
        post_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        # Add to Firestore
        db = get_firestore_client()
        posts_ref = db.collection('posts')
        new_post_ref = posts_ref.add(post_data)[1]
        
        # Get the created document and convert to Pydantic model
        created_post = new_post_ref.get()
        post_data = doc_to_dict(created_post)
        post_model = CommunityPost(**post_data)
        return post_model.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")


@router.get("/{post_id}")
async def get_post(post_id: str, uid: str = Depends(verify_firebase_token)):
    """Fetch a specific post by ID"""
    try:
        db = get_firestore_client()
        post_ref = db.collection('posts').document(post_id)
        post_doc = post_ref.get()
        
        if not post_doc.exists:
            raise HTTPException(status_code=404, detail="Post not found")
        
        post_data = doc_to_dict(post_doc)
        post_model = CommunityPost(**post_data)
        return post_model.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching post: {str(e)}")


@router.patch("/{post_id}")
async def update_post(
    post_id: str, 
    update_data: PostUpdate, 
    uid: str = Depends(verify_firebase_token)
):
    """Update specific fields of a post"""
    try:
        # Convert Pydantic model to dict, excluding None values
        update_dict = update_data.dict(exclude_none=True, by_alias=True)
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        db = get_firestore_client()
        post_ref = db.collection('posts').document(post_id)
        
        # Check if post exists
        post_doc = post_ref.get()
        if not post_doc.exists:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Update the document
        post_ref.update(update_dict)
        
        # Return updated document using Pydantic model
        updated_doc = post_ref.get()
        post_data = doc_to_dict(updated_doc)
        post_model = CommunityPost(**post_data)
        return post_model.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating post: {str(e)}")


@router.delete("/{post_id}")
async def delete_post(post_id: str, uid: str = Depends(verify_firebase_token)):
    """Delete a post by ID"""
    try:
        db = get_firestore_client()
        post_ref = db.collection('posts').document(post_id)
        
        # Check if post exists
        post_doc = post_ref.get()
        if not post_doc.exists:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Delete the document
        post_ref.delete()
        
        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting post: {str(e)}")


@router.get("/space/{space_id}")
async def get_posts_by_space(space_id: str, uid: str = Depends(verify_firebase_token)):
    """Fetch all posts for a specific space"""
    try:
        db = get_firestore_client()
        posts_query = db.collection('posts').where('space_id', '==', space_id).order_by('created_at', direction=firestore.Query.DESCENDING)
        posts_docs = posts_query.stream()
        
        posts = []
        for doc in posts_docs:
            post_data = doc_to_dict(doc)
            post_model = CommunityPost(**post_data)
            posts.append(post_model.model_dump())
        
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching posts: {str(e)}") 