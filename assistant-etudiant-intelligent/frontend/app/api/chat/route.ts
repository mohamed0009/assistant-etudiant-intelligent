import { type NextRequest, NextResponse } from "next/server"

// Configuration de l'API backend
const API_BASE_URL = process.env.API_BASE_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  let message = ""
  
  try {
    const { message: requestMessage, documents, conversationId, studentId } = await request.json()
    message = requestMessage

    if (!message || message.trim().length === 0) {
      return NextResponse.json(
        { error: "Le message ne peut pas être vide" },
        { status: 400 }
      )
    }

    // Préparer la requête pour l'API backend avec Ollama
    const requestBody = {
      question: message,
      subject_filter: null,
      student_id: studentId || null,
      conversation_id: conversationId || null,
      save: true,
      create_conversation: !conversationId,
      title: `Conversation - ${new Date().toLocaleDateString()}`
    }

    // Appeler l'API backend avec Ollama
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify(requestBody),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        errorData.detail || 
        `Erreur API: ${response.status} ${response.statusText}`
      )
    }

    const data = await response.json()

    // Formater la réponse pour le frontend
    return NextResponse.json({
      response: data.answer,
      confidence: data.confidence,
      sources: data.sources || [],
      processing_time: data.processing_time,
      model_used: data.model_used,
      conversation_id: data.conversation_id,
      user_message_id: data.user_message_id,
      assistant_message_id: data.assistant_message_id,
      metadata: data.metadata || {}
    })

  } catch (error) {
    console.error("Erreur dans l'endpoint /api/chat:", error)
    
    // En cas d'erreur, retourner une réponse de fallback
    const fallbackResponse = generateFallbackResponse(message)
    
    return NextResponse.json({
      response: fallbackResponse,
      confidence: 0.5,
      sources: [],
      processing_time: 0.1,
      model_used: "fallback",
      conversation_id: null,
      user_message_id: null,
      assistant_message_id: null,
      metadata: { error: error instanceof Error ? error.message : "Erreur inconnue" }
    })
  }
}

function generateFallbackResponse(message: string): string {
  const responses = {
    "loi d'ohm":
      "La loi d'Ohm établit une relation entre la tension (U), l'intensité (I) et la résistance (R) : U = R × I. Cette loi fondamentale permet de calculer l'une de ces grandeurs connaissant les deux autres.",
    thévenin:
      "Le théorème de Thévenin permet de simplifier un circuit complexe en un générateur de tension équivalent en série avec une résistance. Cela facilite l'analyse des circuits électriques.",
    transformateur:
      "Un transformateur idéal a un rendement de 100% et aucune perte, tandis qu'un transformateur réel présente des pertes par effet Joule, hystérésis et courants de Foucault.",
    "dérivée":
      "La dérivée mesure le taux de variation instantané d'une fonction. Les règles principales incluent la dérivée d'une constante (0), la règle de puissance, et la règle de la chaîne.",
    "intégrale":
      "L'intégrale est l'opération inverse de la dérivée. Elle permet de calculer l'aire sous une courbe et de résoudre des problèmes de calcul infinitésimal.",
    "transistor":
      "Un transistor est un composant électronique semi-conducteur utilisé pour amplifier ou commuter des signaux électriques. Les types principaux sont BJT et FET.",
    "ph":
      "Le pH mesure l'acidité ou la basicité d'une solution. Il est défini comme le logarithme négatif de la concentration en ions H+."
  }

  const lowerMessage = message.toLowerCase()
  for (const [key, response] of Object.entries(responses)) {
    if (lowerMessage.includes(key)) {
      return `${response}\n\n*Note: Cette réponse utilise notre base de connaissances. Pour des réponses plus précises, assurez-vous que l'API backend est en cours d'exécution.*`
    }
  }

  return `Je comprends votre question sur "${message}". 

**Assistant IA Étudiant - Mode Fallback**

Actuellement, je fonctionne en mode de secours car l'API principale n'est pas accessible. Je peux vous aider avec des concepts de base dans plusieurs matières :

- **Électricité** : loi d'Ohm, théorème de Thévenin, circuits
- **Mathématiques** : dérivées, intégrales, fonctions
- **Physique** : lois de Newton, énergie, mouvement
- **Chimie** : pH, acides-bases, réactions
- **Électronique** : transistors, amplificateurs

Pour une assistance complète avec Ollama, veuillez :
1. Démarrer l'API backend : python api.py
2. Vérifier que Ollama est en cours d'exécution
3. Recharger cette page

Pouvez-vous reformuler votre question avec des termes plus spécifiques ?`
}
