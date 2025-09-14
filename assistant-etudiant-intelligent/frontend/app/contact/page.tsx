"use client"

import Link from "next/link"
import { useEffect, useState } from "react"

export default function ContactPage() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [message, setMessage] = useState("")
  const [sent, setSent] = useState(false)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const storedUser = typeof window !== 'undefined' ? localStorage.getItem('user') : null
    setUser(storedUser ? JSON.parse(storedUser) : null)
  }, [])

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    setSent(true)
    setTimeout(() => setSent(false), 2500)
  }

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
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">Contact</h1>
        <p className="text-foreground/70 mb-8 max-w-3xl">Une question, une suggestion, un partenariat ? Envoyez-nous un message.</p>

        <div className="grid md:grid-cols-2 gap-6">
          <form onSubmit={submit} className="rounded-xl border bg-card p-6 space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground/80">Nom</label>
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Votre nom" className="mt-1 w-full h-11 rounded-md border border-border bg-white/90 px-3 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary" />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground/80">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="votre.email@univ.fr" className="mt-1 w-full h-11 rounded-md border border-border bg-white/90 px-3 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary" />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground/80">Message</label>
              <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={6} placeholder="Votre message..." className="mt-1 w-full rounded-md border border-border bg-white/90 p-3 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary" />
            </div>
            <button type="submit" className="h-11 rounded-md bg-primary text-primary-foreground px-5 font-medium hover:opacity-90">
              Envoyer
            </button>
            {sent && <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-md p-2">Message envoyé (demo)</div>}
          </form>

          <div className="rounded-xl border bg-card p-6">
            <h2 className="text-lg font-semibold mb-2">Informations</h2>
            <p className="text-sm text-foreground/70 mb-4">Nous répondons généralement sous 48h ouvrées.</p>
            <div className="text-sm text-foreground/80 space-y-2">
              <p><span className="font-medium">Email :</span> support@univ.fr</p>
              <p><span className="font-medium">Adresse :</span> 123 Avenue des Sciences, 75000 Paris</p>
            </div>
          </div>
        </div>

        <div className="pt-8 text-sm text-foreground/70">
          <Link href="/confidentialite" className="underline hover:no-underline mr-4">Confidentialité</Link>
          <Link href="/conditions" className="underline hover:no-underline mr-4">Conditions</Link>
          <Link href="/a-propos" className="underline hover:no-underline">À propos</Link>
        </div>
      </main>
    </div>
  )
}


