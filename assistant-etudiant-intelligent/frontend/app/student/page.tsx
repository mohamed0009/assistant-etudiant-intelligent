"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

import { useRouter } from "next/navigation"
import { 
  GraduationCap, 
  Brain, 
  BookOpen, 
  MessageSquare, 
  LogOut,
  User,
  Clock,
  TrendingUp,
  ArrowRight,
  Sparkles,
  Zap,
  Target,
  Award,
  Database,
  FileText,
  Plus
} from "lucide-react"
import { apiService, SystemStatus, DocumentStats, SubjectOut, StudentUsageStats } from "@/lib/api"
import { getSubjectColor, getSubjectIconColor } from "@/lib/mock-data"

export default function StudentDashboard() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [documentStats, setDocumentStats] = useState<DocumentStats | null>(null)
  const [subjects, setSubjects] = useState<SubjectOut[]>([])
  const [usageStats, setUsageStats] = useState<StudentUsageStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'documents' | 'analytics'>('overview')

  useEffect(() => {
    // Vérifier l'utilisateur connecté
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const userData = JSON.parse(storedUser)
      setUser(userData)
      
      if (userData.role !== 'student') {
        router.push('/')
        return
      }
      
      loadData()
    } else {
      router.push('/')
    }

    // Écouter les mises à jour des documents
    const handleDocumentsUpdated = (event: CustomEvent<any>) => {
      const newStats = event.detail
      setDocumentStats(prev => ({
        total_documents: newStats?.total_documents ?? prev?.total_documents ?? 0,
        total_chunks: newStats?.total_chunks ?? prev?.total_chunks ?? 0,
        subjects: newStats?.subjects ?? prev?.subjects ?? []
      }))
    }

    window.addEventListener('documentsUpdated', handleDocumentsUpdated as EventListener)

    return () => {
      window.removeEventListener('documentsUpdated', handleDocumentsUpdated as EventListener)
    }
  }, [router])

  const loadData = async () => {
    try {
      setIsLoading(true)
      
      // Get current user to fetch their data
      const storedUser = localStorage.getItem('user')
      const userData = storedUser ? JSON.parse(storedUser) : null
      
      // Create or get student record
      let studentId = 1 // Default fallback
      if (userData) {
        try {
          const student = await apiService.createStudent({
            name: userData.name || 'Étudiant',
            email: userData.email || 'student@example.com',
            role: 'student'
          })
          studentId = student.id
        } catch (error) {
          console.log('Student already exists or error creating:', error)
        }
      }
      
      // Load all data in parallel
      const [status, stats, subjectsData, usageStatsData] = await Promise.allSettled([
        apiService.getStatus(),
        apiService.getStats(),
        apiService.getStudentSubjects(),
        apiService.getStudentUsageStats(studentId)
      ])
      
      // Set the data if successful
      if (status.status === 'fulfilled') setSystemStatus(status.value)
      if (stats.status === 'fulfilled') setDocumentStats(stats.value)
      if (subjectsData.status === 'fulfilled') setSubjects(subjectsData.value)
      if (usageStatsData.status === 'fulfilled') setUsageStats(usageStatsData.value)
      
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('user')
    router.push('/')
  }

  const startChat = () => {
    router.push('/chat')
  }

  if (user?.role !== 'student') {
    return null
  }

  return (
    <div className="min-h-dvh pt-24">
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-7xl mx-auto px-6 py-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 rounded-xl bg-primary text-primary-foreground">
            <GraduationCap className="h-6 w-6" />
          </div>
          <div>
                <h1 className="text-2xl font-bold text-foreground">Espace Étudiant</h1>
            <p className="text-foreground/70">Bienvenue, {user.name}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-foreground/70">Étudiant</span>
          <Button onClick={handleLogout} variant="outline" size="sm">
            <LogOut className="w-4 h-4 mr-2" />
            Déconnexion
          </Button>
        </div>
      </div>
        </div>
        <nav className="bg-white/60 backdrop-blur-sm border-t">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex space-x-8">
              {[
                { id: 'overview', label: "Vue d'ensemble", icon: Target },
                { id: 'documents', label: 'Documents', icon: FileText },
                { id: 'analytics', label: 'Analytiques', icon: TrendingUp },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary text-primary'
                      : 'border-transparent text-foreground/60 hover:text-foreground hover:border-border'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </nav>
      </header>

      <div className="max-w-7xl mx-auto px-4 space-y-8 mt-14">
        {activeTab === 'overview' && (
        <>
        {/* Section d'accueil */}
        <div className="text-center mb-8">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-3">
            Votre Assistant IA Personnel
          </h2>
          <p className="text-foreground/70 max-w-3xl mx-auto">
            Accédez instantanément à l'assistant RAG pour poser vos questions sur vos cours, 
            obtenir de l'aide sur vos exercices et approfondir vos connaissances.
          </p>
        </div>

        {/* Carte principale - Assistant IA */}
        <Card className="p-8 bg-primary text-primary-foreground shadow-sm mb-8">
          <div className="text-center">
            <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <Brain className="w-10 h-10" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Assistant Étudiant Intelligent</h3>
            <p className="opacity-90 mb-8 max-w-2xl mx-auto">
              Posez vos questions sur vos cours, TD et examens. L'assistant utilise la technologie RAG 
              pour vous donner des réponses précises basées sur vos documents de cours.
            </p>
            <Button 
              onClick={startChat}
              size="lg"
              className="bg-background text-foreground hover:bg-foreground/5 px-8 py-4 text-lg font-semibold"
            >
              <MessageSquare className="w-5 h-5 mr-2" />
              Commencer une Conversation
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </Card>

        {/* Actions rapides */}
        <Card className="p-6 mb-8">
          <div className="text-center">
            <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 bg-primary/10">
              <MessageSquare className="w-8 h-8 text-primary" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Actions Rapides</h3>
            <p className="text-foreground/70 mb-6 max-w-2xl mx-auto">Démarrez une conversation ou accédez rapidement à vos documents.</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button 
                onClick={startChat}
                className="px-6 py-3"
              >
                <MessageSquare className="w-5 h-5 mr-2" />
                Nouvelle conversation
              </Button>
              <Button 
                variant="outline"
                onClick={() => router.push('/all-documents')}
                className="px-6 py-3"
              >
                <Database className="w-5 h-5 mr-2" />
                Tous mes Documents
              </Button>
              <Button variant="outline" onClick={() => router.push('/my-documents')} className="px-6 py-3">
                <BookOpen className="w-5 h-5 mr-2" />
                Mes Documents
              </Button>
            </div>
          </div>
        </Card>

        {/* Statistiques et statut */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <BookOpen className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-blue-900">
                {(() => {
                  const storedDocs = JSON.parse(localStorage.getItem('studentDocuments') || '[]')
                  const backendDocs = documentStats?.total_documents || 0
                  return storedDocs.length + backendDocs
                })()}
              </div>
              <div className="text-sm text-foreground/70">Documents Disponibles</div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <Database className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-green-900">
                {systemStatus?.total_vectors || 0}
              </div>
              <div className="text-sm text-foreground/70">Vecteurs Indexés</div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-purple-900">
                {systemStatus?.documents_loaded ? 'Actif' : 'En attente'}
              </div>
              <div className="text-sm text-foreground/70">Statut du Système</div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <TrendingUp className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-orange-900">
                {(() => {
                  const storedDocs = JSON.parse(localStorage.getItem('studentDocuments') || '[]')
                  return storedDocs.length
                })()}
              </div>
              <div className="text-sm text-foreground/70">Vos Ressources</div>
            </div>
          </Card>
        </div>

        {/* Fonctionnalités */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <Card className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-primary" />
              Fonctionnalités Principales
            </h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-sm text-slate-700">Questions sur vos cours et TD</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-sm text-slate-700">Explications détaillées avec sources</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-sm text-slate-700">Aide aux exercices et problèmes</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Sparkles className="w-4 h-4 text-primary" />
                <span className="text-sm text-slate-700">Réponses personnalisées par matière</span>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
              <Award className="w-5 h-5 text-primary" />
              Conseils d'Utilisation
            </h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                <span className="text-sm text-slate-700">Soyez précis dans vos questions pour des réponses optimales</span>
              </div>
              <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                <span className="text-sm text-slate-700">Utilisez les filtres par matière pour des réponses ciblées</span>
              </div>
              <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                <span className="text-sm text-slate-700">Consultez les sources pour approfondir vos connaissances</span>
              </div>
              <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                <span className="text-sm text-slate-700">L'assistant s'améliore avec l'ajout de nouveaux documents</span>
              </div>
            </div>
          </Card>
        </div>

        </>
        )}

        {activeTab === 'documents' && (
          <>
            <Card className="p-6 mb-8">
              <div className="text-center">
                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 bg-primary/10">
                  <Database className="w-8 h-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Vos Documents et Ressources</h3>
                <p className="text-foreground/70 mb-6 max-w-2xl mx-auto">Consultez tous vos documents disponibles, cours officiels et ressources personnelles.</p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button onClick={() => router.push('/all-documents')} className="px-6 py-3">
                    <Database className="w-5 h-5 mr-2" />
                    Tous mes Documents
            </Button>
                  <Button variant="outline" onClick={() => router.push('/my-documents')} className="px-6 py-3">
              <BookOpen className="w-5 h-5 mr-2" />
                    Mes Documents
            </Button>
              </div>
            </div>
          </Card>
          </>
        )}

        {activeTab === 'analytics' && (
          <>
        {/* Statistiques d'utilisation simulées */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-semibold text-slate-800 mb-6 text-center flex items-center justify-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            Statistiques d'Utilisation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{usageStats?.total_questions || 0}</div>
              <div className="text-sm text-slate-600">Questions posées</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{usageStats?.total_conversations || 0}</div>
              <div className="text-sm text-slate-600">Conversations</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{subjects.length}</div>
              <div className="text-sm text-slate-600">Matières disponibles</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold mb-2">{usageStats?.total_documents || 0}</div>
              <div className="text-sm text-slate-600">Documents personnels</div>
            </div>
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-slate-600 mb-2">Dernière activité : {usageStats?.last_activity || 'Aucune'}</p>
            {usageStats?.favorite_subjects && usageStats.favorite_subjects.length > 0 && (
              <>
                <p className="text-sm text-slate-600 mb-2">Matières préférées :</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {usageStats.favorite_subjects.map((subject, index) => (
                    <span key={index} className="px-3 py-1 bg-muted rounded-full text-xs font-medium">
                      {subject}
                    </span>
                  ))}
                </div>
              </>
            )}
          </div>
        </Card>

        {/* Informations système et profil */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <Card className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
              <Clock className="w-5 h-5 text-primary" />
              Informations Système
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Dernière mise à jour</span>
                <span className="text-sm font-medium">
                  {documentStats?.last_updated ? new Date(documentStats.last_updated).toLocaleString('fr-FR') : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Documents chargés</span>
                <span className="text-sm font-medium">
                  {systemStatus?.documents_loaded ? 'Oui' : 'Non'}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Total vecteurs</span>
                <span className="text-sm font-medium">
                  {systemStatus?.total_vectors || 0}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Statut API</span>
                <span className="text-sm font-medium">
                  {systemStatus ? 'Connecté' : 'Déconnecté'}
                </span>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
              <User className="w-5 h-5 text-primary" />
              Votre Profil Étudiant
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Nom</span>
                <span className="text-sm font-medium">{user?.name || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Email</span>
                <span className="text-sm font-medium">{user?.email || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Rôle</span>
                <span className="text-sm font-medium">Étudiant</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                <span className="text-sm text-slate-700">Documents personnels</span>
                <span className="text-sm font-medium text-emerald-600">
                  {(() => {
                    const storedDocs = JSON.parse(localStorage.getItem('studentDocuments') || '[]')
                    return storedDocs.length
                  })()}
                </span>
              </div>
            </div>
          </Card>
        </div>

        {/* Matières populaires */}
        <Card className="p-6 mb-8">
          <h3 className="text-xl font-semibold text-slate-800 mb-6 text-center flex items-center justify-center gap-2">
            <BookOpen className="w-5 h-5 text-primary" />
            Matières les Plus Consultées
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {subjects.slice(0, 6).map((subject) => (
              <div key={subject.id} className={`text-center p-4 ${getSubjectColor(subject.color)} rounded-lg`}>
                <div className={`text-2xl font-bold ${getSubjectIconColor(subject.color)} mb-2`}>
                  {subject.name}
                </div>
                <div className="text-sm text-slate-600">{subject.questions_count} questions</div>
                <div className="text-xs text-slate-500 mt-1">{subject.description}</div>
                <div className="mt-2 text-xs font-medium text-slate-600">
                  {subject.documents_count} documents
                </div>
              </div>
            ))}
          </div>
        </Card>
          </>
        )}

        

        

        

        {/* Informations supplémentaires */}
        <div className="mt-8 text-center text-sm text-slate-500">
          <p>
            L'assistant est disponible 24h/24 et 7j/7. 
            Pour des questions techniques, contactez l'administrateur.
          </p>
        </div>
      </div>
    </div>
  )
}
