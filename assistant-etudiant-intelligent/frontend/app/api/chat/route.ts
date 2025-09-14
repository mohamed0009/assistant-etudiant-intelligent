import { type NextRequest, NextResponse } from "next/server"

// Simulation d'un système RAG simple
export async function POST(request: NextRequest) {
  try {
    const { message, documents } = await request.json()

    // Simulation de la recherche dans les documents
    const simulatedResponse = generateRAGResponse(message, documents)

    return NextResponse.json({
      response: simulatedResponse,
      sources: documents.length > 0 ? [documents[0].name] : [],
    })
  } catch (error) {
    return NextResponse.json({ error: "Erreur lors du traitement de la requête" }, { status: 500 })
  }
}

function generateRAGResponse(message: string, documents: any[]) {
  const responses = {
    "loi d'ohm":
      "La loi d'Ohm établit une relation entre la tension (U), l'intensité (I) et la résistance (R) : U = R × I. Cette loi fondamentale permet de calculer l'une de ces grandeurs connaissant les deux autres.",
    thévenin:
      "Le théorème de Thévenin permet de simplifier un circuit complexe en un générateur de tension équivalent en série avec une résistance. Cela facilite l'analyse des circuits électriques.",
    transformateur:
      "Un transformateur idéal a un rendement de 100% et aucune perte, tandis qu'un transformateur réel présente des pertes par effet Joule, hystérésis et courants de Foucault.",
  }

  const lowerMessage = message.toLowerCase()
  for (const [key, response] of Object.entries(responses)) {
    if (lowerMessage.includes(key)) {
      return `${response} ${documents.length > 0 ? "Cette information est basée sur vos documents téléchargés." : ""}`
    }
  }

  return `Je comprends votre question sur "${message}". ${documents.length > 0 ? "En me basant sur vos documents, " : ""}je peux vous aider à approfondir ce sujet. Pouvez-vous être plus spécifique ?`
}
