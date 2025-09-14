"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ChevronDown, ChevronUp, BookOpen, MessageSquare, FileText, Brain } from "lucide-react"

export function QuickStartGuide() {
  const [isExpanded, setIsExpanded] = useState(false)

  const steps = [
    {
      icon: <BookOpen className="w-5 h-5" />,
      title: "1. Connectez-vous",
      description: "Utilisez les comptes de test pour accéder au système",
      details: "Admin: admin@univ.fr / admin123 | Étudiant: etudiant@univ.fr / etudiant123"
    },
    {
      icon: <FileText className="w-5 h-5" />,
      title: "2. Consultez vos documents",
      description: "Accédez à vos cours, TD et examens corrigés",
      details: "Tous vos documents sont automatiquement indexés et disponibles pour l'assistant"
    },
    {
      icon: <MessageSquare className="w-5 h-5" />,
      title: "3. Posez vos questions",
      description: "Chattez avec l'assistant IA pour obtenir des réponses",
      details: "L'assistant utilise vos documents pour fournir des réponses précises et pédagogiques"
    },
    {
      icon: <Brain className="w-5 h-5" />,
      title: "4. Explorez les fonctionnalités",
      description: "Découvrez le tableau de bord, les statistiques et plus",
      details: "Suivez votre progression et explorez toutes les capacités de l'assistant"
    }
  ]

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-primary" />
              Guide de démarrage rapide
            </CardTitle>
            <CardDescription>
              Découvrez comment utiliser l'assistant en 4 étapes simples
            </CardDescription>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="w-4 h-4" />
                Réduire
              </>
            ) : (
              <>
                <ChevronDown className="w-4 h-4" />
                Voir les étapes
              </>
            )}
          </Button>
        </div>
      </CardHeader>
      
      {isExpanded && (
        <CardContent className="space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="flex items-start gap-4 p-4 rounded-lg border bg-muted/30">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                {step.icon}
              </div>
              <div className="flex-1 space-y-2">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{step.title}</h3>
                  <Badge variant="secondary" className="text-xs">
                    Étape {index + 1}
                  </Badge>
                </div>
                <p className="text-sm text-foreground/80">{step.description}</p>
                <p className="text-xs text-foreground/60 bg-background/50 p-2 rounded border">
                  {step.details}
                </p>
              </div>
            </div>
          ))}
          
          <div className="mt-6 p-4 bg-primary/5 rounded-lg border border-primary/20">
            <h4 className="font-semibold text-primary mb-2">💡 Conseil</h4>
            <p className="text-sm text-foreground/80">
              L'assistant fonctionne mieux avec des questions spécifiques. Essayez des questions comme 
              "Explique-moi la loi d'Ohm" ou "Qu'est-ce que le théorème de Thévenin ?"
            </p>
          </div>
        </CardContent>
      )}
    </Card>
  )
}
