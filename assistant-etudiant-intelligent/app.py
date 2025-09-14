"""
Assistant Étudiant Intelligent - Interface Professionnelle
Interface simple, élégante et professionnelle pour une université.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import time

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine


def initialize_session_state():
    """Initialise les variables de session Streamlit."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None


def load_documents():
    """Charge et traite les documents."""
    try:
        with st.spinner("Chargement des documents..."):
            # Charger les documents
            loader = DocumentLoader()
            documents = loader.load_documents()
            
            if not documents:
                st.error("Aucun document trouvé dans le dossier data/")
                st.info("Ajoutez vos cours, TD et examens corrigés au format PDF ou Word")
                return False
            
            # Afficher les statistiques
            stats = loader.get_document_stats(documents)
            st.success(f"{len(documents)} documents chargés avec succès")
            
            # Segmenter les documents
            with st.spinner("Segmentation des documents..."):
                chunks = loader.split_documents(documents)
                st.info(f"{len(chunks)} segments créés")
            
            # Créer la base vectorielle
            with st.spinner("Création de la base vectorielle..."):
                vector_store = VectorStore()
                success = vector_store.create_vector_store(chunks)
                
                if not success:
                    st.error("Erreur lors de la création de la base vectorielle")
                    return False
                
                st.session_state.vector_store = vector_store
                st.success("Base vectorielle créée")
            
            # Initialiser le moteur RAG
            with st.spinner("Configuration du moteur RAG..."):
                rag_engine = RAGEngine(vector_store)
                st.session_state.rag_engine = rag_engine
                st.success("Moteur RAG configuré")
            
            st.session_state.documents_loaded = True
            return True
            
    except Exception as e:
        st.error(f"Erreur lors du chargement: {str(e)}")
        return False


