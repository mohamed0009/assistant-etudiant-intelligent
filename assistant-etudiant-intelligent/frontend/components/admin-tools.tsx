"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Settings, 
  Database, 
  Users, 
  Activity,
  Shield,
  Download,
  Upload,
  Trash2,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Clock
} from "lucide-react"

interface AdminStats {
  system_health: string
  documents_count: number
  active_users: number
  error_rate: number
  uptime: number
  last_backup: string | null
  performance_metrics: any
}

export function AdminTools() {
  const [adminStats, setAdminStats] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  const fetchAdminStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/admin/stats')
      if (response.ok) {
        const data = await response.json()
        setAdminStats(data)
      }
    } catch (error) {
      console.error('Erreur lors du chargement des stats admin:', error)
    }
  }

  const performAction = async (action: string, endpoint: string) => {
    setActionLoading(action)
    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: action === 'backup' ? 'POST' : 'GET'
      })
      
      if (response.ok) {
        const result = await response.json()
        alert(`Action ${action} réussie: ${result.message || 'OK'}`)
        await fetchAdminStats() // Rafraîchir les stats
      } else {
        throw new Error('Erreur lors de l\'action')
      }
    } catch (error) {
      alert(`Erreur lors de l'action ${action}: ${error}`)
    } finally {
      setActionLoading(null)
    }
  }

  const reloadDocuments = async () => {
    setActionLoading('reload')
    try {
      const response = await fetch('http://localhost:8000/api/reload', {
        method: 'POST'
      })
      
      if (response.ok) {
        const result = await response.json()
        alert(`Documents rechargés: ${result.message}`)
        await fetchAdminStats()
      } else {
        throw new Error('Erreur lors du rechargement')
      }
    } catch (error) {
      alert(`Erreur lors du rechargement: ${error}`)
    } finally {
      setActionLoading(null)
    }
  }

  useEffect(() => {
    fetchAdminStats()
    
    // Actualisation automatique toutes les 60 secondes
    const interval = setInterval(fetchAdminStats, 60000)
    return () => clearInterval(interval)
  }, [])

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy': return 'text-green-600'
      case 'degraded': return 'text-yellow-600'
      case 'error': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getHealthIcon = (health: string) => {
    switch (health) {
      case 'healthy': return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'degraded': return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'error': return <AlertTriangle className="h-5 w-5 text-red-600" />
      default: return <Activity className="h-5 w-5 text-gray-600" />
    }
  }

  if (loading && !adminStats) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin" />
        <span className="ml-2">Chargement des outils d'administration...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Outils d'Administration</h2>
          <p className="text-gray-600">
            Gestion et monitoring du système
          </p>
        </div>
        <Button onClick={fetchAdminStats} disabled={loading} variant="outline">
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Actualiser
        </Button>
      </div>

      {/* Statut système */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Statut Système</CardTitle>
            {getHealthIcon(adminStats?.system_health || 'unknown')}
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getHealthColor(adminStats?.system_health || 'unknown')}`}>
              {adminStats?.system_health || 'Unknown'}
            </div>
            <p className="text-xs text-muted-foreground">
              État général
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Documents</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{adminStats?.documents_count || 0}</div>
            <p className="text-xs text-muted-foreground">
              Fichiers chargés
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Utilisateurs Actifs</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{adminStats?.active_users || 0}</div>
            <p className="text-xs text-muted-foreground">
              Utilisateurs uniques
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Temps de Fonctionnement</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatUptime(adminStats?.uptime || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Depuis le démarrage
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Onglets d'administration */}
      <Tabs defaultValue="system" className="space-y-4">
        <TabsList>
          <TabsTrigger value="system">Système</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
          <TabsTrigger value="backup">Sauvegarde</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
        </TabsList>

        <TabsContent value="system" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Actions Système</CardTitle>
                <CardDescription>
                  Gestion du système et des services
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  onClick={reloadDocuments}
                  disabled={actionLoading === 'reload'}
                  className="w-full"
                  variant="outline"
                >
                  <RefreshCw className={`h-4 w-4 mr-2 ${actionLoading === 'reload' ? 'animate-spin' : ''}`} />
                  Recharger les Documents
                </Button>
                
                <Button 
                  onClick={() => performAction('health', '/api/health')}
                  disabled={actionLoading === 'health'}
                  className="w-full"
                  variant="outline"
                >
                  <Activity className="h-4 w-4 mr-2" />
                  Vérifier la Santé
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Statistiques Système</CardTitle>
                <CardDescription>
                  Métriques de performance
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm">Taux d'erreur</span>
                  <Badge variant={adminStats?.error_rate === 0 ? 'default' : 'destructive'}>
                    {(adminStats?.error_rate || 0).toFixed(2)}%
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Questions totales</span>
                  <span className="text-sm font-medium">
                    {adminStats?.performance_metrics?.total_questions || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Temps de réponse moyen</span>
                  <span className="text-sm font-medium">
                    {(adminStats?.performance_metrics?.average_response_time || 0).toFixed(3)}s
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="documents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Gestion des Documents</CardTitle>
              <CardDescription>
                Administration de la base de connaissances
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h4 className="font-medium">Actions Disponibles</h4>
                  <div className="space-y-2">
                    <Button 
                      onClick={reloadDocuments}
                      disabled={actionLoading === 'reload'}
                      className="w-full"
                      variant="outline"
                    >
                      <RefreshCw className={`h-4 w-4 mr-2 ${actionLoading === 'reload' ? 'animate-spin' : ''}`} />
                      Recharger Documents
                    </Button>
                    
                    <Button 
                      onClick={() => alert('Fonctionnalité à implémenter')}
                      className="w-full"
                      variant="outline"
                    >
                      <Upload className="h-4 w-4 mr-2" />
                      Ajouter Document
                    </Button>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h4 className="font-medium">Statistiques Documents</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Total documents:</span>
                      <span className="font-medium">{adminStats?.documents_count || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Chunks créés:</span>
                      <span className="font-medium">
                        {adminStats?.performance_metrics?.total_chunks || 0}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Matières couvertes:</span>
                      <span className="font-medium">
                        {Object.keys(adminStats?.performance_metrics?.subjects || {}).length}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="backup" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Sauvegarde et Restauration</CardTitle>
              <CardDescription>
                Gestion des sauvegardes du système
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <h4 className="font-medium">Actions de Sauvegarde</h4>
                  <Button 
                    onClick={() => performAction('backup', '/api/admin/backup')}
                    disabled={actionLoading === 'backup'}
                    className="w-full"
                  >
                    <Download className={`h-4 w-4 mr-2 ${actionLoading === 'backup' ? 'animate-spin' : ''}`} />
                    Créer Sauvegarde
                  </Button>
                  
                  <Button 
                    onClick={() => alert('Fonctionnalité à implémenter')}
                    className="w-full"
                    variant="outline"
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Restaurer Sauvegarde
                  </Button>
                </div>
                
                <div className="space-y-2">
                  <h4 className="font-medium">Informations Sauvegarde</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Dernière sauvegarde:</span>
                      <span className="font-medium">
                        {adminStats?.last_backup ? 
                          new Date(adminStats.last_backup).toLocaleString() : 
                          'Jamais'
                        }
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Statut:</span>
                      <Badge variant={adminStats?.last_backup ? 'default' : 'secondary'}>
                        {adminStats?.last_backup ? 'À jour' : 'Aucune'}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="monitoring" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Monitoring en Temps Réel</CardTitle>
                <CardDescription>
                  Surveillance des performances
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm">Statut API:</span>
                    <Badge variant="default">En ligne</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Moteur RAG:</span>
                    <Badge variant={adminStats?.system_health === 'healthy' ? 'default' : 'destructive'}>
                      {adminStats?.system_health === 'healthy' ? 'Actif' : 'Inactif'}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Base vectorielle:</span>
                    <Badge variant="default">Chargée</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Alertes Système</CardTitle>
                <CardDescription>
                  Notifications et alertes
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {adminStats?.error_rate > 0 ? (
                    <div className="flex items-center space-x-2 text-yellow-600">
                      <AlertTriangle className="h-4 w-4" />
                      <span className="text-sm">Taux d'erreur détecté</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2 text-green-600">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm">Système stable</span>
                    </div>
                  )}
                  
                  {adminStats?.documents_count === 0 && (
                    <div className="flex items-center space-x-2 text-red-600">
                      <AlertTriangle className="h-4 w-4" />
                      <span className="text-sm">Aucun document chargé</span>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

