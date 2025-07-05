#!/usr/bin/env python3
"""
Example script demonstrating the Dashboard Metrics API.

This script shows how to:
1. Set up the required environment variables
2. Make requests to the dashboard metrics endpoint with different date ranges
3. Handle the response and errors

Usage:
    python examples/dashboard_metrics_example.py
"""

import os
import requests
import json
from typing import Dict, Any
from datetime import datetime, timedelta


def setup_environment():
    """Set up required environment variables for testing."""
    # These would normally be set in your deployment environment
    os.environ.setdefault("AMPLITUDE_API_KEY", "your_amplitude_api_key")
    os.environ.setdefault("AMPLITUDE_SECRET_KEY", "your_amplitude_secret_key")
    os.environ.setdefault("FERNET_KEY", "your_fernet_encryption_key")
    os.environ.setdefault("FIREBASE_PROJECT_ID", "your_firebase_project_id")


def fetch_dashboard_metrics(base_url: str, firebase_token: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """
    Fetch dashboard metrics from the API.
    
    Args:
        base_url: Base URL of the API (e.g., "http://localhost:8080")
        firebase_token: Valid Firebase ID token
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format
        
    Returns:
        Dictionary containing dashboard metrics
    """
    url = f"{base_url}/dashboard-metrics/"
    
    # Build query parameters
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    headers = {
        "Authorization": f"Bearer {firebase_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return {}


def display_metrics(metrics: Dict[str, Any], date_range: str = "Last 30 days"):
    """Display the dashboard metrics in a formatted way."""
    if not metrics:
        print("No metrics received")
        return
    
    print(f"\n📊 Dashboard Metrics - {date_range}")
    print("=" * 60)
    
    metric_descriptions = {
        "profileViews": "Profile Views",
        "favoritesAdded": "Favorites Added", 
        "favoritesRemoved": "Favorites Removed",
        "markerTaps": "Marker Taps",
        "listViewTaps": "List View Taps",
        "reviewsBrowsed": "Reviews Browsed",
        "reviewsAdded": "Reviews Added",
        "externalLinks": "External Links"
    }
    
    for key, description in metric_descriptions.items():
        value = metrics.get(key, 0)
        print(f"{description:20}: {value:>8}")
    
    print("=" * 60)
    
    # Calculate totals
    total_interactions = sum(metrics.values())
    print(f"Total Interactions: {total_interactions:>8}")


def generate_date_ranges():
    """Generate example date ranges for demonstration."""
    today = datetime.now()
    
    return {
        "Last 7 days": {
            "start_date": (today - timedelta(days=7)).strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d")
        },
        "Last 30 days": {
            "start_date": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d")
        },
        "This month": {
            "start_date": today.replace(day=1).strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d")
        },
        "Last month": {
            "start_date": (today.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d"),
            "end_date": (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
        }
    }


def main():
    """Main function demonstrating the API usage."""
    print("🚀 Dashboard Metrics API Example")
    print("=" * 60)
    
    # Set up environment
    setup_environment()
    
    # Configuration
    base_url = "http://localhost:8080"  # Change this to your API URL
    firebase_token = "your_firebase_id_token_here"  # Replace with actual token
    
    print(f"API Base URL: {base_url}")
    print(f"Firebase Token: {firebase_token[:20]}..." if len(firebase_token) > 20 else "Token not set")
    
    # Generate example date ranges
    date_ranges = generate_date_ranges()
    
    # Example 1: Default (last 30 days)
    print("\n📡 Example 1: Fetching default metrics (last 30 days)...")
    metrics = fetch_dashboard_metrics(base_url, firebase_token)
    display_metrics(metrics, "Last 30 days (default)")
    
    # Example 2: Last 7 days
    print("\n📡 Example 2: Fetching metrics for last 7 days...")
    last_7_days = date_ranges["Last 7 days"]
    metrics = fetch_dashboard_metrics(
        base_url, 
        firebase_token, 
        start_date=last_7_days["start_date"],
        end_date=last_7_days["end_date"]
    )
    display_metrics(metrics, "Last 7 days")
    
    # Example 3: This month
    print("\n📡 Example 3: Fetching metrics for this month...")
    this_month = date_ranges["This month"]
    metrics = fetch_dashboard_metrics(
        base_url, 
        firebase_token, 
        start_date=this_month["start_date"],
        end_date=this_month["end_date"]
    )
    display_metrics(metrics, "This month")
    
    # Example 4: Custom date range
    print("\n📡 Example 4: Fetching metrics for custom date range...")
    custom_start = "2024-01-01"
    custom_end = "2024-01-31"
    metrics = fetch_dashboard_metrics(
        base_url, 
        firebase_token, 
        start_date=custom_start,
        end_date=custom_end
    )
    display_metrics(metrics, f"Custom range: {custom_start} to {custom_end}")
    
    # Example 5: Start date only (end date defaults to today)
    print("\n📡 Example 5: Fetching metrics from start date to today...")
    start_only = "2024-01-15"
    metrics = fetch_dashboard_metrics(
        base_url, 
        firebase_token, 
        start_date=start_only
    )
    display_metrics(metrics, f"From {start_only} to today")
    
    # Example insights
    if metrics:
        print("\n📈 Dashboard Insights:")
        if metrics.get("profileViews", 0) > 0:
            print(f"• Your profile was viewed {metrics['profileViews']} times")
        
        if metrics.get("favoritesAdded", 0) > metrics.get("favoritesRemoved", 0):
            net_favorites = metrics["favoritesAdded"] - metrics["favoritesRemoved"]
            print(f"• Net favorites: +{net_favorites}")
        
        if metrics.get("reviewsAdded", 0) > 0:
            print(f"• {metrics['reviewsAdded']} new reviews were added")
        
        if metrics.get("externalLinks", 0) > 0:
            print(f"• {metrics['externalLinks']} external links were clicked")
    
    print("\n✅ API Examples completed!")
    print("\n💡 Tips:")
    print("• Use YYYY-MM-DD format for dates")
    print("• If no dates provided, defaults to last 30 days")
    print("• You can specify start_date only, end_date only, or both")
    print("• start_date cannot be after end_date")


if __name__ == "__main__":
    main() 