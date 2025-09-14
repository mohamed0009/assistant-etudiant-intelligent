"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { apiService, DocumentOut } from "@/lib/api"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { 
  FileText, 
  BookOpen, 
  ArrowLeft,
  Plus,
  Trash2,
  Download,
  Eye,
  Calendar,
  FileType,
  HardDrive,
  Database,
  Brain
} from "lucide-react"

interface StudentDocument {
  id: string
  name: string
  type: string
  size: string
  uploadedAt: string
  status: 'active' | 'processing' | 'error'
}

export default function MyDocuments() {
  const router = useRouter()
  const [documents, setDocuments] = useState<DocumentOut[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [adminDocs, setAdminDocs] = useState<Array<{ filename: string; size: number; modified: number }>>([])
  const [isImportOpen, setIsImportOpen] = useState(false)
  const [studentId, setStudentId] = useState<number>(1)

  useEffect(() => {
    loadDocuments()
    loadAdminDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      setIsLoading(true)
      
      // Get current user to fetch their data
      const storedUser = localStorage.getItem('user')
      const userData = storedUser ? JSON.parse(storedUser) : null
      
      // Create or get student record
      let currentStudentId = 1 // Default fallback
      if (userData) {
        try {
          const student = await apiService.createStudent({
            name: userData.name || 'Étudiant',
            email: userData.email || 'student@example.com',
            role: 'student'
          })
          currentStudentId = student.id
          setStudentId(currentStudentId)
        } catch (error) {
          console.log('Student already exists or error creating:', error)
        }
      }
      
      // Load student documents from API
      const studentDocs = await apiService.getStudentDocuments(currentStudentId)
      setDocuments(studentDocs)
      
    } catch (error) {
      console.error('Erreur lors du chargement des documents:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadAdminDocuments = async () => {
    try {
      const res = await apiService.listAdminDocuments()
      setAdminDocs(res.documents || [])
    } catch (e) {
      // ignore for now (keeps personal docs functional)
    }
  }

  const deleteDocument = (id: string) => {
    const updatedDocs = documents.filter(doc => doc.id !== id)
    setDocuments(updatedDocs)
    localStorage.setItem('studentDocuments', JSON.stringify(updatedDocs))
    
    // Mettre à jour les statistiques globales
    updateGlobalStats(-1)
  }

  const updateGlobalStats = (change: number) => {
    const currentStats = JSON.parse(localStorage.getItem('documentStats') || '{}')
    const newStats = {
      ...currentStats,
      total_documents: Math.max(0, (currentStats.total_documents || 0) + change),
      last_updated: new Date().toISOString()
    }
    localStorage.setItem('documentStats', JSON.stringify(newStats))
    
    // Déclencher un événement pour notifier les autres composants
    window.dispatchEvent(new CustomEvent('documentsUpdated', { detail: newStats }))
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusColor = (status: StudentDocument['status']) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-blue-100 text-blue-800'
      case 'error':
        return 'bg-red-100 text-red-800'
    }
  }

  const getStatusText = (status: StudentDocument['status']) => {
    switch (status) {
      case 'active':
        return 'Actif'
      case 'processing':
        return 'En traitement'
      case 'error':
        return 'Erreur'
    }
  }

  const getExtFromName = (name: string) => {
    const i = name.lastIndexOf('.')
    return i >= 0 ? name.slice(i + 1).toLowerCase() : 'fichier'
  }

  const humanSize = (bytes: number) => {
    if (!bytes || bytes < 1024) return `${bytes} B`
    const kb = bytes / 1024
    if (kb < 1024) return `${kb.toFixed(1)} KB`
    const mb = kb / 1024
    return `${mb.toFixed(1)} MB`
  }

  const addPersonalDocuments = async (files: FileList | null) => {
    if (!files || files.length === 0) return
    setIsLoading(true)
    try {
      const fileArray = Array.from(files)
      // Upload each file to backend (admin storage) as well
      await Promise.allSettled(fileArray.map((f) => apiService.uploadAdminDocument(f)))
      // Create local personal entries
      const newDocs: StudentDocument[] = fileArray.map((f, idx) => ({
        id: `${Date.now()}_${idx}`,
        name: f.name,
        type: getExtFromName(f.name).toUpperCase(),
        size: humanSize(f.size),
        uploadedAt: new Date().toISOString(),
        status: 'active',
      }))
      const updated = [...newDocs, ...documents]
      setDocuments(updated)
      localStorage.setItem('studentDocuments', JSON.stringify(updated))
      updateGlobalStats(newDocs.length)
      // Refresh backend docs list to reflect uploads
      await loadAdminDocuments()
      setIsImportOpen(false)
    } catch (e) {
      // Keep local entries even if backend upload fails
      setIsImportOpen(false)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-dvh pt-24 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-foreground/70">Chargement des documents...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-dvh pt-24">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button 
                onClick={() => router.push('/student')}
                variant="ghost"
                size="sm"
                className="p-2"
              >
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div className="p-3 bg-primary rounded-xl shadow-lg">
                <BookOpen className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Mes Documents</h1>
                <p className="text-foreground/70">Vos ressources personnelles</p>
              </div>
            </div>
            <Dialog open={isImportOpen} onOpenChange={setIsImportOpen}>
              <DialogTrigger asChild>
                <Button>
              <Plus className="w-4 h-4 mr-2" />
              Importer des Documents
            </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Importer des documents personnels</DialogTitle>
                </DialogHeader>
                <div className="space-y-3">
                  <input
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    multiple
                    onChange={(e) => addPersonalDocuments(e.target.files)}
                    className="block w-full text-sm"
                  />
                  <p className="text-xs text-foreground/60">Formats supportés: PDF, DOC, DOCX, TXT</p>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={() => setIsImportOpen(false)}>Fermer</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {documents.length + adminDocs.length}
              </div>
              <div className="text-sm text-foreground/70">Total Documents</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <BookOpen className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {documents.filter(d => d.status === 'active').length}
              </div>
              <div className="text-sm text-foreground/70">Documents Actifs</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <FileType className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {new Set([
                  ...documents.map(d => d.type.toLowerCase()),
                  ...adminDocs.map(d => getExtFromName(d.filename))
                ]).size}
              </div>
              <div className="text-sm text-foreground/70">Types de Fichiers</div>
            </div>
          </Card>

          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 bg-primary/10">
                <Calendar className="w-6 h-6 text-primary" />
              </div>
              <div className="text-2xl font-bold text-foreground">
                {(() => {
                  const personal = documents.length > 0 ? new Date(documents[0].uploadedAt).getTime() : 0
                  const backend = adminDocs.length > 0 ? Math.max(...adminDocs.map(d => d.modified * 1000)) : 0
                  const latest = Math.max(personal, backend)
                  return latest ? new Date(latest).toLocaleDateString('fr-FR') : 'Aucun'
                })()}
              </div>
              <div className="text-sm text-foreground/70">Dernier Ajout</div>
            </div>
          </Card>
        </div>

        {/* Liste des documents */}
        {documents.length === 0 ? (
          <Card className="p-12 rounded-xl border bg-card shadow-sm text-center">
            <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <FileText className="w-10 h-10 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-3">Aucun document importé</h3>
            <p className="text-foreground/70 mb-6 max-w-md mx-auto">
              Vous n'avez pas encore de documents personnels. Les documents de cours sont disponibles dans "Tous mes Documents".
            </p>
            <Button onClick={() => router.push('/all-documents')}>
              <Database className="w-4 h-4 mr-2" />
              Voir Tous les Documents
            </Button>
          </Card>
        ) : (
          <Card className="p-6 rounded-xl border bg-card shadow-sm">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              Documents Importés ({documents.length})
            </h3>
            
            <div className="space-y-3">
              {documents.map((doc) => (
                <div key={doc.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted transition-colors">
                  <div className="flex items-center gap-4 flex-1">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                      <FileText className="w-5 h-5 text-primary" />
                    </div>
                    
                    <div className="flex-1">
                      <div className="font-medium text-foreground">{doc.name}</div>
                      <div className="text-sm text-foreground/70 flex items-center gap-4">
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
                          {formatDate(doc.uploadedAt)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(doc.status)}`}>
                      {getStatusText(doc.status)}
                    </span>
                    
                    <div className="flex gap-2">
                      <Button variant="ghost" size="sm" title="Voir le document">
                        <Eye className="w-4 h-4" />
                      </Button>
                      
                      <Button variant="ghost" size="sm" title="Télécharger">
                        <Download className="w-4 h-4" />
                      </Button>
                      
                      <Button
                        onClick={() => deleteDocument(doc.id)}
                        variant="ghost"
                        size="sm"
                        title="Supprimer"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Documents de cours (backend) */}
        {adminDocs.length > 0 && (
          <Card className="p-6 rounded-xl border bg-card shadow-sm mt-8">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              Documents de Cours ({adminDocs.length})
            </h3>
            <div className="space-y-3">
              {adminDocs.map((d) => (
                <div key={d.filename} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg grid place-items-center">
                      <FileText className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium text-foreground">{d.filename}</div>
                      <div className="text-sm text-foreground/70">
                        {getExtFromName(d.filename)} • {(d.size / 1024).toFixed(1)} KB • {new Date(d.modified * 1000).toLocaleDateString('fr-FR')}
                      </div>
                    </div>
                  </div>
                  <div className="text-sm text-foreground/60">Lecture seule</div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Actions */}
        <div className="flex justify-center gap-4 mt-8">
          <Button onClick={() => router.push('/student')} variant="outline" className="px-6 py-3">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'Espace Étudiant
          </Button>
          
          <Button onClick={() => router.push('/all-documents')} className="px-6 py-3">
            <Database className="w-4 h-4 mr-2" />
            Voir Tous les Documents
          </Button>
          
          <Button onClick={() => router.push('/chat')} variant="secondary" className="px-6 py-3">
            <Brain className="w-4 h-4 mr-2" />
            Tester l'Assistant RAG
          </Button>
        </div>
      </main>
    </div>
  )
}
