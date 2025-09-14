# 🎓 Assistant Étudiant Intelligent

Un assistant intelligent basé sur RAG (Retrieval-Augmented Generation) pour aider les étudiants à naviguer dans leurs cours, TD et examens corrigés.

## 🎯 Problématique

Les étudiants passent beaucoup de temps à chercher des informations dans leurs documents de cours, et posent souvent les mêmes questions aux professeurs. Cet assistant résout ces problèmes en :

- **Réduisant le temps de recherche** dans les documents
- **Fournissant des réponses fiables** basées sur les cours réels
- **Améliorant l'autonomie** des étudiants
- **Réduisant la charge** des professeurs

## 🏗️ Solution RAG

### Architecture
```
Documents PDF/Word → Chargement → Segmentation → Vectorisation → Base FAISS → Recherche → Génération de réponse
```

### Composants
1. **Document Loader** : Chargement automatique des PDF et Word
2. **Vector Store** : Base vectorielle FAISS pour la recherche rapide
3. **RAG Engine** : Moteur de génération de réponses
4. **Interface Streamlit** : Interface utilisateur moderne

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation rapide
```bash
# 1. Cloner le projet
git clone [url-du-projet]
cd assistant-etudiant-intelligent

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

### Installation automatique (Windows)
```bash
# Double-cliquer sur install.bat
# ou
install.bat
```

## 📁 Structure du projet

```
📁 assistant-etudiant-intelligent/
├── 📁 data/                    # Documents PDF/Doc à analyser
├── 📁 src/                     # Code source
│   ├── 📄 document_loader.py   # Chargement des documents
│   ├── 📄 vector_store.py      # Gestion de la base vectorielle
│   ├── 📄 rag_engine.py        # Moteur RAG principal
│   └── 📄 chatbot.py           # Interface utilisateur
├── 📁 requirements.txt         # Dépendances Python
├── 📄 app.py                   # Application Streamlit
└── 📄 README.md               # Ce fichier
```

## 🎬 Utilisation

### 1. Ajouter des documents
Placez vos documents dans le dossier `data/` :
- PDF (.pdf)
- Word (.docx, .doc)
- Texte (.txt)

### 2. Lancer l'application
```bash
streamlit run app.py
```

### 3. Charger les documents
Cliquez sur "🔄 Charger les documents" dans la barre latérale.

### 4. Poser des questions
Exemples de questions :
- "Explique-moi la loi d'Ohm."
- "Qu'est-ce que le théorème de Thévenin ?"
- "Comment calculer la puissance dans un circuit électrique ?"

## 🛠️ Technologies

### Stack technique
- **LangChain** : Framework RAG complet
- **FAISS** : Base de données vectorielle haute performance
- **Streamlit** : Interface utilisateur moderne
- **HuggingFace** : Modèles d'embeddings et LLM
- **PyPDF2** : Traitement des documents PDF
- **Python-docx** : Traitement des documents Word

### Modèles IA
- **Embeddings** : `sentence-transformers/all-MiniLM-L6-v2`
- **LLM** : HuggingFace Hub (flan-t5-base) ou OpenAI
- **Vectorisation** : FAISS pour la recherche rapide

## 📊 Fonctionnalités

### ✅ Fonctionnalités principales
- **Chargement automatique** des documents PDF/Word
- **Recherche vectorielle** rapide et précise
- **Génération de réponses** basées sur les documents
- **Interface utilisateur** moderne avec Streamlit
- **Filtrage par matière** (Électricité, Électronique, etc.)
- **Score de confiance** pour chaque réponse
- **Historique des conversations**
- **Questions suggérées**

### ✅ Fonctionnalités avancées
- **Gestion d'erreurs** robuste
- **Métadonnées** automatiques (source, matière, type)
- **Sauvegarde** de la base vectorielle
- **Statistiques** des documents
- **Design responsive** et moderne

## 🎯 Avantages

### Avantages techniques
- **Fiabilité** : Réponses basées sur les documents réels
- **Performance** : Recherche vectorielle ultra-rapide
- **Extensibilité** : Facilement adaptable à d'autres matières
- **Modularité** : Code bien structuré et maintenable

### Avantages pédagogiques
- **Gain de temps** : Recherche instantanée dans les cours
- **Autonomie** : Les étudiants peuvent s'aider eux-mêmes
- **Révision efficace** : Accès rapide aux informations clés
- **Réduction de charge** : Moins de questions répétitives aux professeurs

## 🔧 Configuration

### Variables d'environnement (optionnel)
```bash
# Pour utiliser OpenAI (optionnel)
export OPENAI_API_KEY="votre-clé-api"

# Pour utiliser HuggingFace Hub (optionnel)
export HUGGINGFACE_API_TOKEN="votre-token"
```

### Personnalisation
- Modifiez `src/rag_engine.py` pour changer le modèle LLM
- Ajustez `src/document_loader.py` pour d'autres formats de documents
- Personnalisez l'interface dans `app.py`

## 🧪 Tests

### Test du système
```bash
python test_system.py
```

### Test manuel
1. Ajoutez des documents dans `data/`
2. Lancez l'application
3. Testez avec les questions suggérées

## 📈 Développements futurs

- [ ] Support pour plus de formats de documents
- [ ] Interface mobile responsive
- [ ] Export des conversations
- [ ] Intégration avec des LMS (Moodle, etc.)
- [ ] Support multilingue
- [ ] API REST pour intégration

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

Développé pour un projet académique de soutenance.

---

**🎓 Assistant Étudiant Intelligent - Propulsé par RAG et IA**
