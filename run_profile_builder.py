#!/usr/bin/env python3
"""
Profile Builder Script
Loads persona JSON data, injects it into a prompt template, 
and calls OpenRouter API (GPT-5.1) to generate a user profile.
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model configuration - change this to use a different model
MODEL_NAME = "openai/gpt-5.1"

# File paths
PERSONA_FILE = "personas/kirana_shop.json"
PROMPT_TEMPLATE_FILE = "prompt/memory_builder.md"
OUTPUT_DIR = "outputs"  # Output directory

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

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


def load_text_file(file_path: str) -> str:
    """
    Load a text file and return its contents.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        File contents as a string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Successfully loaded template from: {file_path}")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {file_path}")


def inject_context_into_template(template: str, context_data: dict) -> str:
    """
    Replace {CONTEXT_DATA} placeholder with pretty-printed JSON.
    
    Args:
        template: Prompt template string with {CONTEXT_DATA} placeholder
        context_data: Dictionary to inject into the template
        
    Returns:
        Template with context data injected
    """
    # Convert dict to pretty JSON string with 2-space indentation
    json_string = json.dumps(context_data, indent=2, ensure_ascii=False)
    
    # Replace the placeholder
    final_prompt = template.replace("{CONTEXT_DATA}", json_string)
    
    print("✅ Successfully injected context data into template")
    return final_prompt


def call_openrouter_api(prompt: str, api_key: str, model: str) -> dict:
    """
    Call OpenRouter API with the given prompt.
    
    Args:
        prompt: The complete prompt to send to the API
        api_key: OpenRouter API key
        model: Model name to use (e.g., "openai/gpt-5.1")
        
    Returns:
        Parsed JSON response from the API
        
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
            return response_json
        except json.JSONDecodeError:
            # If response is not valid JSON, wrap it
            print("⚠️  Response was not valid JSON, wrapping in object")
            return {
                "raw_response": response_content,
                "note": "Response was not valid JSON"
            }
            
    except Exception as e:
        raise Exception(f"❌ API call failed: {str(e)}")


def save_output(data: dict, output_path: str):
    """
    Save the output data to a JSON file.
    Creates the output directory if it doesn't exist.
    
    Args:
        data: Dictionary to save
        output_path: Path where to save the output file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON with pretty formatting
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Output saved to: {output_path}")
        
    except Exception as e:
        raise Exception(f"❌ Failed to save output: {str(e)}")


def main():
    """
    Main function that orchestrates the entire profile building process.
    """
    try:
        print("=" * 70)
        print("🔧 PROFILE BUILDER - Starting Process")
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
        
        # Generate output filename based on persona filename
        # e.g., personas/kirana_shop.json -> outputs/kirana_shop_output.json
        persona_basename = Path(PERSONA_FILE).stem  # Gets 'kirana_shop' from 'kirana_shop.json'
        output_filename = f"{persona_basename}_output.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"📝 Output will be saved to: {output_path}")
        print()
        
        # Step 1: Load persona JSON
        print("📂 Step 1: Loading persona data...")
        persona_data = load_json_file(PERSONA_FILE)
        print()
        
        # Step 2: Load prompt template
        print("📄 Step 2: Loading prompt template...")
        prompt_template = load_text_file(PROMPT_TEMPLATE_FILE)
        print()
        
        # Step 3: Inject context data into template
        print("💉 Step 3: Injecting context data into template...")
        final_prompt = inject_context_into_template(prompt_template, persona_data)
        print()
        
        # Step 4: Call OpenRouter API
        print("🌐 Step 4: Calling OpenRouter API...")
        response_data = call_openrouter_api(final_prompt, api_key, MODEL_NAME)
        print()
        
        # Step 5: Print response to terminal
        print("=" * 70)
        print("📤 API RESPONSE")
        print("=" * 70)
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
        print()
        
        # Step 6: Save output to file
        print("💾 Step 6: Saving output to file...")
        save_output(response_data, output_path)
        print()
        
        print("=" * 70)
        print("✨ Profile Builder - Process Complete!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n{str(e)}")
        print("Please ensure all required files exist.")
        exit(1)
        
    except json.JSONDecodeError as e:
        print(f"\n{str(e)}")
        print("Please check that your JSON file is properly formatted.")
        exit(1)
        
    except ValueError as e:
        print(f"\n{str(e)}")
        exit(1)
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

