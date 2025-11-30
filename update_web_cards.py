#!/usr/bin/env python3
"""
Update Web App with Latest Cards
This script reads the latest cards from cards_output.json and updates the web app HTML.
Run this after generating new cards with generate_cards.py
"""

import json
import re
from pathlib import Path

# File paths
CARDS_JSON = Path(__file__).parent / "frontend" / "cards" / "cards_output.json"
WEB_APP_HTML = Path(__file__).parent / "web-app" / "index.html"

def load_cards():
    """Load cards from JSON file."""
    try:
        with open(CARDS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('cards', [])
    except Exception as e:
        print(f"❌ Error loading cards: {e}")
        return []

def update_html_with_cards(cards):
    """Update the HTML file with new card data."""
    try:
        # Read current HTML
        with open(WEB_APP_HTML, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert cards to JSON string (formatted nicely)
        cards_json = json.dumps({"cards": cards}, indent=12, ensure_ascii=False)
        
        # Pattern to match the CARD_DATA constant
        pattern = r'const CARD_DATA = \{[^}]*"cards": \[[^\]]*\][^}]*\};'
        
        # Replacement
        replacement = f'const CARD_DATA = {cards_json};'
        
        # Replace
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # Write back
        with open(WEB_APP_HTML, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Successfully updated web app with {len(cards)} cards!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating HTML: {e}")
        return False

def main():
    print("=" * 70)
    print("🔄 Updating Web App with Latest Cards")
    print("=" * 70)
    print()
    
    # Load cards
    print(f"📂 Loading cards from: {CARDS_JSON}")
    cards = load_cards()
    
    if not cards:
        print("⚠️  No cards found or error loading cards.")
        return
    
    print(f"✅ Loaded {len(cards)} cards")
    print()
    
    # Display card info
    print("📇 Card Summary:")
    for i, card in enumerate(cards, 1):
        print(f"  {i}. [{card['type'].upper()}] {card['title']}")
    print()
    
    # Update HTML
    print(f"📝 Updating HTML: {WEB_APP_HTML}")
    success = update_html_with_cards(cards)
    
    if success:
        print()
        print("=" * 70)
        print("✨ Web app updated successfully!")
        print("=" * 70)
        print()
        print("💡 Next steps:")
        print("   1. Open web-app/index.html in your browser")
        print("   2. Refresh if already open (Cmd+R or F5)")
        print("   3. Your new cards will be displayed!")
    else:
        print()
        print("❌ Failed to update web app.")

if __name__ == "__main__":
    main()

