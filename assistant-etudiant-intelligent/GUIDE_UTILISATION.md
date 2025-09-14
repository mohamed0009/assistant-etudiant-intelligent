# 📚 Guide d'Utilisation - Assistant Étudiant Intelligent

## 🚀 **Démarrage Rapide**

### **1. Lancement Automatique**
L'assistant charge **automatiquement** tous les documents au démarrage :
- ✅ **Chargement automatique** des documents du dossier `data/`
- ✅ **Interface prête** dès le lancement
- ✅ **Aucune action manuelle** requise

### **2. Accès à l'Application**
```bash
streamlit run app.py
```
Puis ouvrir : `http://localhost:8501`

## 📁 **Gestion des Documents**

### **Documents Automatiques**
L'assistant charge automatiquement :
- **Cours** : `cours_electricite.txt`, `cours_electronique.txt`
- **Exercices** : `td_electronique.txt`
- **Examens** : `examen_physique.txt`
- **Formats supportés** : PDF, DOCX, TXT

### **Ajout de Nouveaux Documents (Facultatif)**
Si tu veux ajouter de nouveaux cours :

1. **Placer les fichiers** dans le dossier `data/`
2. **Cliquer** sur "Recharger les Documents" dans la barre latérale
3. **Attendre** le message de confirmation

### **Structure Recommandée**
```
data/
├── cours_electricite.txt      # Cours d'électricité
├── cours_electronique.txt     # Cours d'électronique
├── td_electronique.txt        # Travaux dirigés
├── examen_physique.txt        # Examen corrigé
└── nouveaux_cours.pdf         # Nouveaux documents
```

## 💬 **Utilisation de l'Assistant**

### **Poser une Question**
1. **Taper** ta question dans la zone de texte
2. **Cliquer** sur "Envoyer"
3. **Attendre** la réponse avec métadonnées

### **Exemples de Questions**
- "Explique-moi la loi d'Ohm"
- "Qu'est-ce que le théorème de Thévenin ?"
- "Comment calculer la puissance électrique ?"
- "Différences entre transformateur idéal et réel"

### **Filtres par Matière**
- **Toutes les Matières** : Recherche globale
- **Électricité** : Questions spécifiques à l'électricité
- **Électronique** : Questions d'électronique
- **Physique** : Questions de physique
- **Mathématiques** : Questions de maths

## 📊 **Fonctionnalités Avancées**

### **Dashboard en Temps Réel**
- **Documents indexés** : Nombre de documents chargés
- **Vecteurs créés** : Segments de texte vectorisés
- **Segments** : Morceaux de texte analysés
- **Modèle utilisé** : Modèle d'IA actuel

### **Métadonnées des Réponses**
- **Confiance** : Fiabilité de la réponse (0-100%)
- **Temps** : Durée de traitement
- **Sources** : Documents utilisés
- **Qualité** : Évaluation de la réponse

### **Historique des Conversations**
- **Sauvegarde automatique** de toutes les questions/réponses
- **Accès rapide** aux conversations précédentes
- **Métadonnées complètes** pour chaque échange

## 🎯 **Scénarios d'Utilisation**

### **Révision de Cours**
1. **Charger** les documents de cours
2. **Poser** des questions spécifiques
3. **Consulter** les sources pour approfondir

### **Préparation d'Examen**
1. **Utiliser** les filtres par matière
2. **Demander** des explications détaillées
3. **Réviser** avec les questions suggérées

### **Aide aux Exercices**
1. **Poser** des questions sur les concepts
2. **Demander** des méthodes de résolution
3. **Vérifier** les calculs et formules

## 🔧 **Fonctionnalités Techniques**

### **Système RAG (Retrieval-Augmented Generation)**
- **Recherche intelligente** dans les documents
- **Génération de réponses** contextuelles
- **Sources vérifiables** pour chaque réponse

### **Modèles d'IA**
- **Embeddings** : `sentence-transformers/all-MiniLM-L6-v2`
- **LLM** : `ChatOpenAI` (GPT-3.5-turbo) ou fallback local
- **Base vectorielle** : FAISS pour recherche rapide

### **Performance**
- **Réponses instantanées** (< 2 secondes)
- **Recherche précise** dans les documents
- **Interface responsive** et moderne

## 🎓 **Pour les Étudiants**

### **Avantages**
- ✅ **Chargement automatique** - Aucune configuration
- ✅ **Réponses fiables** - Basées sur tes cours
- ✅ **Interface intuitive** - Facile à utiliser
- ✅ **Historique complet** - Suivi de tes questions

### **Conseils d'Utilisation**
- **Poser des questions précises** pour de meilleures réponses
- **Utiliser les filtres** pour des réponses ciblées
- **Consulter les sources** pour approfondir
- **Sauvegarder** les réponses importantes

## 🚀 **Démarrage Immédiat**

1. **Lancer** l'application : `streamlit run app.py`
2. **Attendre** le chargement automatique
3. **Commencer** à poser des questions !

**L'assistant est prêt à t'aider dans tes études !** 📚✨
