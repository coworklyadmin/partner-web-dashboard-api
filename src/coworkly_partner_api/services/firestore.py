"""Firestore database services."""

from firebase_admin import firestore
from google.cloud.firestore import Client


def get_firestore_client() -> Client:
    """Get Firestore client instance."""
    return firestore.client()


def doc_to_dict(doc):
    """Convert Firestore document to dictionary with ID."""
    if not doc.exists:
        return None
    data = doc.to_dict()
    data['id'] = doc.id
    return data 