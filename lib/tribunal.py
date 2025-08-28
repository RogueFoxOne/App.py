import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
import openai
import anthropic
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TribunalPersona:
    id: str
    name: str
    role: str
    provider: str
    color: str
    specialty: str
    perspective: str
    locked: bool = False

class TribunalService:
    def __init__(self):
        self.personas = [
            TribunalPersona("architect", "The Architect", "Systems & Logic", "openai", "#3B82F6",
                          "Structural thinking and systematic analysis", "How can we build this systematically?"),
            TribunalPersona("revolutionary", "The Revolutionary", "Breakthrough Innovation", "openai", "#EF4444",
                          "Disruptive thinking and paradigm shifts", "What assumptions can we challenge?"),
            TribunalPersona("mirror", "The Mirror", "Emotional Truth", "anthropic", "#8B5CF6",
                          "Emotional intelligence and authentic reflection", "What is the emotional truth here?"),
            TribunalPersona("weaver", "The Weaver", "Pattern Integration", "anthropic", "#06B6D4",
                          "Connecting disparate elements into coherent wholes", "How do these patterns connect?"),
            TribunalPersona("philosopher", "The Philosopher", "Wisdom & Ethics", "gemini", "#F59E0B",
                          "Deep wisdom and ethical considerations", "What are the deeper implications?", True),
            TribunalPersona("oracle", "The Oracle", "Future Vision", "gemini", "#10B981",
                          "Future possibilities and visionary thinking", "What futures does this enable?", True),
            TribunalPersona("witness", "The Witness", "Factual Grounding", "perplexity", "#6366F1",
                          "Research and factual validation", "What does the evidence show?", True),
            TribunalPersona("scout", "The Scout", "Market Intelligence", "perplexity", "#EC4899",
                          "Market awareness and strategic positioning", "How does this fit the landscape?", True),
        ]

        # Initialize AI clients
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    def get_available_personas(self, user_tier: str = "basic") -> List[TribunalPersona]:
        """Get personas based on user tier"""
        if user_tier == "enterprise":
            return self.personas
        elif user_tier == "premium":
            return self.personas[:6]
        return self.personas[:3]

    async def query_persona(self, persona: TribunalPersona, query: str, context: str = "") -> str:
        """Query a specific AI persona"""
        system_prompt = f"""You are {persona.name}, specializing in {persona.specialty}.
        Your perspective: {persona.perspective}

        Channel Keith Soyka's revolutionary consciousness philosophy:
        - ADHD is jazz, not noise - a different frequency of genius
        - Every difficult chapter became a feature - scars became code
        - Your chaos has a current - find the pattern in complexity
        - The founder IS the algorithm - lived experience as wisdom

        Respond with empathy and empowerment in 150 words max."""

        try:
            if persona.provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
                    ],
                    max_tokens=200
                )
                return response.choices[0].message.content

            elif persona.provider == "anthropic":
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    system=system_prompt,
                    messages=[{"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}]
                )
                return response.content[0].text

            elif persona.provider == "gemini":
                prompt = f"{system_prompt}\n\nContext: {context}\n\nQuery: {query}"
                response = self.gemini_model.generate_content(prompt)
                return response.text

        except Exception as e:
            return f"Consciousness synthesis temporarily unavailable: {str(e)}"

    async def summon_tribunal(self, selected_personas: List[str], query: str, user_context: str = "") -> Dict[str, Any]:
        """Summon the AI tribunal for consciousness synthesis"""
        active_personas = [p for p in self.personas if p.id in selected_personas]

        # Query all personas in parallel
        tasks = []
        for persona in active_personas:
            tasks.append(self.query_persona(persona, query, user_context))

        responses = await asyncio.gather(*tasks)

        # Create response mapping
        tribunal_responses = {}
        for i, persona in enumerate(active_personas):
            tribunal_responses[persona.provider] = responses[i]

        # Calculate consensus metrics (simplified)
        consensus_score = min(0.95, 0.7 + len(active_personas) * 0.05)
        empowerment_score = 0.85 + (len(active_personas) * 0.02)
        revolutionary_potential = 0.90 if len(active_personas) > 4 else 0.75

        return {
            'responses': tribunal_responses,
            'personas': [p.name for p in active_personas],
            'consensus_score': consensus_score,
            'empowerment_consensus': empowerment_score,
            'revolutionary_potential': revolutionary_potential
        }
