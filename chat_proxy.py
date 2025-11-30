#!/usr/bin/env python3
"""
Simple Backend Proxy for OpenRouter API
Securely handles API key and streams responses
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    print("⚠️  WARNING: OPENROUTER_API_KEY not found in .env file!")

@app.route('/api/chat', methods=['POST'])
def chat():
    """Proxy chat requests to OpenRouter with streaming."""
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', 'openai/gpt-5.1')
        
        # Forward request to OpenRouter
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': request.headers.get('Origin', ''),
            'X-Title': 'AI Persona Cards'
        }
        
        payload = {
            'model': model,
            'messages': messages,
            'stream': True
        }
        
        # Stream response from OpenRouter
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            stream=True
        )
        
        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            return jsonify({
                "error": error_data.get('error', {}).get('message', 'API call failed'),
                "status": response.status_code
            }), response.status_code
        
        def generate():
            for chunk in response.iter_lines():
                if chunk:
                    yield chunk + b'\n'
        
        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            }
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "api_key_configured": bool(OPENROUTER_API_KEY)
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Chat Proxy Server")
    print("=" * 70)
    print(f"📍 Server: http://localhost:5001")
    print(f"🔑 API Key: {'✅ Configured' if OPENROUTER_API_KEY else '❌ Missing'}")
    print()
    print("Endpoints:")
    print("  • POST /api/chat - Chat with streaming")
    print("  • GET  /health - Health check")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    app.run(debug=True, port=5001)

