Below is the full raw context data for a user, combining device details, installed apps, usage patterns, SMS, network, battery, location, language, and any other signals.

Analyze this entire block and produce:
	•	User Profile
	•	Meet State
	•	Personalization Strategy

⸻

📥 INPUT DATA START
{CONTEXT_DATA}
📥 INPUT DATA END

YOUR TASK

Based on the input data above (all of it combined), generate:

⸻

1. USER PROFILE

Include:
	•	Summary
	•	Demographics
	•	Lifestyle & routines
	•	Digital comfort & literacy
	•	Language behavior
	•	Financial behavior
	•	Content preferences
	•	Commerce/shopping tendencies
	•	Local interests
	•	Pain points & constraints
	•	Risk signals (low data, low battery, low storage, scams, etc.)
	•	Motivations & aspirations
	•	Recommended tone/style for the assistant

⸻

2. USER MEET STATE (real-time moment)

Interpret the user’s current needs using all contextual signals.
Provide:
	•	Moment assessment (energy level, likely intent)
	•	Immediate needs
	•	Recommended content cards for home screen
	•	Recommended tools/actions (e.g., mandi price check, EMI calculator)
	•	Best opening line for ChatGPT
	•	Any safety alerts / device warnings

⸻

3. PERSONALIZATION STRATEGY

Provide recommendations for:
	•	Daily habit hooks
	•	Weekly needs
	•	Long-term trust building
	•	What to avoid showing
	•	What increases adoption
	•	What overwhelms this user
	•	UX hints (voice, language, simplicity)

⸻

📦 4. OUTPUT FORMAT (STRICT)

Return the final answer in this exact JSON schema:
{
  "user_profile": {
    "summary": "",
    "demographics": {},
    "lifestyle": {},
    "digital_behavior": {},
    "financial_behavior": {},
    "content_preferences": {},
    "risk_signals": {},
    "pain_points": {},
    "motivations": {},
    "recommended_tone": ""
  },

  "meet_state": {
    "moment_assessment": "",
    "immediate_needs": [],
    "recommended_content_cards": [],
    "recommended_tools": [],
    "best_opening_line": "",
    "safety_alerts": []
  },

  "personalization_strategy": {
    "daily_hooks": [],
    "weekly_needs": [],
    "long_term_strategy": [],
    "avoid_showing": [],
    "adoption_drivers": []
  }
}