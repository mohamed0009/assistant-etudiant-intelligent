"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/hooks/use-auth'

export function TestAuth() {
  const [result, setResult] = useState<string>('')
  const { login, user, logout } = useAuth()

  const testAdminLogin = async () => {
    try {
      setResult('Test de connexion admin...')
      const success = await login('admin@univ.fr', 'admin123')
      setResult(success ? '✅ Connexion admin réussie!' : '❌ Échec connexion admin')
    } catch (error) {
      setResult(`❌ Erreur: ${error}`)
    }
  }

  const testStudentLogin = async () => {
    try {
      setResult('Test de connexion étudiant...')
      const success = await login('etudiant@univ.fr', 'etudiant123')
      setResult(success ? '✅ Connexion étudiant réussie!' : '❌ Échec connexion étudiant')
    } catch (error) {
      setResult(`❌ Erreur: ${error}`)
    }
  }

  const testLogout = () => {
    logout()
    setResult('✅ Déconnexion réussie!')
  }

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h3 className="font-bold mb-4">Test d'Authentification</h3>
      
      <div className="space-y-2 mb-4">
        <Button onClick={testAdminLogin} size="sm">
          Test Admin
        </Button>
        <Button onClick={testStudentLogin} size="sm" variant="outline">
          Test Étudiant
        </Button>
        <Button onClick={testLogout} size="sm" variant="destructive">
          Déconnexion
        </Button>
      </div>
      
      <div className="text-sm">
        <p><strong>Résultat:</strong> {result}</p>
        <p><strong>Utilisateur actuel:</strong> {user ? `${user.name} (${user.role})` : 'Aucun'}</p>
      </div>
    </div>
  )
}

