#!/usr/bin/env python3
"""
Card Generator Script
Reads persona profile output and generates personalized card elements 
for the frontend using OpenRouter API (GPT-5.1).
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model configuration
MODEL_NAME = "openai/gpt-5.1"

# File paths
PERSONA_OUTPUT_FILE = "../../outputs/kirana_shop_output.json"
CARDS_OUTPUT_FILE = "cards_output.json"

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Card generation prompt template
CARD_GENERATION_PROMPT = """You are a personalization expert creating relevant, helpful content cards for a mobile app user in India.

Based on the user profile and context below, generate 4 personalized cards with content that is:
- Highly relevant to the user's current situation and needs
- Written in simple Hindi (Hinglish if technical terms needed)
- Actionable and helpful
- Appropriate for their device constraints and context

USER PROFILE DATA:
{USER_PROFILE_JSON}

REQUIRED OUTPUT FORMAT:
Generate exactly 4 cards with these types: "money", "kids", "govt", "phone"

Each card must have:
- type: one of ["money", "kids", "govt", "phone"]
- title: Short Hindi title (2-5 words)
- body: Helpful content in Hindi (20-40 words, simple language)

CARD GUIDELINES:
1. "money" card: Financial tips, savings advice, EMI reminders, cashflow management for small shop owners
2. "kids" card: Education tips, school information, scholarship opportunities, learning resources
3. "govt" card: Relevant government schemes, subsidies, benefits applicable to their situation
4. "phone" card: Phone optimization, battery saving, data saving tips, app management

Return ONLY valid JSON in this exact format:
{
  "cards": [
    {
      "type": "money",
      "title": "आज का बचत टिप",
      "body": "छोटा, आसान हिंदी में समझाया हुआ बचत या पैसे का टिप।"
    },
    {
      "type": "kids",
      "title": "बच्चों की पढ़ाई",
      "body": "बच्चों की पढ़ाई, स्कूल या स्कॉलरशिप से जुड़ा छोटा सलाह या जानकारी।"
    },
    {
      "type": "govt",
      "title": "सरकारी योजना",
      "body": "यूज़र के लिए काम की किसी सरकारी योजना या योजना से जुड़ा सरल सारांश।"
    },
    {
      "type": "phone",
      "title": "फोन और डाटा",
      "body": "फोन की बैटरी, डाटा या रीचार्ज बचाने से जुड़ा छोटा टिप।"
    }
  ]
}

