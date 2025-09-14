"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  BarChart3, 
  Clock, 
  Users, 
  TrendingUp, 
  Activity,
  Brain,
  FileText,
  Zap,
  RefreshCw
} from "lucide-react"

interface PerformanceMetrics {
  total_questions: number
  average_response_time: number
  total_users: number
  questions_today: number
  most_asked_subjects: Record<string, number>
  response_time_trend: number[]
  confidence_trend: number[]
  documents_usage: Record<string, number>
  precomputed_vs_documents: Record<string, number>
}

interface RecentQuestion {
  question: string
  response_time: number
  confidence: number
  question_type: string
  subject?: string
  timestamp: string
  user_id: string
  sources_used: number
}

export function PerformanceDashboard() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [recentQuestions, setRecentQuestions] = useState<RecentQuestion[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  const fetchMetrics = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/metrics')
      if (response.ok) {
        const data = await response.json()
        setMetrics(data)
      }
    } catch (error) {
      console.error('Erreur lors du chargement des métriques:', error)
    }
  }

  const fetchRecentQuestions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/metrics/recent?limit=10')
      if (response.ok) {
        const data = await response.json()
        setRecentQuestions(data)
      }
    } catch (error) {
      console.error('Erreur lors du chargement des questions récentes:', error)
    }
  }

  const refreshData = async () => {
    setLoading(true)
    await Promise.all([fetchMetrics(), fetchRecentQuestions()])
    setLastUpdate(new Date())
    setLoading(false)
  }

  useEffect(() => {
    refreshData()
    
    // Actualisation automatique toutes les 30 secondes
    const interval = setInterval(refreshData, 30000)
    return () => clearInterval(interval)
  }, [])

  const formatTime = (seconds: number) => {
    if (seconds < 1) return `${(seconds * 1000).toFixed(0)}ms`
    return `${seconds.toFixed(2)}s`
  }

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(1)}%`
  }

  const getSubjectColor = (subject: string) => {
    const colors: Record<string, string> = {
      'mathematics': 'bg-blue-100 text-blue-800',
      'physics': 'bg-purple-100 text-purple-800',
      'chemistry': 'bg-green-100 text-green-800',
      'electronics': 'bg-orange-100 text-orange-800',
      'biology': 'bg-pink-100 text-pink-800',
      'geology': 'bg-yellow-100 text-yellow-800',
      'astronomy': 'bg-indigo-100 text-indigo-800',
      'psychology': 'bg-red-100 text-red-800',
      'computer_science': 'bg-gray-100 text-gray-800'
    }
    return colors[subject] || 'bg-gray-100 text-gray-800'
  }

  if (loading && !metrics) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin" />
        <span className="ml-2">Chargement des métriques...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* En-tête avec bouton de rafraîchissement */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Dashboard de Performance</h2>
          <p className="text-gray-600">
            Dernière mise à jour: {lastUpdate.toLocaleTimeString()}
          </p>
        </div>
        <Button onClick={refreshData} disabled={loading} variant="outline">
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Actualiser
        </Button>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Questions Total</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.total_questions || 0}</div>
            <p className="text-xs text-muted-foreground">
              +{metrics?.questions_today || 0} aujourd'hui
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Temps de Réponse</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatTime(metrics?.average_response_time || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Moyenne globale
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Utilisateurs Actifs</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.total_users || 0}</div>
            <p className="text-xs text-muted-foreground">
              Utilisateurs uniques
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Confiance Moyenne</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatConfidence(
                metrics?.confidence_trend?.reduce((a, b) => a + b, 0) / 
                (metrics?.confidence_trend?.length || 1) || 0
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              Dernières réponses
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Onglets pour les détails */}
      <Tabs defaultValue="subjects" className="space-y-4">
        <TabsList>
          <TabsTrigger value="subjects">Matières</TabsTrigger>
          <TabsTrigger value="recent">Questions Récentes</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="subjects" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Matières les Plus Consultées</CardTitle>
              <CardDescription>
                Répartition des questions par matière
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(metrics?.most_asked_subjects || {})
                  .sort(([,a], [,b]) => b - a)
                  .map(([subject, count]) => (
                    <div key={subject} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Badge className={getSubjectColor(subject)}>
                          {subject}
                        </Badge>
                      </div>
                      <div className="text-sm font-medium">{count} questions</div>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="recent" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Questions Récentes</CardTitle>
              <CardDescription>
                Les 10 dernières questions posées
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentQuestions.map((question, index) => (
                  <div key={index} className="border rounded-lg p-3">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-medium line-clamp-2">
                          {question.question}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          {question.subject && (
                            <Badge className={getSubjectColor(question.subject)}>
                              {question.subject}
                            </Badge>
                          )}
                          <Badge variant="outline">
                            {question.question_type}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-right text-xs text-gray-500 ml-4">
                        <div>{formatTime(question.response_time)}</div>
                        <div>{formatConfidence(question.confidence)}</div>
                        <div>{new Date(question.timestamp).toLocaleTimeString()}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Types de Réponses</CardTitle>
                <CardDescription>
                  Répartition pré-calculé vs documents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(metrics?.precomputed_vs_documents || {}).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {type === 'precomputed' ? (
                          <Zap className="h-4 w-4 text-yellow-500" />
                        ) : (
                          <FileText className="h-4 w-4 text-blue-500" />
                        )}
                        <span className="text-sm capitalize">{type}</span>
                      </div>
                      <span className="text-sm font-medium">{count}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tendances de Performance</CardTitle>
                <CardDescription>
                  Évolution des temps de réponse
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Temps moyen récent</span>
                    <span className="text-sm font-medium">
                      {formatTime(
                        metrics?.response_time_trend?.reduce((a, b) => a + b, 0) / 
                        (metrics?.response_time_trend?.length || 1) || 0
                      )}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Confiance récente</span>
                    <span className="text-sm font-medium">
                      {formatConfidence(
                        metrics?.confidence_trend?.reduce((a, b) => a + b, 0) / 
                        (metrics?.confidence_trend?.length || 1) || 0
                      )}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

