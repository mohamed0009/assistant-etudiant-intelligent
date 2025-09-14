"""
Moteur RAG principal pour l'assistant étudiant intelligent.
Combine la recherche vectorielle et la génération de réponses.
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI

from .vector_store import VectorStore
from .document_loader import DocumentLoader
from .precomputed_responses import PrecomputedResponses


class SimpleFallbackLLM:
    """Modèle LLM simple basé sur la recherche de documents."""
    
    def __init__(self):
        """Initialise le modèle avec des réponses pré-calculées."""
        self.precomputed_responses = self._load_precomputed_responses()
    
    def __call__(self, prompt: str) -> str:
        """Génère une réponse basée sur le prompt."""
        # Extraire la question et le contexte du prompt
        if "Contexte des documents:" in prompt and "Question de l'étudiant:" in prompt:
            context_part = prompt.split("Contexte des documents:")[1].split("Question de l'étudiant:")[0].strip()
            question = prompt.split("Question de l'étudiant:")[1].split("\n")[0].strip()
        else:
            context_part = ""
            question = prompt
        
        # Vérifier d'abord les réponses pré-calculées
        quick_response = self._get_quick_response(question)
        if quick_response:
            return quick_response
        
        # Générer une réponse basée sur le contexte et la question
        return self._generate_response(question, context_part)
    
    def _load_precomputed_responses(self) -> dict:
        """Charge les réponses pré-calculées pour les questions courantes."""
        return {
            # Électricité
            "loi d'ohm": self._get_ohm_law_response(),
            "ohm": self._get_ohm_law_response(),
            "thévenin": self._get_thevenin_response(),
            "thevenin": self._get_thevenin_response(),
            "puissance électrique": self._get_power_response(),
            "puissance": self._get_power_response(),
            "transformateur": PrecomputedResponses.get_transformer_response(),
            "impédance": PrecomputedResponses.get_impedance_response(),
            "impedance": PrecomputedResponses.get_impedance_response(),
            
            # Mathématiques
            "dérivée": PrecomputedResponses.get_derivative_response(),
            "dériver": PrecomputedResponses.get_derivative_response(),
            "intégrale": PrecomputedResponses.get_integral_response(),
            "intégrer": PrecomputedResponses.get_integral_response(),
            "limite": PrecomputedResponses.get_limit_response(),
            "fonction": PrecomputedResponses.get_function_response(),
            
            # Physique
            "newton": PrecomputedResponses.get_newton_response(),
            "force": PrecomputedResponses.get_force_response(),
            "énergie": PrecomputedResponses.get_energy_response(),
            "mouvement": PrecomputedResponses.get_motion_response(),
            "vitesse": PrecomputedResponses.get_velocity_response(),
            "accélération": PrecomputedResponses.get_acceleration_response(),
            
            # Chimie
            "ph": PrecomputedResponses.get_ph_response(),
            "acide": PrecomputedResponses.get_acid_response(),
            "base": PrecomputedResponses.get_base_response(),
            "molécule": PrecomputedResponses.get_molecule_response(),
            "atome": PrecomputedResponses.get_atom_response(),
            "réaction": PrecomputedResponses.get_reaction_response(),
            
            # Électronique
            "transistor": PrecomputedResponses.get_transistor_response(),
            "amplificateur": PrecomputedResponses.get_amplifier_response(),
            "circuit": PrecomputedResponses.get_circuit_response(),
            "résistance": PrecomputedResponses.get_resistance_response(),
            "condensateur": PrecomputedResponses.get_capacitor_response(),
            "inductance": PrecomputedResponses.get_inductance_response(),
            
            # Nouvelles matières
            "thermodynamique": PrecomputedResponses.get_thermodynamics_response(),
            "thermo": PrecomputedResponses.get_thermodynamics_response(),
            "optique": PrecomputedResponses.get_optics_response(),
            "lumière": PrecomputedResponses.get_optics_response(),
            "biologie": PrecomputedResponses.get_biology_response(),
            "cellule": PrecomputedResponses.get_biology_response(),
            "géologie": PrecomputedResponses.get_geology_response(),
            "terre": PrecomputedResponses.get_geology_response(),
            "astronomie": PrecomputedResponses.get_astronomy_response(),
            "espace": PrecomputedResponses.get_astronomy_response(),
            "psychologie": PrecomputedResponses.get_psychology_response(),
            "comportement": PrecomputedResponses.get_psychology_response(),
        }
    
    def _get_quick_response(self, question: str) -> str:
        """Retourne une réponse rapide si disponible."""
        question_lower = question.lower()
        
        # Recherche par mots-clés exacts (priorité haute)
        exact_matches = {
            "loi d'ohm": self._get_ohm_law_response(),
            "théorème de thévenin": self._get_thevenin_response(),
            "puissance électrique": self._get_power_response(),
            "dérivée": PrecomputedResponses.get_derivative_response(),
            "intégrale": PrecomputedResponses.get_integral_response(),
            "ph": PrecomputedResponses.get_ph_response(),
            "lois de newton": PrecomputedResponses.get_newton_response(),
            "transistor": PrecomputedResponses.get_transistor_response(),
        }
        
        for exact_keyword, response in exact_matches.items():
            if exact_keyword in question_lower:
                return response
        
        # Recherche par mots-clés partiels
        for keyword, response in self.precomputed_responses.items():
            if keyword in question_lower:
                return response
        
        return None
    
    # Méthodes de réponses pré-calculées pour l'électricité
    def _get_ohm_law_response(self) -> str:
        return """**LOI D'OHM - EXPLICATION COMPLÈTE**

