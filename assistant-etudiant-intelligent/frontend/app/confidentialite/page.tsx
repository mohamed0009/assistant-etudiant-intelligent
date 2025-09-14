"use client"

import Link from "next/link"
import { useEffect, useState } from "react"

export default function ConfidentialitePage() {
  const [user, setUser] = useState<any>(null)
  useEffect(() => {
    const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null
    setUser(storedUser ? JSON.parse(storedUser) : null)
  }, [])
  return (
    <div className="space-y-10">
      <header className="w-full border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg grid place-items-center bg-primary text-primary-foreground font-bold">AI</div>
            <div>
              <div className="text-base font-semibold leading-tight">Assistant Étudiant Intelligent</div>
              <div className="text-xs text-foreground/60 leading-tight">Université de Technologie</div>
            </div>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm text-foreground/70">
            <Link href="/">Accueil</Link>
            <Link href={user ? "/chat" : "/#login"} title={user ? undefined : "Connectez-vous pour accéder"}>Chat</Link>
            <Link href={user ? "/all-documents" : "/#login"} title={user ? undefined : "Connectez-vous pour accéder"}>Documents</Link>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">Confidentialité</h1>
        <p className="text-foreground/70 mb-8 max-w-3xl">Votre confidentialité est essentielle. Cette page explique comment nous traitons vos données et sécurisons vos informations.</p>

        <div className="grid gap-6">
          <section className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Collecte des données</h2>
            <p className="text-sm text-foreground/70">Nous collectons uniquement les informations nécessaires au bon fonctionnement de l'assistant (questions posées, métriques d'usage anonymisées). Vos documents restent dans votre environnement.</p>
          </section>
          <section className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Utilisation</h2>
            <p className="text-sm text-foreground/70">Les données sont utilisées pour améliorer la qualité des réponses et fournir des statistiques d'apprentissage. Aucune donnée n'est vendue ni partagée à des tiers.</p>
          </section>
          <section className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Sécurité</h2>
            <p className="text-sm text-foreground/70">Nous appliquons des contrôles d'accès et des bonnes pratiques de sécurité pour protéger vos informations.</p>
          </section>
        </div>

        <div className="pt-8 text-sm text-foreground/70">
          <Link href="/conditions" className="underline hover:no-underline mr-4">Conditions d'utilisation</Link>
          <Link href="/contact" className="underline hover:no-underline mr-4">Contact</Link>
          <Link href="/a-propos" className="underline hover:no-underline">À propos</Link>
        </div>
      </main>
    </div>
  )
}


