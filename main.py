#!/usr/bin/env python3
"""
Main entry point for the CoWorkly Partner Dashboard API.
Supports both Firebase Functions deployment and local development.
"""

import json
import asyncio
import os
from functools import partial
from urllib.parse import parse_qs, urlparse

import firebase_functions
from firebase_functions import https_fn
from firebase_admin import initialize_app

# Import our FastAPI app
from src.coworkly_partner_api.app import app
from src.coworkly_partner_api.utils.config import settings

# Initialize Firebase Admin SDK only if not already initialized
try:
    initialize_app()
except ValueError:
    # App already initialized, continue
    pass

@https_fn.on_request()
def coworkly_partner_api(req: https_fn.Request) -> https_fn.Response:
    """Firebase Function entry point for the CoWorkly Partner Dashboard API"""
    
    # Debug logging
    print(f"Request method: {req.method}")
    print(f"Request URL: {req.url}")
    print(f"Request headers: {dict(req.headers)}")
    print(f"Request data: {req.data}")
    
    # Test JSON parsing
    try:
        if req.data:
            parsed_json = json.loads(req.data)
            print(f"Parsed JSON: {parsed_json}")
        else:
            print("No request data to parse")
    except Exception as e:
        print(f"JSON parsing error: {e}")
    
    # Handle CORS preflight requests
    if req.method == 'OPTIONS':
        print("Handling OPTIONS preflight request")
        return https_fn.Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Max-Age': '86400',
            }
        )
    
    # Parse the URL
    parsed_url = urlparse(req.url)
    path = parsed_url.path
    query_string = parsed_url.query
    
    print(f"Parsed path: {path}")
    print(f"Query string: {query_string}")
    
    try:
        # Convert Firebase Function request to ASGI scope
        scope = {
            'type': 'http',
            'asgi': {'version': '3.0'},
            'http_version': '1.1',
            'method': req.method,
            'scheme': 'https',
            'server': ('localhost', 8080),
            'path': path,
            'query_string': query_string.encode() if query_string else b'',
            'headers': [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
            'client': ('127.0.0.1', 0),
        }
        
        print(f"ASGI scope created: {scope}")
        
        # Process the request
        response = asyncio.run(handle_request(scope, req))
        print(f"Response status: {response.status}")
        print(f"Response headers: {response.headers}")
        return response
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        # Return error response
        return https_fn.Response(
            status=500,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Content-Type': 'application/json'
            },
            response=json.dumps({
                "detail": f"Internal server error: {str(e)}",
                "error_type": str(type(e))
            })
        )

async def handle_request(scope, req):
    """Handle the ASGI request and return a Firebase Function response"""
    
    response_body = b''
    response_headers = []
    response_status = 200
    
    # Prepare the request body
    if req.data:
        if isinstance(req.data, str):
            body = req.data.encode('utf-8')
        else:
            body = req.data  # Already bytes
    else:
        body = b''
    body_sent = False
    print(f"Prepared body: {body}")
    print(f"Body length: {len(body)}")
    
    async def receive():
        """Receive function for ASGI"""
        nonlocal body_sent
        if not body_sent:
            body_sent = True
            print(f"ASGI receive: sending body of length {len(body)}")
            return {'type': 'http.request', 'body': body}
        else:
            print("ASGI receive: sending empty body")
            return {'type': 'http.request', 'body': b''}
    
    async def send(message):
        """Send function for ASGI"""
        nonlocal response_body, response_headers, response_status
        
        if message['type'] == 'http.response.start':
            response_status = message['status']
            response_headers = message['headers']
            print(f"FastAPI response status: {response_status}")
            print(f"FastAPI response headers: {response_headers}")
        elif message['type'] == 'http.response.body':
            response_body += message['body']
            print(f"FastAPI response body chunk: {message['body']}")
    
    # Process the request through FastAPI
    await app(scope, receive, send)
    
    # Log the complete response
    print(f"Complete response body: {response_body}")
    
    # Convert headers to dict
    headers_dict = {}
    for name, value in response_headers:
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        headers_dict[name] = value
    
    # Return Firebase Function response
    return https_fn.Response(
        status=response_status,
        headers=headers_dict,
        response=response_body.decode('utf-8') if response_body else ''
    )

# Local development server
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting CoWorkly Partner Dashboard API (Local Development)")
    print(f"📍 Server: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 API Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"🔧 Debug Mode: {settings.DEBUG}")
    print("=" * 60)
    
    uvicorn.run(
        "src.coworkly_partner_api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 