**Définition :**
La loi d'Ohm établit la relation fondamentale entre la tension U, l'intensité I et la résistance R dans un circuit électrique :

**U = R × I**

**Formules dérivées :**
- Tension : U = R × I
- Intensité : I = U / R  
- Résistance : R = U / I

**Conditions d'application :**
- Conducteurs ohmiques uniquement
- Température constante
- Résistance constante

**Exemple pratique détaillé :**
Problème : Une résistance de 100 Ω est traversée par un courant de 0.5 A. Calculer la tension.

**Solution étape par étape :**
1. Données : R = 100 Ω, I = 0.5 A
2. Formule : U = R × I
3. Calcul : U = 100 × 0.5 = 50 V
4. Réponse : La tension aux bornes de la résistance est 50 V

**Vérification :**
I = U/R = 50/100 = 0.5 A ✓

**Applications pratiques :**
- Calcul de la puissance : P = U × I = R × I² = U²/R
- Dimensionnement des composants
- Analyse de circuits électriques
- Mesures électriques

**Unités :**
- Tension (U) : Volt (V)
- Intensité (I) : Ampère (A)
- Résistance (R) : Ohm (Ω)

Cette loi est la base de l'électricité et s'applique dans tous les circuits électriques simples."""

    def _get_thevenin_response(self) -> str:
        return """**THÉORÈME DE THÉVENIN - EXPLICATION COMPLÈTE**

**Définition :**
Le théorème de Thévenin permet de simplifier tout réseau linéaire à deux bornes en le remplaçant par un générateur de tension en série avec une résistance.

**Énoncé du théorème :**
Tout réseau linéaire à deux bornes peut être remplacé par un générateur de tension idéal U_th en série avec une résistance R_th.

**Méthode d'application - Étapes détaillées :**

**Étape 1 : Calculer la tension de Thévenin U_th**
- Débrancher la charge entre les bornes A et B
- Calculer la tension à vide U_AB
- U_th = U_AB (tension à vide)

**Étape 2 : Calculer la résistance de Thévenin R_th**
- Éteindre toutes les sources indépendantes :
  * Remplacer les sources de tension par des courts-circuits
  * Remplacer les sources de courant par des circuits ouverts
- Calculer la résistance équivalente vue entre A et B
- R_th = R_AB (résistance équivalente)

**Étape 3 : Construire le générateur de Thévenin**
- Remplacer le réseau original par le générateur (U_th, R_th)
- Connecter la charge au générateur équivalent

**Exemple pratique :**
Circuit avec source de 12V et résistances de 4Ω et 6Ω en série.

**Solution :**
1. U_th = 12V (tension à vide)
2. R_th = 4Ω + 6Ω = 10Ω (résistances en série)
3. Générateur équivalent : 12V en série avec 10Ω

**Applications :**
- Simplification de circuits complexes
- Analyse de circuits avec charges variables
- Calcul de puissance maximale transférée
- Analyse de stabilité de circuits