Make the content specific to this user's:
- Current battery level and phone constraints
- Business type (kirana shop)
- Location and local context
- Financial behavior and needs
- Family situation
- Device limitations"""

# ============================================================================
# MAIN LOGIC
# ============================================================================

def load_json_file(file_path: str) -> dict:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as a dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded JSON from: {file_path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"❌ Invalid JSON in {file_path}: {str(e)}", e.doc, e.pos)


def create_card_generation_prompt(user_profile: dict) -> str:
    """
    Create the prompt for card generation by injecting user profile data.
    
    Args:
        user_profile: Dictionary containing user profile data
        
    Returns:
        Complete prompt string for the API
    """
    # Convert profile to pretty JSON string
    profile_json = json.dumps(user_profile, indent=2, ensure_ascii=False)
    
    # Inject into prompt template
    prompt = CARD_GENERATION_PROMPT.replace("{USER_PROFILE_JSON}", profile_json)
    
    print("✅ Card generation prompt created")
    return prompt


def call_openrouter_api(prompt: str, api_key: str, model: str) -> dict:
    """
    Call OpenRouter API to generate personalized cards.
    
    Args:
        prompt: The complete prompt to send to the API
        api_key: OpenRouter API key
        model: Model name to use (e.g., "openai/gpt-5.1")
        
    Returns:
        Parsed JSON response containing cards
        
    Raises:
        Exception: If API call fails
    """
    try:
        print(f"🚀 Calling OpenRouter API with model: {model}")
        
        # Initialize OpenAI client with OpenRouter base URL
        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
        )
        
        # Make API call with JSON response format
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},  # Request JSON output mode
            extra_body={"reasoning": {"enabled": True}}  # Enable reasoning for GPT-5.1
        )
        
        # Extract the content from response
        response_content = response.choices[0].message.content
        
        print("✅ Successfully received response from API")
        
        # Parse the JSON response
        try:
            response_json = json.loads(response_content)
            
            # Validate that we have the expected structure
            if "cards" not in response_json:
                raise ValueError("Response does not contain 'cards' array")
            
            if len(response_json["cards"]) != 4:
                print(f"⚠️  Warning: Expected 4 cards, got {len(response_json['cards'])}")
            
            return response_json
            
        except json.JSONDecodeError:
            # If response is not valid JSON, wrap it
            print("⚠️  Response was not valid JSON")
            raise ValueError("API returned invalid JSON")
            
    except Exception as e:
        raise Exception(f"❌ API call failed: {str(e)}")


def save_cards(cards_data: dict, output_path: str):
    """
    Save the generated cards to a JSON file.
    
    Args:
        cards_data: Dictionary containing the cards
        output_path: Path where to save the cards file
    """
    try:
        # Save JSON with pretty formatting
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cards_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Cards saved to: {output_path}")
        
    except Exception as e:
        raise Exception(f"❌ Failed to save cards: {str(e)}")


def display_cards(cards_data: dict):
    """
    Display the generated cards in a readable format.
    
    Args:
        cards_data: Dictionary containing the cards
    """
    print("=" * 70)
    print("📇 GENERATED CARDS")
    print("=" * 70)
    
    if "cards" in cards_data:
        for i, card in enumerate(cards_data["cards"], 1):
            card_type = card.get("type", "unknown")
            title = card.get("title", "No title")
            body = card.get("body", "No content")
            
            print(f"\n🎴 Card {i}: [{card_type.upper()}]")
            print(f"   Title: {title}")
            print(f"   Body: {body}")
    
    print("\n" + "=" * 70)


def main():
    """
    Main function that orchestrates the card generation process.
    """
    try:
        print("=" * 70)
        print("🎴 CARD GENERATOR - Starting Process")
        print("=" * 70)
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ OPENROUTER_API_KEY not found in environment variables.\n"
                "Please create a .env file with your API key:\n"
                "OPENROUTER_API_KEY=your_key_here"
            )
        
        print("✅ API key loaded from environment")
        print()
        
        # Get the script's directory and construct absolute paths
        script_dir = Path(__file__).parent
        persona_output_path = script_dir / PERSONA_OUTPUT_FILE
        cards_output_path = script_dir / CARDS_OUTPUT_FILE
        
        print(f"📂 Reading persona output from: {persona_output_path}")
        print(f"📝 Cards will be saved to: {cards_output_path}")
        print()
        
        # Step 1: Load persona output JSON
        print("📂 Step 1: Loading persona output data...")
        persona_data = load_json_file(str(persona_output_path))
        print()
        
        # Step 2: Create card generation prompt
        print("📝 Step 2: Creating card generation prompt...")
        prompt = create_card_generation_prompt(persona_data)
        print()
        
        # Step 3: Call OpenRouter API
        print("🌐 Step 3: Calling OpenRouter API to generate cards...")
        cards_data = call_openrouter_api(prompt, api_key, MODEL_NAME)
        print()
        
        # Step 4: Display cards in terminal
        display_cards(cards_data)
        print()
        
        # Step 5: Save cards to file
        print("💾 Step 4: Saving cards to file...")
        save_cards(cards_data, str(cards_output_path))
        print()
        
        print("=" * 70)
        print("✨ Card Generation Complete!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n{str(e)}")
        print("Please ensure the persona output file exists.")
        print("Run 'python3 run_profile_builder.py' first to generate it.")
        exit(1)
        
    except json.JSONDecodeError as e:
        print(f"\n{str(e)}")
        print("Please check that the JSON file is properly formatted.")
        exit(1)
        
    except ValueError as e:
        print(f"\n{str(e)}")
        exit(1)
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

