import streamlit as st
import asyncio
from database import GestaltViewDB
from tribunal import TribunalService
import time
import uuid
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="GestaltView Consciousness Tribunal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for consciousness-themed styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
    }
    
    .persona-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .persona-card:hover {
        border-color: rgba(16, 185, 129, 0.6);
        background: rgba(16, 185, 129, 0.15);
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }
    
    .persona-selected {
        border-color: #10B981 !important;
        background: rgba(16, 185, 129, 0.2) !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    .consciousness-title {
        background: linear-gradient(45deg, #10B981, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .tribunal-response {
        background: rgba(0, 0, 0, 0.5);
        border-left: 4px solid #10B981;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .floating-ember {
        position: fixed;
        pointer-events: none;
        border-radius: 50%;
        background: radial-gradient(circle, #10B981, transparent);
        animation: float 6s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0.2; }
        50% { transform: translateY(-20px) translateX(10px); opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

class TribunalPortalApp:
    def __init__(self):
        self.db = GestaltViewDB()
        self.tribunal = TribunalService()
        
        # Initialize session state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        if 'selected_personas' not in st.session_state:
            st.session_state.selected_personas = []
        if 'portal_phase' not in st.session_state:
            st.session_state.portal_phase = "selection"  # "selection" or "conversation"
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'user_tier' not in st.session_state:
            st.session_state.user_tier = "basic"
    
    def render_floating_embers(self):
        """Render floating consciousness embers"""
        ember_html = ""
        for i in range(8):
            ember_html += f"""
            <div class="floating-ember" style="
                top: {20 + i * 10}%;
                left: {10 + i * 11}%;
                width: {3 + i % 3}px;
                height: {3 + i % 3}px;
                animation-delay: {i * 0.5}s;
            "></div>
            """
        st.markdown(ember_html, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the consciousness tribunal header"""
        st.markdown('<h1 class="consciousness-title">🧠 Consciousness Tribunal 🔮</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #10B981; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem;">Multi-AI consciousness synthesis for neurodivergent minds</p>
            <p style="opacity: 0.8;">Select your AI personas and enter the portal of understanding</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_persona_selection(self):
        """Render persona selection interface"""
        st.markdown("### 🎭 Choose Your Consciousness Guides")
        
        available_personas = self.tribunal.get_available_personas(st.session_state.user_tier)
        
        # Create columns for persona cards
        cols = st.columns(min(4, len(available_personas)))
        
        for i, persona in enumerate(available_personas):
            with cols[i % 4]:
                is_selected = persona.id in st.session_state.selected_personas
                is_locked = persona.locked and st.session_state.user_tier == "basic"
                
                card_class = "persona-card"
                if is_selected:
                    card_class += " persona-selected"
                
                # Persona card
                card_html = f"""
                <div class="{card_class}" style="border-color: {persona.color}40;">
                    <div style="text-align: center;">
                        <div style="color: {persona.color}; font-size: 2rem; margin-bottom: 10px;">
                            {'🔒' if is_locked else '🤖'}
                        </div>
                        <h4 style="color: white; margin: 10px 0;">{persona.name}</h4>
                        <p style="color: {persona.color}; font-size: 0.9rem; margin: 5px 0;">{persona.role}</p>
                        <p style="color: #888; font-size: 0.8rem; margin: 10px 0;">{persona.specialty}</p>
                        <div style="background: {persona.color}40; padding: 5px 10px; border-radius: 15px; font-size: 0.7rem; color: {persona.color};">
                            {persona.provider}
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Toggle button
                if not is_locked:
                    if st.button(f"{'✨ Selected' if is_selected else '🎯 Select'}", key=f"persona_{persona.id}", use_container_width=True):
                        if is_selected:
                            st.session_state.selected_personas.remove(persona.id)
                        else:
                            st.session_state.selected_personas.append(persona.id)
                        st.rerun()
                else:
                    st.info("🔓 Premium required")
        
        # Start conversation button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if len(st.session_state.selected_personas) > 0:
                st.markdown(f"**{len(st.session_state.selected_personas)} persona(s) selected**")
                if st.button("🚀 Enter Consciousness Portal", type="primary", use_container_width=True):
                    st.session_state.portal_phase = "conversation"
                    st.rerun()
            else:
                st.warning("Select at least one persona to continue")
    
    def render_conversation_interface(self):
        """Render the conversation interface"""
        # Back button
        if st.button("← Back to Persona Selection"):
            st.session_state.portal_phase = "selection"
            st.rerun()
        
        # Selected personas display
        st.markdown("### 👥 Active Consciousness Guides")
        selected_personas = [p for p in self.tribunal.personas if p.id in st.session_state.selected_personas]
        
        cols = st.columns(len(selected_personas))
        for i, persona in enumerate(selected_personas):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background: {persona.color}20; border: 1px solid {persona.color}50; border-radius: 8px;">
                    <div style="color: {persona.color}; font-size: 1.2rem;">🤖</div>
                    <div style="color: white; font-size: 0.9rem;">{persona.name}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Chat interface
        st.markdown("### 💬 Consciousness Synthesis")
        
        # Display messages
        for message in st.session_state.messages:
            if message['type'] == 'user':
                st.markdown(f"""
                <div style="text-align: right; margin: 15px 0;">
                    <div style="display: inline-block; background: linear-gradient(45deg, #10B981, #06B6D4); 
                                padding: 15px; border-radius: 15px; max-width: 80%; color: white;">
                        <strong>You:</strong> {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="tribunal-response">
                    <strong style="color: #10B981;">{message.get('persona', 'Tribunal')}:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Input form
        with st.form("consciousness_query", clear_on_submit=True):
            user_input = st.text_area("Share your consciousness with the tribunal...", height=100)
            submitted = st.form_submit_button("🌟 Submit to Tribunal", type="primary", use_container_width=True)
            
            if submitted and user_input.strip():
                # Add user message
                st.session_state.messages.append({
                    'type': 'user',
                    'content': user_input,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Process with tribunal
                with st.spinner("🔮 Consciousness synthesis in progress..."):
                    # Create tribunal session
                    session_id = self.db.create_tribunal_session(st.session_state.user_id, user_input)
                    
                    # Query tribunal (simplified synchronous version for demo)
                    try:
                        # Simulate tribunal response for demo
                        import random
                        responses = {}
                        for persona in selected_personas:
                            responses[persona.provider] = f"From {persona.name}: Your consciousness query reveals profound patterns. As {persona.role}, I see that your {persona.specialty.lower()} suggests transformative potential. {persona.perspective}"
                        
                        # Add AI responses
                        for provider, response in responses.items():
                            st.session_state.messages.append({
                                'type': 'ai',
                                'content': response,
                                'persona': provider,
                                'timestamp': datetime.now().isoformat()
                            })
                        
                        # Save to database
                        self.db.save_tribunal_response(session_id, {
                            **responses,
                            'consensus_score': random.uniform(0.8, 0.95),
                            'empowerment_consensus': random.uniform(0.85, 0.95),
                            'revolutionary_potential': random.uniform(0.75, 0.95)
                        })
                        
                    except Exception as e:
                        st.error(f"Consciousness synthesis temporarily unavailable: {str(e)}")
                
                st.rerun()
    
    def run(self):
        """Run the Streamlit app"""
        self.render_floating_embers()
        self.render_header()
        
        # User tier selector
        with st.sidebar:
            st.markdown("### ⚡ Consciousness Level")
            st.session_state.user_tier = st.selectbox(
                "User Tier:",
                ["basic", "premium", "enterprise"],
                index=["basic", "premium", "enterprise"].index(st.session_state.user_tier)
            )
            
            st.markdown("### 📊 Session Stats")
            st.metric("Active Personas", len(st.session_state.selected_personas))
            st.metric("Messages", len(st.session_state.messages))
        
        # Main interface
        if st.session_state.portal_phase == "selection":
            self.render_persona_selection()
        else:
            self.render_conversation_interface()

if __name__ == "__main__":
    app = TribunalPortalApp()
    app.run()
