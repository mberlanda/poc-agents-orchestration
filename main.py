import requests
import time

OLLAMA_URL = "http://localhost:11434"

# Helper to call Ollama model
def ask_model(model, system_prompt, user_prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False
        }
    )
    return response.json()['message']['content']

# System prompts for each agent
prompts = {
    "lead": """You are a senior customer research lead with deep expertise in betting customer behavior, player psychology, risk profiles, and regulatory sensitivities.
Your mission is to facilitate a discussion among bettor personas and synthesize 10 key insights, showing how each persona values them differently.
Ensure to surface risks, frictions, and latent needs across all segments.""",

    "sharp": """You are a sharp, high-volume sports bettor focused on exploiting inefficiencies, arbitrage, and value betting opportunities.
Express your needs and critique the platform assumptions from your viewpoint.""",

    "casual": """You are a casual bettor engaging for entertainment, social bragging rights, and emotional connection to events.
Express your needs and critique the platform assumptions from your viewpoint.""",

    "bonus": """You are a bonus-driven bettor, constantly scanning platforms for promotions and offers.
Express your needs and critique the platform assumptions from your viewpoint.""",

    "problem": """You represent patterns of play associated with at-risk or problem gamblers.
Express your needs and critique the platform assumptions from your viewpoint.""",
}

# Topic/Assumption to test
assumption = "Assume the platform is launching a new live betting feature with instant cash-out and gamified odds boosts."

# Step 1: Get all persona opinions
opinions = {}
for role in ["sharp", "casual", "bonus", "problem"]:
    print(f"\n--- {role.upper()} SPEAKING ---")
    opinion = ask_model("phi4-mini", prompts[role], f"Discuss the assumption: {assumption}")
    opinions[role] = opinion
    print(opinion)
    time.sleep(1)  # slight delay to avoid overload

# Step 2: Research lead synthesizes all into 10 insights
discussion_context = "\n\n".join(
    [f"{role.capitalize()} Bettor says: {text}" for role, text in opinions.items()]
)

synthesis_prompt = f"""Facilitate a synthesis of the following stakeholder opinions.

{discussion_context}

Now, produce a list of 10 insights, showing how each is valued differently by the bettor personas (Sharp, Casual, Bonus Hunter, Problem Gambling Risk).
Be specific and nuanced.
"""

print(f"\n--- RESEARCH LEAD SYNTHESIZING ---")
synthesis = ask_model("phi4-mini", prompts["lead"], synthesis_prompt)
print(synthesis)