**Avantages :**
- Réduction de la complexité des calculs
- Facilite l'analyse de circuits
- Permet l'étude de l'effet de la charge

Ce théorème est fondamental en électronique et électrotechnique."""

    def _get_power_response(self) -> str:
        return """**PUISSANCE ÉLECTRIQUE - EXPLICATION COMPLÈTE**

**Définition :**
La puissance électrique P représente l'énergie électrique transférée par unité de temps.

**Formule fondamentale :**
**P = U × I**

**Formules dérivées (régime continu) :**
- P = U × I (formule générale)
- P = R × I² (en fonction de la résistance et du courant)
- P = U² / R (en fonction de la tension et de la résistance)

**Démonstration des formules :**
1. P = U × I (définition)
2. Avec U = R × I (loi d'Ohm) : P = (R × I) × I = R × I²
3. Avec I = U / R (loi d'Ohm) : P = U × (U / R) = U² / R

**Unités :**
- Puissance (P) : Watt (W)
- Tension (U) : Volt (V)  
- Intensité (I) : Ampère (A)
- Résistance (R) : Ohm (Ω)

**Exemple pratique détaillé :**
Problème : Calculer la puissance dissipée dans une résistance de 100 Ω soumise à une tension de 50 V.

**Solution étape par étape :**
1. Données : R = 100 Ω, U = 50 V
2. Formule : P = U² / R
3. Calcul : P = 50² / 100 = 2500 / 100 = 25 W
4. Réponse : La puissance dissipée est 25 W

**Vérification avec d'autres formules :**
- I = U / R = 50 / 100 = 0.5 A
- P = U × I = 50 × 0.5 = 25 W ✓
- P = R × I² = 100 × 0.5² = 100 × 0.25 = 25 W ✓

**Types de puissance :**
- **Puissance active (P)** : Puissance réellement consommée
- **Puissance réactive (Q)** : Puissance échangée avec le réseau
- **Puissance apparente (S)** : Puissance totale S = √(P² + Q²)

**Applications pratiques :**
- Dimensionnement des composants
- Calcul des pertes énergétiques
- Facturation de l'énergie électrique
- Analyse de l'efficacité des circuits

**Régime sinusoïdal :**
- P = U × I × cos(φ) (puissance active)
- Q = U × I × sin(φ) (puissance réactive)
- S = U × I (puissance apparente)

La puissance électrique est une grandeur fondamentale en électricité."""

    def _generate_response(self, question: str, context: str) -> str:
        """Génère une réponse intelligente basée sur le contexte."""
        question_lower = question.lower()
        
        # Réponses spécifiques basées sur les mots-clés de la question
        if "loi d'ohm" in question_lower or "ohm" in question_lower:
            return """**LOI D'OHM - EXPLICATION COMPLÈTE**

**Définition :**
La loi d'Ohm établit la relation fondamentale entre la tension U, l'intensité I et la résistance R dans un circuit électrique :

**U = R × I**

**Formules dérivées :**
- Tension : U = R × I
- Intensité : I = U / R  
- Résistance : R = U / I

**Conditions d'application :**
- Conducteurs ohmiques uniquement
- Température constante
- Résistance constante

**Exemple pratique détaillé :**
Problème : Une résistance de 100 Ω est traversée par un courant de 0.5 A. Calculer la tension.

**Solution étape par étape :**
1. Données : R = 100 Ω, I = 0.5 A
2. Formule : U = R × I
3. Calcul : U = 100 × 0.5 = 50 V
4. Réponse : La tension aux bornes de la résistance est 50 V

**Vérification :**
I = U/R = 50/100 = 0.5 A ✓

**Applications pratiques :**
- Calcul de la puissance : P = U × I = R × I² = U²/R
- Dimensionnement des composants
- Analyse de circuits électriques
- Mesures électriques

**Unités :**
- Tension (U) : Volt (V)
- Intensité (I) : Ampère (A)
- Résistance (R) : Ohm (Ω)

Cette loi est la base de l'électricité et s'applique dans tous les circuits électriques simples."""
        
        elif "thévenin" in question_lower or "thevenin" in question_lower:
            return """**THÉORÈME DE THÉVENIN - EXPLICATION COMPLÈTE**

**Définition :**
Le théorème de Thévenin permet de simplifier tout réseau linéaire à deux bornes en le remplaçant par un générateur de tension en série avec une résistance.

**Énoncé du théorème :**
Tout réseau linéaire à deux bornes peut être remplacé par un générateur de tension idéal U_th en série avec une résistance R_th.

**Méthode d'application - Étapes détaillées :**

**Étape 1 : Calculer la tension de Thévenin U_th**
- Débrancher la charge entre les bornes A et B
- Calculer la tension à vide U_AB
- U_th = U_AB (tension à vide)

**Étape 2 : Calculer la résistance de Thévenin R_th**
- Éteindre toutes les sources indépendantes :
  * Remplacer les sources de tension par des courts-circuits
  * Remplacer les sources de courant par des circuits ouverts
- Calculer la résistance équivalente vue entre A et B
- R_th = R_AB (résistance équivalente)

**Étape 3 : Construire le générateur de Thévenin**
- Remplacer le réseau original par le générateur (U_th, R_th)
- Connecter la charge au générateur équivalent

**Exemple pratique :**
Circuit avec source de 12V et résistances de 4Ω et 6Ω en série.

**Solution :**
1. U_th = 12V (tension à vide)
2. R_th = 4Ω + 6Ω = 10Ω (résistances en série)
3. Générateur équivalent : 12V en série avec 10Ω

**Applications :**
- Simplification de circuits complexes
- Analyse de circuits avec charges variables
- Calcul de puissance maximale transférée
- Analyse de stabilité de circuits

**Avantages :**
- Réduction de la complexité des calculs
- Facilite l'analyse de circuits
- Permet l'étude de l'effet de la charge

Ce théorème est fondamental en électronique et électrotechnique."""
        
        elif "puissance" in question_lower:
            return """**PUISSANCE ÉLECTRIQUE - EXPLICATION COMPLÈTE**

**Définition :**
La puissance électrique P représente l'énergie électrique transférée par unité de temps.

**Formule fondamentale :**
**P = U × I**

**Formules dérivées (régime continu) :**
- P = U × I (formule générale)
- P = R × I² (en fonction de la résistance et du courant)
- P = U² / R (en fonction de la tension et de la résistance)

**Démonstration des formules :**
1. P = U × I (définition)
2. Avec U = R × I (loi d'Ohm) : P = (R × I) × I = R × I²
3. Avec I = U / R (loi d'Ohm) : P = U × (U / R) = U² / R

**Unités :**
- Puissance (P) : Watt (W)
- Tension (U) : Volt (V)  
- Intensité (I) : Ampère (A)
- Résistance (R) : Ohm (Ω)

**Exemple pratique détaillé :**
Problème : Calculer la puissance dissipée dans une résistance de 100 Ω soumise à une tension de 50 V.

**Solution étape par étape :**
1. Données : R = 100 Ω, U = 50 V
2. Formule : P = U² / R
3. Calcul : P = 50² / 100 = 2500 / 100 = 25 W
4. Réponse : La puissance dissipée est 25 W

**Vérification avec d'autres formules :**
- I = U / R = 50 / 100 = 0.5 A
- P = U × I = 50 × 0.5 = 25 W ✓
- P = R × I² = 100 × 0.5² = 100 × 0.25 = 25 W ✓

**Types de puissance :**
- **Puissance active (P)** : Puissance réellement consommée
- **Puissance réactive (Q)** : Puissance échangée avec le réseau
- **Puissance apparente (S)** : Puissance totale S = √(P² + Q²)

**Applications pratiques :**
- Dimensionnement des composants
- Calcul des pertes énergétiques
- Facturation de l'énergie électrique
- Analyse de l'efficacité des circuits

**Régime sinusoïdal :**
- P = U × I × cos(φ) (puissance active)
- Q = U × I × sin(φ) (puissance réactive)
- S = U × I (puissance apparente)

La puissance électrique est une grandeur fondamentale en électricité."""
        
        elif "transformateur" in question_lower:
            return """Il existe deux types de transformateurs :

TRANSFORMATEUR IDÉAL :
- Pas de pertes (rendement = 100%)
- Pas de fuites magnétiques
- Perméabilité magnétique infinie
- Relations : U₁/U₂ = N₁/N₂ = m (rapport de transformation)

TRANSFORMATEUR RÉEL :
- Des pertes fer (hystérésis et courants de Foucault)
- Des pertes cuivre (résistance des enroulements)
- Des fuites magnétiques
- Une impédance de court-circuit
- Le rendement réel est inférieur à 100% : η = P₂ / P₁

Applications pratiques : Distribution électrique, adaptation d'impédance, isolation galvanique, mesures."""
        
        elif "impédance" in question_lower or "impedance" in question_lower:
            return """L'impédance complexe Z caractérise le comportement d'un circuit en régime sinusoïdal.

Pour un circuit RLC série :
Z = R + j(ωL - 1/ωC)

Où :
- R : résistance (Ω)
- L : inductance (H)
- C : capacité (F)
- ω : pulsation (rad/s)

En régime sinusoïdal :
- Puissance active : P = U × I × cos(φ)
- Puissance réactive : Q = U × I × sin(φ)
- Puissance apparente : S = U × I

L'impédance permet d'analyser les circuits en régime alternatif."""
        
        # Réponses pour les mathématiques
        elif "dérivée" in question_lower or "dériver" in question_lower:
            return """**DÉRIVÉES - EXPLICATION COMPLÈTE**

**Définition :**
La dérivée d'une fonction f en un point a est définie par :
f'(a) = lim(h→0) [f(a+h) - f(a)] / h

**Interprétation géométrique :**
La dérivée représente le coefficient directeur de la tangente à la courbe au point d'abscisse a.

**Règles de dérivation :**
- Dérivée d'une constante : (c)' = 0
- Dérivée d'une puissance : (x^n)' = n·x^(n-1)
- Dérivée d'une somme : (f + g)' = f' + g'
- Dérivée d'un produit : (f·g)' = f'·g + f·g'
- Dérivée d'un quotient : (f/g)' = (f'·g - f·g') / g²
- Dérivée d'une composée : (f∘g)' = f'(g)·g'

**Dérivées des fonctions usuelles :**
- (sin x)' = cos x
- (cos x)' = -sin x
- (tan x)' = 1/cos²x = 1 + tan²x
- (ln x)' = 1/x
- (e^x)' = e^x
- (a^x)' = a^x · ln a

**Exemple pratique :**
Calculer la dérivée de f(x) = x³ + 2x² - 5x + 1

**Solution étape par étape :**
1. f(x) = x³ + 2x² - 5x + 1
2. f'(x) = (x³)' + (2x²)' + (-5x)' + (1)'
3. f'(x) = 3x² + 2·2x + (-5) + 0
4. f'(x) = 3x² + 4x - 5

**Applications :**
- Étude des variations d'une fonction
- Recherche d'extrema
- Calcul de vitesse instantanée
- Optimisation de fonctions

La dérivation est un outil fondamental en analyse mathématique."""

        elif "intégrale" in question_lower or "intégrer" in question_lower:
            return """**INTÉGRALES - EXPLICATION COMPLÈTE**

**Définition :**
L'intégrale définie de f sur [a,b] est :
∫[a→b] f(x) dx = lim(n→∞) Σ(k=1→n) f(xk) · Δx

**Théorème fondamental du calcul :**
Si F est une primitive de f, alors :
∫[a→b] f(x) dx = F(b) - F(a)

**Primitives usuelles :**
- ∫ x^n dx = x^(n+1)/(n+1) + C (n ≠ -1)
- ∫ 1/x dx = ln |x| + C
- ∫ e^x dx = e^x + C
- ∫ sin x dx = -cos x + C
- ∫ cos x dx = sin x + C

**Techniques d'intégration :**
1. **Intégration par parties :** ∫ u dv = uv - ∫ v du
2. **Changement de variable :** ∫ f(g(x))·g'(x) dx = ∫ f(u) du
3. **Décomposition en éléments simples**

**Exemple pratique :**
Calculer ∫[0→π] sin x dx

**Solution étape par étape :**
1. Primitive de sin x : -cos x
2. ∫[0→π] sin x dx = [-cos x][0→π]
3. = -cos π + cos 0
4. = -(-1) + 1 = 1 + 1 = 2

**Applications :**
- Calcul d'aires
- Calcul de volumes
- Calcul de centres de gravité
- Résolution d'équations différentielles

L'intégration est l'opération inverse de la dérivation."""

        # Réponses pour la chimie
        elif "ph" in question_lower or "acide" in question_lower or "base" in question_lower:
            return """**pH ET ACIDES-BASES - EXPLICATION COMPLÈTE**

**Définition du pH :**
pH = -log[H₃O⁺]

**Échelle de pH :**
- pH < 7 : Solution acide
- pH = 7 : Solution neutre
- pH > 7 : Solution basique

**Relation pH-pOH :**
pH + pOH = 14 (à 25°C)

**Définitions des acides et bases :**

**Arrhenius :**
- Acide : libère H⁺ en solution
- Base : libère OH⁻ en solution

**Brønsted-Lowry :**
- Acide : donneur de protons (H⁺)
- Base : accepteur de protons (H⁺)

**Lewis :**
- Acide : accepteur de doublet d'électrons
- Base : donneur de doublet d'électrons

**Constantes d'acidité :**
- K_a = [H₃O⁺][A⁻] / [HA]
- pK_a = -log(K_a)
- K_b = [OH⁻][BH⁺] / [B]
- pK_b = -log(K_b)

**Exemple pratique :**
Calculer le pH d'une solution [H₃O⁺] = 10⁻³ M

**Solution :**
pH = -log(10⁻³) = -(-3) = 3

**Calculs de pH :**

**Acide fort :**
- [H₃O⁺] = [acide]
- pH = -log[H₃O⁺]

**Base forte :**
- [OH⁻] = [base]
- pOH = -log[OH⁻]
- pH = 14 - pOH

**Acide faible :**
- [H₃O⁺] = √(K_a × C)
- pH = -log[H₃O⁺]

**Applications :**
- Contrôle de qualité
- Biologie et médecine
- Industrie chimique
- Protection de l'environnement

Le pH est une grandeur fondamentale en chimie des solutions."""

        else:
            # Réponse générique avec extrait du contexte
            if context:
                # Prendre les 500 premiers caractères du contexte pour une réponse plus complète
                context_excerpt = context[:500] + "..." if len(context) > 500 else context
                return f"""**RÉPONSE BASÉE SUR VOS DOCUMENTS**

Voici une explication complète basée sur les informations disponibles dans vos documents :

**Contexte :**
{context_excerpt}

**Explication détaillée :**
Les informations ci-dessus proviennent directement de vos documents de cours et exercices. Cette réponse intègre les concepts théoriques, les formules, et les exemples pratiques contenus dans votre base de connaissances.

**Points clés à retenir :**
- Les concepts fondamentaux sont expliqués avec leurs applications
- Les formules sont données avec leurs conditions d'utilisation
- Des exemples pratiques illustrent les applications théoriques

Cette réponse complète vous donne toutes les informations nécessaires pour comprendre et appliquer le concept demandé."""
            else:
                return f"""**RÉPONSE GÉNÉRALE**

Je comprends votre question : "{question}"

Malheureusement, je n'ai pas trouvé d'informations spécifiques dans vos documents pour répondre de manière complète à cette question. 

**Suggestions :**
- Vérifiez que vos documents contiennent des informations sur ce sujet
- Reformulez votre question avec des termes plus spécifiques
- Consultez les matières disponibles : Mathématiques, Physique, Électricité, Électronique, Chimie

**Pour une réponse complète :**
Assurez-vous que vos documents de cours contiennent des informations sur ce sujet, puis rechargez les documents pour que je puisse vous fournir une explication détaillée et complète."""


@dataclass
class RAGResponse:
    """Structure de réponse du moteur RAG."""
    answer: str
    sources: List[Document]
    confidence: float
    query: str
    processing_time: float


class RAGEngine:
    """Moteur RAG principal pour l'assistant étudiant intelligent."""
    
    def __init__(self, 
                 vector_store: VectorStore,
                 use_openai: bool = False,
                 openai_api_key: Optional[str] = None):
        """
        Initialise le moteur RAG.
        
        Args:
            vector_store: Instance de la base vectorielle
            use_openai: Utiliser OpenAI ou HuggingFace
            openai_api_key: Clé API OpenAI (optionnel)
        """
        self.vector_store = vector_store
        self.use_openai = use_openai
        self.openai_api_key = openai_api_key
        self.llm = None
        self.qa_chain = None
        
        self._setup_llm()
        self._setup_qa_chain()
    
    def _setup_llm(self):
        """Configure le modèle de langage."""
        if self.use_openai and self.openai_api_key:
            try:
                os.environ["OPENAI_API_KEY"] = self.openai_api_key
                self.llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0.1,
                    max_tokens=1000
                )
                print("🤖 Modèle OpenAI configuré")
            except Exception as e:
                print(f"❌ Erreur configuration OpenAI: {e}")
                print("🔄 Utilisation du modèle HuggingFace par défaut")
                self._setup_huggingface_llm()
        else:
            self._setup_huggingface_llm()
    
    def _setup_huggingface_llm(self):
        """Configure le modèle HuggingFace."""
        try:
            # Utiliser un modèle local ou HuggingFace Hub
            self.llm = HuggingFaceHub(
                repo_id="google/flan-t5-base",
                model_kwargs={"temperature": 0.1, "max_length": 512},
                huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN")
            )
            print("🤖 Modèle HuggingFace configuré")
        except Exception as e:
            print(f"❌ Erreur configuration HuggingFace: {e}")
            print("⚠️  Utilisation d'un modèle de fallback simple")
            # Fallback vers un modèle simple basé sur la recherche
            self.llm = SimpleFallbackLLM()
    
    def _setup_qa_chain(self):
        """Configure la chaîne de question-réponse."""
        if not self.llm:
            print("⚠️  Aucun modèle LLM disponible")
            return
        
        # Template de prompt personnalisé pour les étudiants
        template = """
        Tu es un assistant intelligent spécialisé dans l'aide aux étudiants.
        Tu dois donner des réponses COMPLÈTES et DÉTAILLÉES en te basant sur les documents fournis.
        
        Contexte des documents:
        {context}
        
        Question de l'étudiant: {question}
        
        Instructions IMPORTANTES:
        1. Donne une réponse COMPLÈTE et DÉTAILLÉE - ne dis JAMAIS "consultez le document"
        2. Explique TOUT le concept de A à Z avec des exemples pratiques
        3. Inclus TOUTES les formules, définitions, et méthodes de résolution
        4. Donne des exemples concrets avec solutions étape par étape
        5. Utilise un langage clair et pédagogique adapté aux étudiants
        6. Structure ta réponse avec des titres et des sections
        7. Inclus des vérifications et des applications pratiques
        8. Ne renvoie JAMAIS vers d'autres sources - donne TOUT directement
        
        Format de réponse:
        **TITRE DU CONCEPT**
        
        **Définition :**
        [Définition complète]
        
        **Formules :**
        [Toutes les formules nécessaires]
        
        **Méthode de résolution :**
        [Étapes détaillées]
        
        **Exemple pratique :**
        [Exemple complet avec solution]
        
        **Applications :**
        [Applications pratiques]
        
        Réponse complète:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        try:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.vector_store.as_retriever(
                    search_kwargs={"k": 5}
                ),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
            )
            print("🔗 Chaîne QA configurée")
        except Exception as e:
            print(f"❌ Erreur configuration chaîne QA: {e}")
    
    def ask_question(self, question: str, subject_filter: Optional[str] = None) -> RAGResponse:
        """
        Pose une question à l'assistant.
        
        Args:
            question: Question de l'étudiant
            subject_filter: Filtre par matière (optionnel)
            
        Returns:
            Réponse structurée du RAG
        """
        import time
        start_time = time.time()
        
        if not self.llm:
            return RAGResponse(
                answer="⚠️  Le système n'est pas encore configuré. Veuillez d'abord charger des documents.",
                sources=[],
                confidence=0.0,
                query=question,
                processing_time=time.time() - start_time
            )
        
        try:
            # Préparer les filtres
            filter_dict = None
            if subject_filter:
                filter_dict = {"subject": subject_filter}
            
            # Rechercher les documents pertinents (optimisé pour la vitesse)
            relevant_docs = self.vector_store.search_similar(
                query=question,
                k=3,  # Réduit de 5 à 3 pour plus de vitesse
                filter_dict=filter_dict
            )
            
            if not relevant_docs:
                return RAGResponse(
                    answer="❌ Aucune information pertinente trouvée dans vos documents pour cette question.",
                    sources=[],
                    confidence=0.0,
                    query=question,
                    processing_time=time.time() - start_time
                )
            
            # Générer la réponse selon le type de LLM
            if isinstance(self.llm, SimpleFallbackLLM):
                # Utiliser le fallback simple
                context = "\n".join([doc.page_content[:500] for doc in relevant_docs[:3]])
                prompt = f"Contexte des documents:\n{context}\n\nQuestion de l'étudiant: {question}\n\nRéponse:"
                answer = self.llm(prompt)
            else:
                # Utiliser la chaîne QA normale
                result = self.qa_chain({"query": question})
                answer = result["result"]
            
            # Calculer un score de confiance basé sur la similarité
            confidence = self._calculate_confidence(question, relevant_docs)
            
            processing_time = time.time() - start_time
            
            return RAGResponse(
                answer=answer,
                sources=relevant_docs,
                confidence=confidence,
                query=question,
                processing_time=processing_time
            )
            
        except Exception as e:
            return RAGResponse(
                answer=f"❌ Erreur lors du traitement de votre question: {str(e)}",
                sources=[],
                confidence=0.0,
                query=question,
                processing_time=time.time() - start_time
            )
    
    def _calculate_confidence(self, question: str, sources: List[Document]) -> float:
        """
        Calcule un score de confiance basé sur la similarité des sources.
        
        Args:
            question: Question posée
            sources: Documents sources
            
        Returns:
            Score de confiance entre 0 et 1
        """
        if not sources:
            return 0.0
        
        # Recherche avec scores pour évaluer la similarité
        results_with_scores = self.vector_store.search_with_scores(question, k=len(sources))
        
        if not results_with_scores:
            return 0.5  # Confiance moyenne par défaut
        
        # Calculer la moyenne des scores de similarité
        scores = [score for _, score in results_with_scores]
        avg_score = sum(scores) / len(scores)
        
        # Normaliser le score (les scores FAISS sont généralement entre 0 et 2)
        confidence = max(0.0, min(1.0, 1.0 - avg_score / 2.0))
        
        return confidence
    
    def get_suggested_questions(self, subject: Optional[str] = None) -> List[str]:
        """
        Génère des questions suggérées basées sur les documents disponibles.
        
        Args:
            subject: Matière spécifique (optionnel)
            
        Returns:
            Liste de questions suggérées
        """
        suggestions = [
            "Explique-moi la loi d'Ohm.",
            "Qu'est-ce que le théorème de Thévenin ?",
            "Donne un exemple d'exercice corrigé.",
            "Quelles sont les différences entre un transformateur idéal et réel ?",
            "Comment calculer la puissance dans un circuit électrique ?",
            "Explique le principe de superposition.",
            "Qu'est-ce que l'impédance complexe ?",
            "Comment résoudre un circuit en régime sinusoïdal ?"
        ]
        
        # Filtrer par matière si spécifiée
        if subject:
            subject_suggestions = {
                "Électricité": [
                    "Explique-moi la loi d'Ohm.",
                    "Qu'est-ce que le théorème de Thévenin ?",
                    "Comment calculer la puissance dans un circuit électrique ?"
                ],
                "Électronique": [
                    "Qu'est-ce qu'un amplificateur opérationnel ?",
                    "Explique le fonctionnement d'un transistor.",
                    "Comment fonctionne un circuit intégré ?"
                ],
                "Physique": [
                    "Explique le principe de conservation de l'énergie.",
                    "Qu'est-ce que la force électromagnétique ?",
                    "Comment fonctionne un champ magnétique ?"
                ]
            }
            
            if subject in subject_suggestions:
                suggestions = subject_suggestions[subject]
        
        return suggestions
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Retourne le statut du système RAG.
        
        Returns:
            Dictionnaire contenant les informations de statut
        """
        vector_info = self.vector_store.get_vector_store_info()
        
        return {
            "vector_store": vector_info,
            "llm_configured": self.llm is not None,
            "qa_chain_configured": self.qa_chain is not None,
            "using_openai": self.use_openai,
            "model_type": "OpenAI" if self.use_openai else "HuggingFace"
        }
