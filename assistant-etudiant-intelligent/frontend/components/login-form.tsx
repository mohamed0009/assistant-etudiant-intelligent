"use client"

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

import { useRouter } from 'next/navigation'
import { Eye, EyeOff, Lock, Mail, GraduationCap, Loader2, BrainCircuit, Sparkles } from 'lucide-react'


type LoginFormProps = {
  compact?: boolean
}

export function LoginForm({ compact = false }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [mounted, setMounted] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setMounted(true)
  }, [])

  // Fonction d'authentification locale temporaire
  const localLogin = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    
    // Simulation simple
    await new Promise(resolve => setTimeout(resolve, 300))
    
    if (email === 'admin@univ.fr' && password === 'admin123') {
      const user = {
        id: '1',
        email: 'admin@univ.fr',
        name: 'Administrateur',
        role: 'admin'
      }
      localStorage.setItem('user', JSON.stringify(user))
      setIsLoading(false)
      return true
    } else if (email === 'etudiant@univ.fr' && password === 'etudiant123') {
      const user = {
        id: '2',
        email: 'etudiant@univ.fr',
        name: 'Étudiant',
        role: 'student'
      }
      localStorage.setItem('user', JSON.stringify(user))
      setIsLoading(false)
      return true
    } else {
      setIsLoading(false)
      return false
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Veuillez remplir tous les champs')
      return
    }

    try {
      console.log('Tentative de connexion avec:', { email, password })
      const success = await localLogin(email, password)
      console.log('Résultat de la connexion:', success)
      
      if (success) {
        console.log('Connexion réussie, redirection...')
        // Redirection selon le rôle
        if (email === 'admin@univ.fr') {
          router.push('/admin')
        } else {
          router.push('/student')
        }
      } else {
        setError('Identifiants invalides')
      }
    } catch (error) {
      console.error('Erreur lors de la connexion:', error)
      setError('Erreur de connexion')
    }
  }

  if (compact) {
    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-1.5">
          <label htmlFor="email" className="text-xs font-medium text-foreground/80 flex items-center gap-2">
            <Mail className="w-3.5 h-3.5" />
            Adresse email
          </label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="votre.email@univ.fr"
            className="h-10 bg-white/90 border-border focus:border-primary focus:ring-primary/20"
            required
          />
        </div>

        <div className="space-y-1.5">
          <label htmlFor="password" className="text-xs font-medium text-foreground/80 flex items-center gap-2">
            <Lock className="w-3.5 h-3.5" />
            Mot de passe
          </label>
          <div className="relative">
            <Input
              id="password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Votre mot de passe"
              className="h-10 bg-white/90 border-border focus:border-primary focus:ring-primary/20 pr-10"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-2.5 top-1/2 transform -translate-y-1/2 text-foreground/40 hover:text-foreground/70"
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {error && (
          <div className="p-2 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
            {error}
          </div>
        )}

        <Button
          type="submit"
          disabled={isLoading}
          className="w-full h-10 bg-primary text-primary-foreground hover:opacity-90"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin mr-2" />
          ) : (
            <Lock className="w-4 h-4 mr-2" />
          )}
          {isLoading ? 'Connexion...' : 'Se connecter'}
        </Button>
      </form>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-cyan-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <GraduationCap className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent mb-2">
            Assistant Étudiant Intelligent
          </h1>
          <p className="text-gray-600">
            Connectez-vous pour accéder à votre espace
          </p>
        </div>

        <Card className="p-8 bg-white/80 backdrop-blur-sm border border-border shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium text-foreground/80 flex items-center gap-2">
                <Mail className="w-4 h-4" />
                Adresse email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre.email@univ.fr"
                className="h-12 bg-white/90 border-border focus:border-primary focus:ring-primary/20"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium text-foreground/80 flex items-center gap-2">
                <Lock className="w-4 h-4" />
                Mot de passe
              </label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Votre mot de passe"
                  className="h-12 bg-white/90 border-border focus:border-primary focus:ring-primary/20 pr-12"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-foreground/40 hover:text-foreground/70"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full h-12 bg-primary text-primary-foreground hover:opacity-90 shadow-lg"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin mr-2" />
              ) : (
                <Lock className="w-5 h-5 mr-2" />
              )}
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  )
}
