# AI-Powered User Profile & Personalized Cards System

A complete pipeline that transforms user persona data into intelligent, personalized content cards using GPT-5.1 via OpenRouter.

## 📋 System Overview

This project creates personalized content cards for users based on their device, behavior, and context data. It uses AI to generate deep user insights and then creates actionable, relevant cards in the user's native language (Hindi).

## 🔄 Data Flow

```
personas/kirana_shop.json
    ↓
    (Injected into prompt template)
    ↓
prompt/memory_builder.md
    ↓
    (Sent to OpenRouter GPT-5.1 API)
    ↓
outputs/kirana_shop_output.json
    ↓
    (Used to generate personalized cards)
    ↓
frontend/cards/cards_output.json
    ↓
    (Displayed in web app)
    ↓
web-app/index.html
```

## 📁 Project Structure

```
.
├── personas/
│   └── kirana_shop.json          # Raw user persona data (device, apps, behavior)
├── prompt/
│   └── memory_builder.md          # LLM prompt template with {CONTEXT_DATA} placeholder
├── outputs/
│   └── kirana_shop_output.json   # AI-generated user profile & meet state
├── frontend/cards/
│   ├── generate_cards.py          # Script to generate personalized cards
│   └── cards_output.json          # Final personalized cards (type, title, body)
├── web-app/
│   └── index.html                 # Interactive web app to display cards
├── run_profile_builder.py         # Main script: persona → LLM → profile
└── requirements.txt               # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/srrm99/ai-fools.git
   cd ai-fools
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the root directory:
   ```bash
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## 📝 Usage

### Step 1: Generate User Profile

Takes the persona data and generates a comprehensive user profile with AI insights.

```bash
python3 run_profile_builder.py
```

**What it does:**
- Reads `personas/kirana_shop.json`
- Injects the data into `prompt/memory_builder.md` template
- Sends the prompt to OpenRouter GPT-5.1 API
- Saves the AI-generated profile to `outputs/kirana_shop_output.json`

**Output includes:**
- User Profile (demographics, behavior, preferences)
- Meet State (immediate needs, moment assessment)
- Personalization Strategy (daily hooks, long-term strategy)

### Step 2: Generate Personalized Cards

Creates specific, actionable content cards based on the user profile.

```bash
cd frontend/cards
python3 generate_cards.py
```

**What it does:**
- Reads `outputs/kirana_shop_output.json`
- Sends user profile to GPT-5.1 with card generation prompt
- Creates 4 personalized cards (money, kids, govt, phone)
- Saves cards to `frontend/cards/cards_output.json`

**Card Structure:**
```json
{
  "cards": [
    {
      "type": "money",
      "title": "दुकान का रोज़ हिसाब",
      "body": "आज दुकान बंद करते समय 5 मिनट में गिन लें..."
    }
  ]
}
```

### Step 3: View Cards in Web App

Open the interactive web interface to see and interact with the cards.

```bash
open web-app/index.html
```

**Features:**
- Swipeable card interface (like Tinder)
- Clean white design with Poppins font
- Mobile-responsive
- Hindi text support
- Swipe right to like, left to dislike

## 🎯 Example Use Case: Kirana Shop Owner

The included example (`personas/kirana_shop.json`) represents:

**Profile:** Hindi-speaking kirana shop owner in Vidisha, Madhya Pradesh
- **Device:** Low-end Android (Redmi A2, 2GB RAM, 3GB free storage)
- **Network:** Jio 4G with weak signal
- **Apps:** WhatsApp, PhonePe, Khatabook, JioMart Partner
- **Language:** Hindi (hi-IN)
- **Needs:** Money management, kids education, govt schemes, data saving

**Generated Cards:**
1. 💰 **Money Card**: Daily shop accounting tips
2. 👨‍👩‍👧 **Kids Card**: Homework tracking advice
3. 🏛 **Govt Card**: Ayushman Bharat scheme info
4. 📱 **Phone Card**: Storage and data saving tips

## 🔑 API Configuration

This project uses **OpenRouter** to access OpenAI's GPT-5.1 model.

### Why OpenRouter?
- Single API for multiple AI models
- Pay-as-you-go pricing
- No monthly subscriptions
- Access to latest models (GPT-5.1)

### Cost Estimate
- Profile generation: ~$0.02-0.05 per run
- Card generation: ~$0.01-0.03 per run
- Total per complete flow: ~$0.05-0.08

## 🛠 Customization

### Create Your Own Persona

1. Copy `personas/kirana_shop.json` to a new file
2. Modify the data (device, location, apps, behavior)
3. Update `PERSONA_FILE` in `run_profile_builder.py`
4. Run the pipeline

### Modify Card Types

Edit `frontend/cards/generate_cards.py` to change:
- Number of cards
- Card types (money, kids, govt, phone, shop, etc.)
- Language and tone
- Card content structure

### Customize Prompt

Edit `prompt/memory_builder.md` to adjust:
- Analysis depth
- Output structure
- Personalization strategy
- Tone and style guidelines

## 📊 Output Examples

### User Profile Output
```json
{
  "user_profile": {
    "summary": "Hindi-speaking kirana shop owner...",
    "demographics": { ... },
    "digital_behavior": { ... }
  },
  "meet_state": {
    "moment_assessment": "User is on low-end phone...",
    "immediate_needs": [ ... ]
  }
}
```

### Cards Output
```json
{
  "cards": [
    {
      "type": "money",
      "title": "दुकान का रोज़ हिसाब",
      "body": "आज दुकान बंद करते समय..."
    }
  ]
}
```

## 🌐 Web App Features

- **Swipeable Interface**: Drag cards left (dislike) or right (like)
- **Responsive Design**: Works on desktop and mobile
- **Smooth Animations**: Cards rotate and scale during swipe
- **Clean Typography**: Poppins font with light weights
- **Hindi Support**: Full support for Devanagari script
- **Infinite Loop**: Cards cycle continuously

## 🔒 Privacy & Security

- **No data collection**: All processing happens locally
- **API key security**: Stored in `.env` file (not committed to git)
- **User privacy**: Persona data is synthetic for demonstration
- **Open source**: Full transparency of data flow

## 📦 Dependencies

- `openai>=1.0.0` - OpenAI SDK (compatible with OpenRouter)
- `python-dotenv>=1.0.0` - Environment variable management

## 🤝 Contributing

Feel free to:
- Add new persona templates
- Create card type variants
- Improve the web UI
- Add multi-language support
- Optimize prompts

## 📄 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Credits

- **OpenRouter** for AI API access
- **OpenAI GPT-5.1** for intelligent profile generation
- **Poppins Font** by Indian Type Foundry

## 📧 Contact

For questions or suggestions, open an issue on GitHub.

---

**Made with ❤️ for personalized user experiences**

