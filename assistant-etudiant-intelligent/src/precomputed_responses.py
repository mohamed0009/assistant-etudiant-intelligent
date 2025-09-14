"""
Réponses pré-calculées pour améliorer les performances de l'assistant RAG.
Ces réponses sont optimisées pour des réponses rapides et complètes.
"""

class PrecomputedResponses:
    """Classe contenant toutes les réponses pré-calculées."""
    
    @staticmethod
    def get_derivative_response() -> str:
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

    @staticmethod
    def get_integral_response() -> str:
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

    @staticmethod
    def get_ph_response() -> str:
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

    @staticmethod
    def get_newton_response() -> str:
        return """**LOIS DE NEWTON - EXPLICATION COMPLÈTE**

**Première loi de Newton (Principe d'inertie) :**
Un objet au repos reste au repos, et un objet en mouvement continue à se déplacer à vitesse constante, sauf si une force nette agit sur lui.

**Deuxième loi de Newton (Principe fondamental) :**
F = m × a
- F : force nette (N)
- m : masse (kg)
- a : accélération (m/s²)

**Troisième loi de Newton (Action-Réaction) :**
Pour chaque action, il y a une réaction égale et opposée.

**Exemple pratique :**
Un objet de 5 kg subit une force de 20 N. Calculer son accélération.

**Solution :**
1. Données : m = 5 kg, F = 20 N
2. Formule : F = m × a
3. Calcul : a = F/m = 20/5 = 4 m/s²
4. Réponse : L'accélération est 4 m/s²

**Applications :**
- Mécanique classique
- Ingénierie
- Astronomie
- Physique des particules

Les lois de Newton sont fondamentales en mécanique."""

    @staticmethod
    def get_transistor_response() -> str:
        return """**TRANSISTOR - EXPLICATION COMPLÈTE**

**Définition :**
Le transistor est un composant électronique à semi-conducteur qui peut amplifier ou commuter des signaux électriques.

**Types principaux :**
- **BJT (Bipolar Junction Transistor)** : NPN et PNP
- **FET (Field Effect Transistor)** : MOSFET et JFET

**Fonctionnement BJT :**
- **Base** : Contrôle le courant
- **Collecteur** : Collecte les électrons
- **Émetteur** : Émet les électrons

**Modes de fonctionnement :**
- **Mode actif** : Amplification
- **Mode saturation** : Commutation ON
- **Mode coupure** : Commutation OFF

**Exemple pratique :**
Transistor NPN en mode actif avec β = 100, I_B = 10 μA

**Solution :**
1. I_C = β × I_B = 100 × 10 μA = 1 mA
2. I_E = I_C + I_B = 1 mA + 10 μA = 1.01 mA

**Applications :**
- Amplificateurs
- Commutateurs
- Oscillateurs
- Circuits logiques

Le transistor est le composant fondamental de l'électronique moderne."""

    @staticmethod
    def get_impedance_response() -> str:
        return """**IMPÉDANCE COMPLEXE - EXPLICATION COMPLÈTE**

**Définition :**
L'impédance complexe Z caractérise le comportement d'un circuit en régime sinusoïdal.

**Forme générale :**
Z = R + jX
- R : partie réelle (résistance)
- X : partie imaginaire (réactance)
- j : unité imaginaire

**Impédances des composants :**
- **Résistance** : Z_R = R
- **Inductance** : Z_L = jωL
- **Condensateur** : Z_C = 1/(jωC) = -j/(ωC)

**Circuit RLC série :**
Z = R + j(ωL - 1/ωC)

**Exemple pratique :**
Circuit RLC avec R = 10Ω, L = 0.1H, C = 100μF, f = 50Hz

**Solution :**
1. ω = 2πf = 2π × 50 = 314 rad/s
2. X_L = ωL = 314 × 0.1 = 31.4Ω
3. X_C = 1/(ωC) = 1/(314 × 100×10⁻⁶) = 31.8Ω
4. Z = 10 + j(31.4 - 31.8) = 10 - j0.4Ω

**Applications :**
- Analyse de circuits AC
- Filtres électroniques
- Résonance
- Adaptation d'impédance

L'impédance complexe est essentielle en électronique."""

    @staticmethod
    def get_transformer_response() -> str:
        return """**TRANSFORMATEUR - EXPLICATION COMPLÈTE**

**Définition :**
Le transformateur est un dispositif qui transfère l'énergie électrique d'un circuit à un autre par induction magnétique.

**Principe de fonctionnement :**
- Champ magnétique variable dans le primaire
- Induction de tension dans le secondaire
- Conservation de la puissance (idéalement)

**Types de transformateurs :**

**TRANSFORMATEUR IDÉAL :**
- Pas de pertes (rendement = 100%)
- Pas de fuites magnétiques
- Perméabilité magnétique infinie
- Relations : U₁/U₂ = N₁/N₂ = m (rapport de transformation)

**TRANSFORMATEUR RÉEL :**
- Des pertes fer (hystérésis et courants de Foucault)
- Des pertes cuivre (résistance des enroulements)
- Des fuites magnétiques
- Une impédance de court-circuit
- Le rendement réel est inférieur à 100% : η = P₂ / P₁

**Exemple pratique :**
Transformateur 220V/12V avec 1000 spires au primaire

**Solution :**
1. Rapport de transformation : m = 220/12 = 18.33
2. Spires secondaire : N₂ = N₁/m = 1000/18.33 = 54.5 spires
3. Si I₁ = 1A, alors I₂ = I₁ × m = 1 × 18.33 = 18.33A

**Applications :**
- Distribution électrique
- Adaptation d'impédance
- Isolation galvanique
- Mesures électriques

Le transformateur est fondamental en électrotechnique."""

    @staticmethod
    def get_limit_response() -> str:
        return """**LIMITES - EXPLICATION COMPLÈTE**

**Définition :**
La limite d'une fonction f(x) quand x tend vers a est L si :
lim(x→a) f(x) = L

**Limites usuelles :**
- lim(x→0) sin(x)/x = 1
- lim(x→∞) 1/x = 0
- lim(x→0) (1-cos(x))/x = 0
- lim(x→∞) e^x = ∞
- lim(x→-∞) e^x = 0

**Techniques de calcul :**
1. **Substitution directe**
2. **Factorisation**
3. **Règle de L'Hôpital**
4. **Développements limités**

**Exemple pratique :**
Calculer lim(x→2) (x²-4)/(x-2)

**Solution :**
1. Forme indéterminée 0/0
2. Factorisation : x²-4 = (x-2)(x+2)
3. lim(x→2) (x-2)(x+2)/(x-2) = lim(x→2) (x+2)
4. = 2 + 2 = 4

**Applications :**
- Continuité des fonctions
- Calcul de dérivées
- Analyse asymptotique
- Optimisation

Les limites sont fondamentales en analyse mathématique."""

    @staticmethod
    def get_function_response() -> str:
        return """**FONCTIONS - EXPLICATION COMPLÈTE**

**Définition :**
Une fonction f est une relation qui associe à chaque élément x d'un ensemble de départ (domaine) un unique élément y d'un ensemble d'arrivée (codomaine).

**Notation :**
f : A → B
x ↦ f(x) = y

**Types de fonctions :**
- **Fonction injective** : f(x₁) = f(x₂) ⇒ x₁ = x₂
- **Fonction surjective** : ∀y ∈ B, ∃x ∈ A tel que f(x) = y
- **Fonction bijective** : injective et surjective

**Fonctions usuelles :**
- **Polynômes** : f(x) = aₙxⁿ + ... + a₁x + a₀
- **Exponentielle** : f(x) = e^x
- **Logarithme** : f(x) = ln(x)
- **Trigonométriques** : sin(x), cos(x), tan(x)

**Exemple pratique :**
Étudier la fonction f(x) = x² - 4x + 3

**Solution :**
1. **Domaine** : ℝ
2. **Dérivée** : f'(x) = 2x - 4
3. **Points critiques** : f'(x) = 0 ⇒ x = 2
4. **Variations** : f'(x) < 0 si x < 2, f'(x) > 0 si x > 2
5. **Minimum** : f(2) = 4 - 8 + 3 = -1

**Applications :**
- Modélisation mathématique
- Optimisation
- Analyse de données
- Physique et ingénierie

Les fonctions sont la base de l'analyse mathématique."""

    @staticmethod
    def get_force_response() -> str:
        return """**FORCES - EXPLICATION COMPLÈTE**

**Définition :**
Une force est une grandeur vectorielle qui peut modifier l'état de mouvement ou de repos d'un objet.

**Caractéristiques d'une force :**
- **Point d'application**
- **Direction**
- **Sens**
- **Intensité** (module)

**Types de forces :**
- **Force de gravité** : F = mg
- **Force de frottement** : F = μN
- **Force élastique** : F = -kx (loi de Hooke)
- **Force centripète** : F = mv²/r

**Principe fondamental :**
F = ma (deuxième loi de Newton)

**Exemple pratique :**
Un objet de 2 kg subit une force de 10 N. Calculer son accélération.

**Solution :**
1. Données : m = 2 kg, F = 10 N
2. Formule : F = ma
3. Calcul : a = F/m = 10/2 = 5 m/s²
4. Réponse : L'accélération est 5 m/s²

**Applications :**
- Mécanique classique
- Ingénierie
- Astronomie
- Physique des particules

Les forces sont fondamentales en physique."""

    @staticmethod
    def get_energy_response() -> str:
        return """**ÉNERGIE - EXPLICATION COMPLÈTE**

**Définition :**
L'énergie est la capacité d'un système à effectuer un travail.

**Principe de conservation :**
L'énergie totale d'un système isolé reste constante.

**Types d'énergie :**
- **Énergie cinétique** : E_c = ½mv²
- **Énergie potentielle** : E_p = mgh
- **Énergie mécanique** : E_m = E_c + E_p
- **Énergie thermique** : E_th = mcΔT

**Unités :**
- Joule (J) dans le système international
- 1 J = 1 kg·m²/s²

**Exemple pratique :**
Un objet de 1 kg tombe de 10 m de hauteur. Calculer sa vitesse au sol.

**Solution :**
1. Conservation de l'énergie : E_p = E_c
2. mgh = ½mv²
3. v = √(2gh) = √(2 × 9.81 × 10) = √196.2 = 14 m/s

**Applications :**
- Mécanique
- Thermodynamique
- Électricité
- Physique nucléaire

L'énergie est un concept fondamental en physique."""

    @staticmethod
    def get_motion_response() -> str:
        return """**MOUVEMENT - EXPLICATION COMPLÈTE**

**Types de mouvement :**
- **Mouvement rectiligne uniforme** : v = constante
- **Mouvement rectiligne uniformément accéléré** : a = constante
- **Mouvement circulaire** : trajectoire circulaire
- **Mouvement harmonique** : mouvement oscillatoire

**Équations du mouvement :**
- **Position** : x(t) = x₀ + v₀t + ½at²
- **Vitesse** : v(t) = v₀ + at
- **Accélération** : a = constante

**Exemple pratique :**
Un objet part du repos avec une accélération de 2 m/s². Calculer sa vitesse après 5 secondes.

**Solution :**
1. Données : v₀ = 0, a = 2 m/s², t = 5 s
2. Formule : v = v₀ + at
3. Calcul : v = 0 + 2 × 5 = 10 m/s
4. Réponse : La vitesse est 10 m/s

**Applications :**
- Mécanique classique
- Ingénierie
- Astronomie
- Physique des particules

Le mouvement est fondamental en mécanique."""

    @staticmethod
    def get_velocity_response() -> str:
        return """**VITESSE - EXPLICATION COMPLÈTE**

**Définition :**
La vitesse est la dérivée de la position par rapport au temps.

**Types de vitesse :**
- **Vitesse instantanée** : v = dx/dt
- **Vitesse moyenne** : v_m = Δx/Δt
- **Vitesse angulaire** : ω = dθ/dt

**Unités :**
- m/s dans le système international
- km/h (conversion : 1 m/s = 3.6 km/h)

**Exemple pratique :**
Un objet parcourt 100 m en 10 secondes. Calculer sa vitesse moyenne.

**Solution :**
1. Données : Δx = 100 m, Δt = 10 s
2. Formule : v_m = Δx/Δt
3. Calcul : v_m = 100/10 = 10 m/s
4. Réponse : La vitesse moyenne est 10 m/s

**Applications :**
- Mécanique
- Cinématique
- Dynamique
- Physique des particules

La vitesse est fondamentale en mécanique."""

    @staticmethod
    def get_acceleration_response() -> str:
        return """**ACCÉLÉRATION - EXPLICATION COMPLÈTE**

**Définition :**
L'accélération est la dérivée de la vitesse par rapport au temps.

**Formule :**
a = dv/dt = d²x/dt²

**Types d'accélération :**
- **Accélération tangentielle** : a_t = dv/dt
- **Accélération centripète** : a_c = v²/r
- **Accélération de la pesanteur** : g = 9.81 m/s²

**Unités :**
- m/s² dans le système international

**Exemple pratique :**
Un objet passe de 10 m/s à 30 m/s en 5 secondes. Calculer son accélération.

**Solution :**
1. Données : v₀ = 10 m/s, v = 30 m/s, t = 5 s
2. Formule : a = (v - v₀)/t
3. Calcul : a = (30 - 10)/5 = 20/5 = 4 m/s²
4. Réponse : L'accélération est 4 m/s²

**Applications :**
- Mécanique
- Dynamique
- Physique des particules
- Ingénierie

L'accélération est fondamentale en mécanique."""

    @staticmethod
    def get_acid_response() -> str:
        return """**ACIDES - EXPLICATION COMPLÈTE**

**Définition :**
Un acide est une substance qui libère des ions H⁺ en solution aqueuse.

**Classification :**
- **Acides forts** : HCl, H₂SO₄, HNO₃
- **Acides faibles** : CH₃COOH, H₂CO₃

**Propriétés :**
- Goût acide
- Conducteurs électriques
- Réagissent avec les métaux
- Changent la couleur des indicateurs

**Exemple pratique :**
Calculer le pH d'une solution d'acide chlorhydrique 0.1 M

**Solution :**
1. HCl est un acide fort : [H⁺] = [HCl] = 0.1 M
2. pH = -log[H⁺] = -log(0.1) = 1
3. Réponse : Le pH est 1

**Applications :**
- Industrie chimique
- Biologie
- Médecine
- Agriculture

Les acides sont fondamentaux en chimie."""

    @staticmethod
    def get_base_response() -> str:
        return """**BASES - EXPLICATION COMPLÈTE**

**Définition :**
Une base est une substance qui libère des ions OH⁻ en solution aqueuse.

**Classification :**
- **Bases fortes** : NaOH, KOH, Ca(OH)₂
- **Bases faibles** : NH₃, CH₃NH₂

**Propriétés :**
- Goût amer
- Conducteurs électriques
- Réagissent avec les acides
- Changent la couleur des indicateurs

**Exemple pratique :**
Calculer le pH d'une solution de soude 0.01 M

**Solution :**
1. NaOH est une base forte : [OH⁻] = [NaOH] = 0.01 M
2. pOH = -log[OH⁻] = -log(0.01) = 2
3. pH = 14 - pOH = 14 - 2 = 12
4. Réponse : Le pH est 12

**Applications :**
- Industrie chimique
- Biologie
- Médecine
- Agriculture

Les bases sont fondamentales en chimie."""

    @staticmethod
    def get_molecule_response() -> str:
        return """**MOLÉCULES - EXPLICATION COMPLÈTE**

**Définition :**
Une molécule est un ensemble d'atomes liés par des liaisons chimiques.

**Types de liaisons :**
- **Liaison covalente** : partage d'électrons
- **Liaison ionique** : transfert d'électrons
- **Liaison métallique** : électrons délocalisés

**Exemple pratique :**
Molécule d'eau H₂O

**Solution :**
1. **Formule** : H₂O
2. **Géométrie** : Angulaire (104.5°)
3. **Polarité** : Polaire
4. **Liaisons** : 2 liaisons O-H covalentes

**Applications :**
- Chimie organique
- Biologie
- Matériaux
- Pharmacie

Les molécules sont fondamentales en chimie."""

    @staticmethod
    def get_atom_response() -> str:
        return """**ATOMES - EXPLICATION COMPLÈTE**

**Définition :**
Un atome est la plus petite particule d'un élément qui conserve ses propriétés chimiques.

**Structure :**
- **Noyau** : protons (positifs) et neutrons (neutres)
- **Électrons** : particules négatives en orbite

**Exemple pratique :**
Atome de carbone (C)

**Solution :**
1. **Numéro atomique** : Z = 6
2. **Protons** : 6
3. **Électrons** : 6
4. **Neutrons** : 6 (isotope ¹²C)

**Applications :**
- Chimie
- Physique
- Biologie
- Matériaux

Les atomes sont la base de la matière."""

    @staticmethod
    def get_reaction_response() -> str:
        return """**RÉACTIONS CHIMIQUES - EXPLICATION COMPLÈTE**

**Définition :**
Une réaction chimique est une transformation de substances en d'autres substances.

**Types de réactions :**
- **Synthèse** : A + B → C
- **Décomposition** : C → A + B
- **Substitution** : A + BC → AC + B
- **Double déplacement** : AB + CD → AD + CB

**Exemple pratique :**
Réaction de combustion du méthane

**Solution :**
1. **Équation** : CH₄ + 2O₂ → CO₂ + 2H₂O
2. **Type** : Combustion
3. **Produits** : CO₂ et H₂O
4. **Énergie** : Libérée (exothermique)

**Applications :**
- Industrie chimique
- Biologie
- Médecine
- Environnement

Les réactions chimiques sont fondamentales en chimie."""

    @staticmethod
    def get_amplifier_response() -> str:
        return """**AMPLIFICATEURS - EXPLICATION COMPLÈTE**

**Définition :**
Un amplificateur est un dispositif qui augmente l'amplitude d'un signal électrique.

**Types d'amplificateurs :**
- **Amplificateur opérationnel** : Gain élevé, impédance d'entrée élevée
- **Amplificateur de puissance** : Forte puissance de sortie
- **Amplificateur différentiel** : Amplifie la différence entre deux signaux

**Paramètres importants :**
- **Gain** : A = V_out/V_in
- **Bande passante** : Plage de fréquences
- **Impédance d'entrée** : Résistance d'entrée
- **Impédance de sortie** : Résistance de sortie

**Exemple pratique :**
Amplificateur avec gain de 10 et signal d'entrée de 0.1 V

**Solution :**
1. Données : A = 10, V_in = 0.1 V
2. Formule : V_out = A × V_in
3. Calcul : V_out = 10 × 0.1 = 1 V
4. Réponse : Le signal de sortie est 1 V

**Applications :**
- Audio
- Radiofréquences
- Instrumentation
- Télécommunications

Les amplificateurs sont fondamentaux en électronique."""

    @staticmethod
    def get_circuit_response() -> str:
        return """**CIRCUITS ÉLECTRIQUES - EXPLICATION COMPLÈTE**

**Définition :**
Un circuit électrique est un ensemble de composants électriques connectés par des conducteurs.

**Lois fondamentales :**
- **Loi d'Ohm** : U = R × I
- **Loi des nœuds** : ΣI_entrant = ΣI_sortant
- **Loi des mailles** : ΣU = 0 dans une maille

**Types de circuits :**
- **Circuit série** : Composants en série
- **Circuit parallèle** : Composants en parallèle
- **Circuit mixte** : Combinaison série-parallèle

**Exemple pratique :**
Circuit série avec R₁ = 10Ω, R₂ = 20Ω, U = 30V

**Solution :**
1. Résistance équivalente : R_eq = R₁ + R₂ = 10 + 20 = 30Ω
2. Courant : I = U/R_eq = 30/30 = 1 A
3. Tension R₁ : U₁ = R₁ × I = 10 × 1 = 10 V
4. Tension R₂ : U₂ = R₂ × I = 20 × 1 = 20 V

**Applications :**
- Électronique
- Électrotechnique
- Télécommunications
- Informatique

Les circuits électriques sont fondamentaux en électronique."""

    @staticmethod
    def get_resistance_response() -> str:
        return """**RÉSISTANCE ÉLECTRIQUE - EXPLICATION COMPLÈTE**

**Définition :**
La résistance électrique est l'opposition au passage du courant électrique.

**Loi d'Ohm :**
R = U/I
- R : résistance (Ω)
- U : tension (V)
- I : intensité (A)

**Facteurs influençant la résistance :**
- **Matériau** : Conductivité
- **Longueur** : R ∝ L
- **Section** : R ∝ 1/S
- **Température** : R = R₀(1 + αΔT)

**Exemple pratique :**
Fil de cuivre de 100 m, section 1 mm², résistivité 1.7×10⁻⁸ Ω·m

**Solution :**
1. Données : L = 100 m, S = 1×10⁻⁶ m², ρ = 1.7×10⁻⁸ Ω·m
2. Formule : R = ρL/S
3. Calcul : R = 1.7×10⁻⁸ × 100 / 1×10⁻⁶ = 1.7 Ω
4. Réponse : La résistance est 1.7 Ω

**Applications :**
- Électronique
- Électrotechnique
- Mesures
- Chauffage

La résistance est fondamentale en électricité."""

    @staticmethod
    def get_capacitor_response() -> str:
        return """**CONDENSATEUR - EXPLICATION COMPLÈTE**

**Définition :**
Un condensateur est un composant qui stocke l'énergie électrique sous forme de champ électrique.

**Capacité :**
C = Q/U
- C : capacité (F)
- Q : charge (C)
- U : tension (V)

**Énergie stockée :**
E = ½CU²

**Exemple pratique :**
Condensateur de 100 μF chargé à 12 V

**Solution :**
1. Données : C = 100×10⁻⁶ F, U = 12 V
2. Charge : Q = CU = 100×10⁻⁶ × 12 = 1.2×10⁻³ C
3. Énergie : E = ½CU² = ½ × 100×10⁻⁶ × 12² = 7.2×10⁻³ J
4. Réponse : Charge = 1.2 mC, Énergie = 7.2 mJ

**Applications :**
- Filtres
- Alimentations
- Couplage
- Stockage d'énergie

Le condensateur est fondamental en électronique."""

    @staticmethod
    def get_inductance_response() -> str:
        return """**INDUCTANCE - EXPLICATION COMPLÈTE**

**Définition :**
Une inductance est un composant qui stocke l'énergie magnétique.

**Inductance :**
L = Φ/I
- L : inductance (H)
- Φ : flux magnétique (Wb)
- I : intensité (A)

**Énergie stockée :**
E = ½LI²

**Exemple pratique :**
Inductance de 10 mH avec courant de 2 A

**Solution :**
1. Données : L = 10×10⁻³ H, I = 2 A
2. Énergie : E = ½LI² = ½ × 10×10⁻³ × 2² = 20×10⁻³ J
3. Réponse : L'énergie stockée est 20 mJ

**Applications :**
- Filtres
- Alimentations
- Couplage
- Stockage d'énergie

L'inductance est fondamentale en électronique."""

    # Nouvelles réponses pré-calculées pour les matières ajoutées
    
    @staticmethod
    def get_thermodynamics_response() -> str:
        return """**THERMODYNAMIQUE - EXPLICATION COMPLÈTE**

**Premier principe de la thermodynamique :**
ΔU = Q - W
- ΔU : variation d'énergie interne
- Q : chaleur reçue par le système
- W : travail effectué par le système

**Deuxième principe :**
L'entropie d'un système isolé ne peut que croître : ΔS ≥ 0

**Entropie :**
dS = δQ_rev / T
- δQ_rev : chaleur échangée de manière réversible
- T : température absolue

**Gaz parfait :**
PV = nRT
- P : pression (Pa)
- V : volume (m³)
- n : nombre de moles
- R : constante des gaz parfaits (8,314 J/mol·K)
- T : température absolue (K)

**Exemple pratique :**
Calculer le travail d'un gaz parfait lors d'une expansion isotherme de 2L à 5L à 300K.

**Solution :**
1. W = nRT ln(V2/V1)
2. W = 1 × 8,314 × 300 × ln(5/2)
3. W = 2,28 kJ

**Applications :**
- Moteurs thermiques
- Réfrigérateurs
- Centrales électriques
- Thermodynamique industrielle

La thermodynamique est fondamentale en physique et ingénierie."""

    @staticmethod
    def get_optics_response() -> str:
        return """**OPTIQUE - EXPLICATION COMPLÈTE**

**Loi de Snell-Descartes :**
n1 sin(i1) = n2 sin(i2)
- n1, n2 : indices de réfraction
- i1, i2 : angles d'incidence et de réfraction

**Vitesse de la lumière :**
Dans le vide : c = 3×10⁸ m/s
Dans un milieu : v = c/n

**Formule de conjugaison (lentilles) :**
1/f = 1/p + 1/p'
- f : distance focale
- p : distance objet
- p' : distance image

**Grandissement :**
γ = -p'/p

**Exemple pratique :**
Un rayon passe de l'air (n=1) au verre (n=1,5) avec un angle de 30°.

**Solution :**
1. n1 sin(i1) = n2 sin(i2)
2. 1 × sin(30°) = 1,5 × sin(i2)
3. sin(i2) = 0,5/1,5 = 0,333
4. i2 = arcsin(0,333) = 19,5°

**Applications :**
- Lentilles et miroirs
- Fibres optiques
- Lasers
- Instruments d'optique

L'optique est essentielle en physique et technologie."""

    @staticmethod
    def get_biology_response() -> str:
        return """**BIOLOGIE CELLULAIRE - EXPLICATION COMPLÈTE**

**Théorie cellulaire :**
- Tous les êtres vivants sont constitués de cellules
- La cellule est l'unité de base de la vie
- Toutes les cellules proviennent de cellules préexistantes

**Types de cellules :**
- Procaryotes : sans noyau (bactéries)
- Eucaryotes : avec noyau (plantes, animaux)

**Organites principaux :**
- Noyau : contient l'ADN
- Mitochondries : production d'ATP
- Réticulum endoplasmique : synthèse des protéines
- Appareil de Golgi : modification des protéines

**Division cellulaire :**
- Mitose : division équitable
- Méiose : division réductionnelle

**Exemple pratique :**
Expliquer le rôle de la pompe sodium-potassium.

**Solution :**
La pompe sodium-potassium maintient les concentrations ioniques :
- Expulse 3 Na+ vers l'extérieur
- Fait entrer 2 K+ vers l'intérieur
- Consomme 1 ATP
- Crée un potentiel de membrane de -70 mV

**Applications :**
- Médecine
- Biotechnologie
- Recherche fondamentale
- Thérapie génique

La biologie cellulaire est fondamentale en sciences de la vie."""

    @staticmethod
    def get_geology_response() -> str:
        return """**GÉOLOGIE - EXPLICATION COMPLÈTE**

**Structure de la Terre :**
- Croûte : 5-70 km d'épaisseur
- Manteau : 10-2900 km
- Noyau : 2900-6370 km

**Tectonique des plaques :**
- 7 plaques majeures
- Mouvements : divergence, convergence, coulissage
- Phénomènes : séismes, volcanisme, montagnes

**Types de roches :**
- Igneuses : solidification du magma
- Sédimentaires : accumulation de sédiments
- Métamorphiques : transformation sous pression/température

**Lois de Kepler (mécanique céleste) :**
- 1ère loi : orbites elliptiques
- 2ème loi : aires égales en temps égaux
- 3ème loi : T² ∝ a³

**Exemple pratique :**
Calculer la période orbitale de Mars (a = 1,52 UA).

**Solution :**
1. T² = a³ (en années et UA)
2. T² = (1,52)³ = 3,51
3. T = √3,51 = 1,87 années

**Applications :**
- Exploration pétrolière
- Génie civil
- Protection de l'environnement
- Prévention des risques

La géologie est essentielle pour comprendre la Terre."""

    @staticmethod
    def get_astronomy_response() -> str:
        return """**ASTRONOMIE - EXPLICATION COMPLÈTE**

**Système solaire :**
- 8 planètes : 4 telluriques, 4 géantes
- Soleil : étoile de type G2V
- Objets mineurs : astéroïdes, comètes

**Loi de Hubble :**
v = H0 × d
- v : vitesse de récession
- H0 : constante de Hubble (70 km/s/Mpc)
- d : distance

**Loi de la gravitation universelle :**
F = G × m1 × m2 / r²
- G = 6,67×10⁻¹¹ N·m²/kg²

**Exemple pratique :**
Calculer la période orbitale de Mars (a = 1,52 UA).

**Solution :**
1. T² = a³ (en années et UA)
2. T² = (1,52)³ = 3,51
3. T = √3,51 = 1,87 années

**Applications :**
- Navigation
- Calendriers
- Exploration spatiale
- Recherche d'exoplanètes

L'astronomie révèle l'univers et notre place dans le cosmos."""

    @staticmethod
    def get_psychology_response() -> str:
        return """**PSYCHOLOGIE - EXPLICATION COMPLÈTE**

**Définition :**
Science qui étudie le comportement et les processus mentaux.

**Branches principales :**
- Cognitive : processus mentaux
- Sociale : interactions
- Clinique : troubles mentaux
- Développement : évolution

**Méthodes de recherche :**
- Expérimentale : variables contrôlées
- Observationnelle : comportement naturel
- Corrélationnelle : relations entre variables

**Apprentissage :**
- Conditionnement classique : Pavlov
- Conditionnement opérant : Skinner
- Apprentissage social : Bandura

**Exemple pratique :**
Calculer le pourcentage de rétention après 24h.

**Solution :**
1. Mots appris : 20
2. Mots rappelés : 12
3. Pourcentage = (12/20) × 100 = 60%

**Applications :**
- Psychologie clinique
- Psychologie du travail
- Psychologie de l'éducation
- Recherche fondamentale

La psychologie aide à comprendre l'être humain."""
