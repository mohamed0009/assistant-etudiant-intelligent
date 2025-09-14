"use client"

import { LoginForm } from "@/components/login-form"
import { RegisterForm } from "@/components/register-form"
import { QuickStartGuide } from "@/components/quick-start-guide"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { Loader2, CheckCircle2 } from "lucide-react"
import Link from "next/link"

export default function Home() {
  const [user, setUser] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showRegister, setShowRegister] = useState(false)
  const router = useRouter()

  useEffect(() => {
    // Vérifier si un utilisateur est connecté
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const userData = JSON.parse(storedUser)
      setUser(userData)
      
      // Redirection automatique selon le rôle
      if (userData.role === 'admin') {
        router.push('/admin')
      } else {
        router.push('/student')
      }
    }
    setIsLoading(false)
  }, [router])

  if (isLoading) {
    return (
      <div className="min-h-dvh grid place-items-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    )
  }

  if (user) {
    return (
      <div className="min-h-dvh grid place-items-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-4" />
          <p className="text-foreground/70">Redirection...</p>
        </div>
      </div>
    )
  }
  return (
    <div className="space-y-10 pt-20">
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="w-full px-10 md:px-16 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg grid place-items-center bg-primary text-primary-foreground font-bold">
              AI
            </div>
            <div>
              <div className="text-base font-semibold leading-tight">Assistant Étudiant Intelligent</div>
              <div className="text-xs text-foreground/60 leading-tight">Université de Technologie</div>
            </div>
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm text-foreground/70">
            <Link href={user ? (user.role === 'admin' ? "/admin" : "/student") : "#login"} className="hover:text-foreground" title={user ? undefined : "Connectez-vous pour accéder"}>Tableau de bord</Link>
            <Link href={user ? "/chat" : "#login"} className="hover:text-foreground" title={user ? undefined : "Connectez-vous pour accéder"}>Chat</Link>
            <Link href={user ? "/all-documents" : "#login"} className="hover:text-foreground" title={user ? undefined : "Connectez-vous pour accéder"}>Documents</Link>
          </nav>
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-foreground/70">
              <span className="h-2 w-2 rounded-full bg-green-500" /> Prêt
            </span>
          </div>
        </div>
      </header>

      <div className="max-w-14xl mx-auto px-4 grid lg:grid-cols-2 gap-24 lg:gap-40 xl:gap-48 items-center">
        <div className="space-y-5 md:space-y-6 ml-6 md:ml-12 lg:ml-16 xl:ml-24 2xl:ml-28">
          <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-foreground/70">
            <span className="h-2 w-2 rounded-full bg-primary" /> IA universitaire
          </div>
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">
            Assistant Étudiant Intelligent
          </h1>
          <p className="text-foreground/70 text-base md:text-lg max-w-xl">
            Obtenez des réponses fiables basées sur vos cours et documents. Un assistant clair, pédagogique et rapide pour réussir vos études.
          </p>
          <ul className="grid gap-2.5">
            <li className="flex items-center gap-2 text-foreground/80">
              <CheckCircle2 className="h-4 w-4 text-primary" /> Réponses basées sur vos documents
            </li>
            <li className="flex items-center gap-2 text-foreground/80">
              <CheckCircle2 className="h-4 w-4 text-primary" /> Tableau de bord de progression
            </li>
            <li className="flex items-center gap-2 text-foreground/80">
              <CheckCircle2 className="h-4 w-4 text-primary" /> Sécurité et interface moderne
            </li>
          </ul>
          <div className="flex items-center gap-3 pt-2">
            <a 
              href="#login" 
              className="inline-flex items-center justify-center rounded-md bg-primary text-primary-foreground px-6 py-3 text-sm font-medium hover:bg-primary/90 transition-colors shadow-sm"
              onClick={(e) => {
                e.preventDefault()
                document.getElementById('login')?.scrollIntoView({ behavior: 'smooth' })
              }}
            >
              Découvrir l'assistant
            </a>
          </div>
        </div>
        <div className="w-full justify-self-center relative">
          <div className="pointer-events-none absolute -inset-6 md:-inset-8 rounded-3xl bg-primary/5 blur-2xl" />
          <div id="login" className="relative rounded-xl border bg-card p-6 shadow-sm w-80 md:w-96 mx-auto flex flex-col">
            <h2 className="text-lg md:text-xl font-semibold mb-3 md:mb-4">
              {showRegister ? "Créer un compte" : "Connexion"}
            </h2>
            <div className="flex-1 overflow-auto">
              {showRegister ? (
                <RegisterForm compact />
              ) : (
                <LoginForm compact />
              )}
            </div>
            <div className="mt-2 text-[10px] md:text-xs text-foreground/60 flex items-center gap-2 justify-between">
              <div className="flex items-center gap-2">
                {!showRegister ? (
                  <>
                    <a href="#" className="hover:text-foreground">Mot de passe oublié ?</a>
                    <span aria-hidden>·</span>
                    <button
                      onClick={() => setShowRegister(true)}
                      className="hover:text-foreground transition-colors"
                    >
                      Créer un compte
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => setShowRegister(false)}
                    className="hover:text-foreground transition-colors"
                  >
                    Se connecter
                  </button>
                )}
              </div>
              <a href="#" className="hover:text-foreground">Confidentialité</a>
            </div>
          </div>
        </div>
      </div>

      {/* Guide de démarrage rapide */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="max-w-4xl mx-auto mb-8">
          <QuickStartGuide />
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-4">
          <div className="rounded-xl border bg-card p-5">
            <div className="text-sm font-semibold mb-1">Réponses fiables</div>
            <p className="text-sm text-foreground/70">Générées à partir de vos cours, TD et examens pour un apprentissage contextualisé.</p>
          </div>
          <div className="rounded-xl border bg-card p-5">
            <div className="text-sm font-semibold mb-1">Interface moderne</div>
            <p className="text-sm text-foreground/70">Expérience claire et fluide, pensée pour les étudiants pressés.</p>
          </div>
          <div className="rounded-xl border bg-card p-5">
            <div className="text-sm font-semibold mb-1">Suivi de progression</div>
            <p className="text-sm text-foreground/70">Tableau de bord synthétique pour visualiser votre avancée.</p>
          </div>
        </div>
      </section>
    </div>
  )
}

