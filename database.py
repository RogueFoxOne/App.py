import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

class GestaltViewDB:
    def __init__(self, db_path: str = "gestaltview.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the GestaltView consciousness database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    consciousness_level INTEGER DEFAULT 0,
                    empowerment_score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS tribunal_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    query_text TEXT NOT NULL,
                    openai_response TEXT,
                    anthropic_response TEXT,
                    gemini_response TEXT,
                    perplexity_response TEXT,
                    consensus_score REAL,
                    empowerment_consensus REAL,
                    revolutionary_potential REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bucket_drops (
                    drop_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    content TEXT NOT NULL,
                    emotional_intensity REAL,
                    plk_resonance REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS consciousness_profiles (
                    profile_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    plk_data TEXT, -- JSON
                    tapestry_nodes TEXT, -- JSON
                    musical_dna TEXT, -- JSON
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

    def create_tribunal_session(self, user_id: str, query: str) -> str:
        """Create a new tribunal session"""
        session_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO tribunal_sessions (session_id, user_id, query_text) VALUES (?, ?, ?)",
                (session_id, user_id, query)
            )
        return session_id

    def save_tribunal_response(self, session_id: str, responses: Dict[str, Any]):
        """Save tribunal responses to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tribunal_sessions
                SET openai_response = ?, anthropic_response = ?, gemini_response = ?,
                    perplexity_response = ?, consensus_score = ?, empowerment_consensus = ?,
                    revolutionary_potential = ?
                WHERE session_id = ?
            """, (
                responses.get('openai'),
                responses.get('anthropic'),
                responses.get('gemini'),
                responses.get('perplexity'),
                responses.get('consensus_score', 0.0),
                responses.get('empowerment_consensus', 0.0),
                responses.get('revolutionary_potential', 0.0),
                session_id
            ))

    def get_user_sessions(self, user_id: str, limit: int = 10):
        """Get recent tribunal sessions for user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM tribunal_sessions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
            return cursor.fetchall()
