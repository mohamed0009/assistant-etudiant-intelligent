"use client"

import Link from "next/link"
import { useEffect, useState } from "react"

export default function AProposPage() {
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
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">À propos</h1>
        <p className="text-foreground/70 mb-8 max-w-3xl">Notre mission est d'aider les étudiants à apprendre plus vite et mieux grâce à une IA pédagogique s'appuyant sur leurs propres documents.</p>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Technologie</h2>
            <p className="text-sm text-foreground/70">RAG (Retrieval-Augmented Generation), base vectorielle FAISS et interface moderne (Next.js + Tailwind).</p>
          </div>
          <div className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Approche pédagogique</h2>
            <p className="text-sm text-foreground/70">Explications complètes, exemples concrets, et transparence des sources utilisées.</p>
          </div>
          <div className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Engagement</h2>
            <p className="text-sm text-foreground/70">Respect de la vie privée, sécurité des données et amélioration continue.</p>
          </div>
        </div>

        <div className="pt-8 text-sm text-foreground/70">
          <Link href="/confidentialite" className="underline hover:no-underline mr-4">Confidentialité</Link>
          <Link href="/conditions" className="underline hover:no-underline mr-4">Conditions</Link>
          <Link href="/contact" className="underline hover:no-underline">Contact</Link>
        </div>
      </main>
    </div>
  )
}