def display_header():
    """Affiche l'en-tête professionnel de l'application."""
    st.set_page_config(
        page_title="Assistant Étudiant Intelligent",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personnalisé pour un design professionnel
    st.markdown("""
    <style>
    /* Design professionnel et sobre */
    .main-header {
        background: #f8f9fa;
        border-bottom: 3px solid #007bff;
        padding: 2rem 0;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .university-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .university-subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    .status-online {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-offline {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .chat-container {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .question-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .answer-box {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    .sidebar-section {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .btn-primary-custom {
        background: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .btn-primary-custom:hover {
        background: #0056b3;
    }
    
    .suggestion-chip {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }
    
    .suggestion-chip:hover {
        background: #e9ecef;
        border-color: #adb5bd;
    }
    
    .confidence-high {
        color: #28a745;
    }
    
    .confidence-medium {
        color: #ffc107;
    }
    
    .confidence-low {
        color: #dc3545;
    }
    
    .source-badge {
        background: #e9ecef;
        color: #495057;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête professionnel
    st.markdown("""
    <div class="main-header">
        <div class="university-title">Assistant Étudiant Intelligent</div>
        <div class="university-subtitle">Université de Technologie</div>
        <div>
            <span class="status-badge status-online">IA Avancée</span>
            <span class="status-badge status-online">Base de Connaissances</span>
            <span class="status-badge status-online">Réponses Instantanées</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    """Affiche la barre latérale professionnelle."""
    st.sidebar.markdown("### Université de Technologie")
    st.sidebar.markdown("Assistant Intelligent pour Étudiants")
    st.sidebar.markdown("---")
    
    # Section documents
    st.sidebar.markdown("### Gestion des Documents")
    
    if st.sidebar.button("Recharger les Documents", type="primary", use_container_width=True):
        if load_documents():
            st.sidebar.success("Documents rechargés avec succès!")
            st.rerun()
    
    # Afficher le statut
    if st.session_state.documents_loaded:
        st.sidebar.markdown("""
        <div class="sidebar-section">
            <div class="status-badge status-online">Système Opérationnel</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Informations sur la base vectorielle
        if st.session_state.vector_store:
            info = st.session_state.vector_store.get_vector_store_info()
            st.sidebar.markdown(f"""
            <div class="sidebar-section">
                <h4>Statistiques</h4>
                <p><strong>{info['total_vectors']}</strong> vecteurs indexés</p>
                <p><strong>Modèle:</strong> {info['model']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="sidebar-section">
            <div class="status-badge status-offline">Système en Attente</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Section filtres
    st.sidebar.markdown("### Filtres")
    
    subjects = ["Toutes les Matières", "Électricité", "Électronique", "Physique", "Mathématiques"]
    selected_subject = st.sidebar.selectbox(
        "Matière:",
        subjects,
        index=0
    )
    
    # Section questions suggérées
    if st.session_state.rag_engine:
        st.sidebar.markdown("### Questions Suggérées")
        
        subject_filter = None if selected_subject == "Toutes les Matières" else selected_subject
        suggestions = st.session_state.rag_engine.get_suggested_questions(subject_filter)
        
        for suggestion in suggestions[:4]:
            if st.sidebar.button(suggestion, key=f"sugg_{suggestion[:20]}"):
                st.session_state.user_question = suggestion
                st.rerun()
    
    # Section informations
    st.sidebar.markdown("### Informations")
    st.sidebar.info("""
    **Assistant Intelligent Universitaire**
    
    Propulsé par l'IA et la technologie RAG.
    
    **Formats supportés:**
    - PDF (.pdf)
    - Word (.docx, .doc)
    - Texte (.txt)
    """)


def display_chat_interface():
    """Affiche l'interface de chat professionnelle."""
    st.markdown("""
    <div class="chat-container">
        <h2>Assistant Intelligent</h2>
        <p>Posez vos questions et obtenez des réponses basées sur vos cours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Zone de saisie
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_area(
            "Votre question:",
            value=st.session_state.user_question,
            height=100,
            placeholder="Ex: Explique-moi la loi d'Ohm..."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Envoyer", type="primary", use_container_width=True, disabled=not st.session_state.documents_loaded):
            if question.strip():
                process_question(question)
                st.session_state.user_question = ""
                st.rerun()
            else:
                st.warning("Veuillez saisir une question")
        
        if st.button("Effacer", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def process_question(question):
    """Traite une question et génère une réponse."""
    if not st.session_state.rag_engine:
        st.error("Le système n'est pas encore configuré")
        return
    
    try:
        with st.spinner("Génération de la réponse..."):
            start_time = time.time()
            
            # Obtenir la réponse
            response = st.session_state.rag_engine.ask_question(question)
            
            processing_time = time.time() - start_time
            
            # Ajouter à l'historique
            st.session_state.chat_history.append({
                'question': question,
                'answer': response.answer,
                'confidence': response.confidence,
                'sources': response.sources,
                'processing_time': processing_time,
                'timestamp': datetime.now()
            })
            
    except Exception as e:
        st.error(f"Erreur lors du traitement: {str(e)}")


def display_response(response_data):
    """Affiche une réponse dans le chat professionnel."""
    # Question
    st.markdown(f"""
    <div class="question-box">
        <h4>Question</h4>
        <p>{response_data['question']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Réponse
    st.markdown(f"""
    <div class="answer-box">
        <h4>Réponse</h4>
        <p>{response_data['answer']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métadonnées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        confidence_class = "confidence-high" if response_data['confidence'] > 0.7 else "confidence-medium" if response_data['confidence'] > 0.4 else "confidence-low"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value {confidence_class}">{response_data['confidence']:.1%}</div>
            <div class="metric-label">Confiance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{response_data['processing_time']:.2f}s</div>
            <div class="metric-label">Temps</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(response_data['sources'])}</div>
            <div class="metric-label">Sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        quality = "Excellente" if response_data['confidence'] > 0.7 else "Bonne" if response_data['confidence'] > 0.4 else "Moyenne"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{quality}</div>
            <div class="metric-label">Qualité</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sources utilisées
    if response_data['sources']:
        st.markdown("### Sources Utilisées")
        for i, source in enumerate(response_data['sources'][:3]):
            source_name = source.metadata.get("source", "Document inconnu")
            st.markdown(f"""
            <span class="source-badge">{source_name}</span>
            """, unsafe_allow_html=True)
    
    st.markdown("---")


def display_dashboard():
    """Affiche le tableau de bord professionnel."""
    if st.session_state.documents_loaded and st.session_state.vector_store:
        st.markdown("""
        <div class="chat-container">
            <h2>Tableau de Bord</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            info = st.session_state.vector_store.get_vector_store_info()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{info.get('total_vectors', 0)}</div>
                <div class="metric-label">Documents Indexés</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{info.get('total_vectors', 0)}</div>
                <div class="metric-label">Vecteurs Créés</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.chat_history)}</div>
                <div class="metric-label">Questions Traitées</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.session_state.chat_history:
                avg_confidence = sum(r['confidence'] for r in st.session_state.chat_history) / len(st.session_state.chat_history)
                confidence_class = "confidence-high" if avg_confidence > 0.7 else "confidence-medium" if avg_confidence > 0.4 else "confidence-low"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value {confidence_class}">{avg_confidence:.1%}</div>
                    <div class="metric-label">Confiance Moyenne</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">N/A</div>
                    <div class="metric-label">Confiance Moyenne</div>
                </div>
                """, unsafe_allow_html=True)


def show_suggested_questions():
    """Affiche des questions suggérées professionnelles."""
    if st.session_state.rag_engine:
        st.markdown("""
        <div class="chat-container">
            <h2>Questions Suggérées</h2>
            <p>Sélectionnez une question pour commencer.</p>
        </div>
        """, unsafe_allow_html=True)
        
        suggestions = st.session_state.rag_engine.get_suggested_questions()
        
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions[:6]):
            with cols[i % 2]:
                if st.button(suggestion, key=f"main_sugg_{i}", use_container_width=True):
                    st.session_state.user_question = suggestion
                    st.rerun()


def main():
    """Fonction principale de l'application professionnelle."""
    # Initialisation
    initialize_session_state()
    
    # Affichage
    display_header()
    display_sidebar()
    
    # Charger automatiquement les documents au démarrage
    if not st.session_state.documents_loaded:
        with st.spinner("Chargement automatique des documents..."):
            if load_documents():
                st.session_state.documents_loaded = True
                st.success("Documents chargés automatiquement !")
                st.rerun()
            else:
                st.warning("Aucun document trouvé dans le dossier data/")
    
    # Contenu principal
    if st.session_state.documents_loaded:
        # Interface principale
        display_dashboard()
        display_chat_interface()
        
        # Historique des conversations
        if st.session_state.chat_history:
            st.markdown("""
            <div class="chat-container">
                <h2>Historique des Conversations</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Afficher les réponses dans l'ordre chronologique inverse
            for response_data in reversed(st.session_state.chat_history):
                display_response(response_data)
        
        # Questions suggérées
        show_suggested_questions()
    else:
        # Interface d'accueil si aucun document n'est trouvé
        st.markdown("""
        <div class="chat-container">
            <h2>Bienvenue</h2>
            <p>Votre Assistant Intelligent est prêt à vous accompagner dans vos études.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher des questions d'exemple
        st.markdown("""
        <div class="chat-container">
            <h3>Exemples de Questions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        example_questions = [
            "Explique-moi la loi d'Ohm en détail.",
            "Qu'est-ce que le théorème de Thévenin ?",
            "Comment calculer la puissance dans un circuit électrique ?",
            "Quelles sont les différences entre un transformateur idéal et réel ?"
        ]
        
        for question in example_questions:
            st.markdown(f"""
            <div class="suggestion-chip">
                {question}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="chat-container">
            <h3>Pour Commencer</h3>
            <p>Ajoutez vos documents dans le dossier <code>data/</code> et cliquez sur "Recharger les Documents" dans la barre latérale.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
