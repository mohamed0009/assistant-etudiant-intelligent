"use client"

import { useState, useEffect, createContext, useContext } from 'react'

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'student'
  avatar?: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    
    // Simulation simple
    await new Promise(resolve => setTimeout(resolve, 300))
    
    let newUser: User | null = null
    
    if (email === 'admin@univ.fr' && password === 'admin123') {
      newUser = {
        id: '1',
        email: 'admin@univ.fr',
        name: 'Administrateur',
        role: 'admin',
        avatar: '/admin-avatar.png'
      }
    } else if (email === 'etudiant@univ.fr' && password === 'etudiant123') {
      newUser = {
        id: '2',
        email: 'etudiant@univ.fr',
        name: 'Étudiant',
        role: 'student',
        avatar: '/student-avatar.png'
      }
    }
    
    if (newUser) {
      setUser(newUser)
      localStorage.setItem('user', JSON.stringify(newUser))
      setIsLoading(false)
      return true
    } else {
      setIsLoading(false)
      return false
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      login,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  )
}
