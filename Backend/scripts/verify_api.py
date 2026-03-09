#!/usr/bin/env python
"""Verify API endpoints are working correctly"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
import json

client = Client()

print("=" * 60)
print("Testing API Endpoints")
print("=" * 60)

# Test establishments
print("\n1. Testing GET /api/establishments/")
try:
    response = client.get('/api/establishments/')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.content)
        # Check if results key exists (paginated response)
        if 'results' in data:
            count = len(data['results'])
            print(f"   ✓ Response contains {count} establishments")
            if count > 0:
                first = data['results'][0]
                print(f"   ✓ First establishment: {first.get('name', 'N/A')}")
        else:
            count = len(data) if isinstance(data, list) else 'unknown'
            print(f"   ✓ Response contains {count} establishments (non-paginated)")
    else:
        print(f"   ✗ Error: {response.content}")
except Exception as e:
    print(f"   ✗ Exception: {str(e)}")

# Test categories
print("\n2. Testing GET /api/categories/")
try:
    response = client.get('/api/categories/')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.content)
        if 'results' in data:
            count = len(data['results'])
            print(f"   ✓ Response contains {count} categories")
        else:
            count = len(data) if isinstance(data, list) else 'unknown'
            print(f"   ✓ Response contains {count} categories")
    else:
        print(f"   ✗ Error: {response.content}")
except Exception as e:
    print(f"   ✗ Exception: {str(e)}")

# Test by_category endpoint
print("\n3. Testing GET /api/establishments/by_category/?category=almuerzos")
try:
    response = client.get('/api/establishments/by_category/?category=almuerzos')
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.content)
        count = len(data) if isinstance(data, list) else 'unknown'
        print(f"   ✓ Response contains {count} establishments in almuerzos category")
    else:
        print(f"   ✗ Error: {response.content}")
except Exception as e:
    print(f"   ✗ Exception: {str(e)}")

print("\n" + "=" * 60)
print("API verification complete!")
print("=" * 60)
