"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { 
  FileText, 
  BookOpen, 
  ArrowLeft,
  Plus,
  Database,
  Brain,
  MessageSquare,
  Calendar,
  FileType,
  HardDrive,
  ExternalLink
} from "lucide-react"
import { apiService, SystemStatus, DocumentStats, DocumentOut } from "@/lib/api"

interface StudentDocument {
  id: string
  name: string
  type: string
  size: string
  uploadedAt: string
  status: 'active' | 'processing' | 'error'
  source: 'student' | 'backend'
}

export default function AllDocuments() {
  const router = useRouter()
  const [documents, setDocuments] = useState<DocumentOut[]>([])
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [documentStats, setDocumentStats] = useState<DocumentStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadAllDocuments()
  }, [])

  const loadAllDocuments = async () => {
    try {
      setIsLoading(true)
      
      // Load all data in parallel
      const [status, stats, documentsData] = await Promise.allSettled([
        apiService.getStatus(),
        apiService.getStats(),
        apiService.getAllDocuments()
      ])
      
      // Set the data if successful
      if (status.status === 'fulfilled') setSystemStatus(status.value)
      if (stats.status === 'fulfilled') setDocumentStats(stats.value)
      if (documentsData.status === 'fulfilled') setDocuments(documentsData.value)
      
    } catch (error) {
      console.error('Erreur lors du chargement des documents:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const startChatWithDocument = (docId: string) => {
    // Stocker le document sélectionné pour l'assistant RAG
    const selectedDoc = documents.find(d => d.id === docId)
    if (selectedDoc) {
      localStorage.setItem('selectedDocument', JSON.stringify(selectedDoc))
      router.push('/chat')
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }

  const getSourceColor = (source: StudentDocument['source']) => {
    return source === 'student' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
  }

  const getSourceText = (source: StudentDocument['source']) => {
    return source === 'student' ? 'Personnel' : 'Cours'
  }

  if (isLoading) {
    return (
      <div className="min-h-dvh flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-foreground/60">Chargement des documents...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-dvh pt-24">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="w-full px-10 md:px-16 py-5 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button 
              onClick={() => router.push('/student')}
              variant="ghost"
              size="sm"
              className="p-2"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div className="p-3 bg-gradient-to-r from-primary to-secondary rounded-xl shadow-lg">
              <Database className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Tous mes Documents</h1>
              <p className="text-foreground/60">Cours officiels + vos ressources personnelles</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {documents.length}
              </div>
              <div className="text-sm text-foreground/60">Total Documents</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <BookOpen className="w-6 h-6 text-secondary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {documents.filter(d => d.source === 'student').length}
              </div>
              <div className="text-sm text-foreground/60">Vos Documents</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <Database className="w-6 h-6 text-accent" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {documents.filter(d => d.source === 'backend').length}
              </div>
              <div className="text-sm text-foreground/60">Cours Officiels</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3">
                <Brain className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {systemStatus?.documents_loaded ? 'Actif' : 'En attente'}
              </div>
              <div className="text-sm text-foreground/60">Assistant RAG</div>
            </div>
          </Card>
        </div>

        {/* Liste des documents */}
        {documents.length === 0 ? (
          <Card className="p-12 rounded-xl border bg-card shadow-sm text-center">
            <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <FileText className="w-10 h-10 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-3">Aucun document disponible</h3>
            <p className="text-foreground/60 mb-6 max-w-md mx-auto">
              Commencez par importer vos premiers documents ou attendez que les cours soient chargés.
            </p>
            <Button 
              onClick={() => router.push('/my-documents')}
            >
              <Plus className="w-4 h-4 mr-2" />
              Importer des Documents
            </Button>
          </Card>
        ) : (
          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              Documents Disponibles ({documents.length})
            </h3>
            
            <div className="space-y-3">
              {documents.map((doc) => (
                <div key={doc.id} className="flex items-center justify-between p-4 bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                  <div className="flex items-center gap-4 flex-1">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      doc.source === 'student' ? 'bg-secondary/10' : 'bg-primary/10'
                    }`}>
                      <FileText className={`w-5 h-5 ${
                        doc.source === 'student' ? 'text-secondary' : 'text-primary'
                      }`} />
                    </div>
                    
                    <div className="flex-1">
                      <div className="font-medium text-foreground">{doc.name}</div>
                      <div className="text-sm text-foreground/60 flex items-center gap-4">
                        <span className="flex items-center gap-1">
                          <FileType className="w-3 h-3" />
                          {doc.type}
                        </span>
                        <span className="flex items-center gap-1">
                          <HardDrive className="w-3 h-3" />
                          {doc.size}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {formatDate(doc.uploaded_at)}
                        </span>
                        {doc.subject && (
                          <span className="flex items-center gap-1">
                            <BookOpen className="w-3 h-3" />
                            {doc.subject}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      doc.source === 'student' ? 'bg-secondary/10 text-secondary' : 'bg-primary/10 text-primary'
                    }`}>
                      {getSourceText(doc.source)}
                    </span>
                    
                    <Button
                      onClick={() => startChatWithDocument(doc.id)}
                      size="sm"
                    >
                      <MessageSquare className="w-4 h-4 mr-2" />
                      Interroger
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Actions */}
        <div className="flex justify-center gap-4 mt-8">
          <Button 
            onClick={() => router.push('/student')}
            variant="outline"
            className="px-6 py-3"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'Espace Étudiant
          </Button>
          
          <Button 
            onClick={() => router.push('/chat')}
            variant="secondary"
            className="px-6 py-3"
          >
            <Brain className="w-4 h-4 mr-2" />
            Tester l'Assistant RAG
          </Button>
        </div>
      </main>
    </div>
  )
}
