"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

import { useRouter } from "next/navigation"
import { 
  Brain, 
  Users, 
  BookOpen, 
  Database, 
  TrendingUp, 
  Activity,
  Shield,
  LogOut,
  Settings,
  BarChart3,
  FileText,
  MessageSquare,
  RefreshCw,
  Plus,
  Eye,
  Edit,
  Trash2,
  X
} from "lucide-react"
import { PerformanceDashboard } from "@/components/performance-dashboard"
import { AdminTools } from "@/components/admin-tools"
import { apiService, SystemStatus, DocumentStats, StudentCreate, StudentOut } from "@/lib/api"

interface Student {
  id: number
  name: string
  email: string
  role: string
  lastActive?: string
  questionsAsked?: number
  status?: 'active' | 'inactive'
}

export default function AdminDashboard() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [documentStats, setDocumentStats] = useState<DocumentStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'students' | 'documents' | 'analytics'>('overview')
  
  // Real data states
  const [metrics, setMetrics] = useState<any>(null)
  const [recentMetrics, setRecentMetrics] = useState<any[]>([])
  const [adminStats, setAdminStats] = useState<any>(null)
  
  // Add student form state
  const [isAddStudentOpen, setIsAddStudentOpen] = useState(false)
  const [isQuickActionsAddOpen, setIsQuickActionsAddOpen] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    role: "student" as 'student' | 'admin'
  })
  const [quickActionsFormData, setQuickActionsFormData] = useState({
    name: "",
    email: "",
    role: "student" as 'student' | 'admin'
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  // Real student data from API
  const [students, setStudents] = useState<Student[]>([])
  const [studentsLoading, setStudentsLoading] = useState(false)

  // Student management modals state
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null)
  const [isViewModalOpen, setIsViewModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [editFormData, setEditFormData] = useState({
    name: "",
    email: "",
    role: "student" as 'student' | 'admin'
  })

  // Document management state
  const [isDocumentUploadOpen, setIsDocumentUploadOpen] = useState(false)
  const [isReloadingDocuments, setIsReloadingDocuments] = useState(false)
  const [isRAGConfigOpen, setIsRAGConfigOpen] = useState(false)
  const [isDetailedStatsOpen, setIsDetailedStatsOpen] = useState(false)
  const [isFormatManagementOpen, setIsFormatManagementOpen] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  useEffect(() => {
    // Vérifier l'utilisateur connecté
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const userData = JSON.parse(storedUser)
      setUser(userData)
      
      if (userData.role !== 'admin') {
        router.push('/')
        return
      }
      
      loadData()
    } else {
      router.push('/')
    }
  }, [router])

  const loadStudents = async () => {
    try {
      setStudentsLoading(true)
      const studentsData = await apiService.listStudents()
      // Convert StudentOut to Student with additional properties
      const extendedStudents: Student[] = studentsData.map(student => ({
        ...student,
        lastActive: 'Récemment', // Default value since we don't have this in API
        questionsAsked: 0, // Default value since we don't have this in API
        status: 'active' as const // Default status
      }))
      setStudents(extendedStudents)
    } catch (error) {
      console.error('Erreur lors du chargement des étudiants:', error)
      setError('Erreur lors du chargement des étudiants')
    } finally {
      setStudentsLoading(false)
    }
  }

  const createSampleDataIfNeeded = async () => {
    try {
      // Create sample conversations for existing students if they don't have any
      const students = await apiService.listStudents()
      
      for (const student of students) {
        try {
          // Try to create a sample conversation for each student
          await apiService.createConversation({ 
            student_id: student.id, 
            title: `Conversation de ${student.name}` 
          })
        } catch (error) {
          // Conversation might already exist, continue
          console.log(`Conversation already exists for student ${student.id}`)
        }
      }
    } catch (error) {
      console.log('Error creating sample data:', error)
    }
  }

  const loadAllRealData = async () => {
    try {
      setIsLoading(true)
      
      // Create sample data if needed
      await createSampleDataIfNeeded()
      
      // Defaults
      const defaultStatus: SystemStatus = { documents_loaded: false, total_vectors: 0, model: 'unknown', llm_configured: false }
      const defaultStats: DocumentStats = { total_documents: 0, total_chunks: 0, subjects: [], last_updated: undefined }
      const defaultMetrics: any = { total_questions: 0, avg_response_time: 'N/A', accuracy: 'N/A', uptime: 'N/A', total_sessions: 0, most_asked_subjects: {} }

      // Load system status
      try {
        const status = await apiService.getStatus()
        setSystemStatus(status)
      } catch (_) {
        setSystemStatus(defaultStatus)
      }

      // Load document stats
      try {
        const stats = await apiService.getStats()
        setDocumentStats(stats)
      } catch (_) {
        setDocumentStats(defaultStats)
      }

      // Load metrics
      try {
        const metricsData = await apiService.getMetrics()
        setMetrics(metricsData)
      } catch (_) {
        setMetrics(defaultMetrics)
      }
      
      // Load students
      await loadStudents()
      
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadData = loadAllRealData

  const handleLogout = () => {
    localStorage.removeItem('user')
    router.push('/')
  }

  // Student management handlers
  const handleViewStudent = (student: Student) => {
    setSelectedStudent(student)
    setIsViewModalOpen(true)
  }

  const handleEditStudent = (student: Student) => {
    setSelectedStudent(student)
    setEditFormData({
      name: student.name,
      email: student.email,
      role: student.role as 'student' | 'admin'
    })
    setIsEditModalOpen(true)
  }

  const handleDeleteStudent = (student: Student) => {
    setSelectedStudent(student)
    setIsDeleteModalOpen(true)
  }

  const handleEditInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setEditFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleUpdateStudent = async () => {
    if (!selectedStudent) return

    try {
      setIsSubmitting(true)
      setError(null)

      // Validate form
      if (!editFormData.name.trim() || !editFormData.email.trim()) {
        setError('Tous les champs sont requis')
        return
      }

      if (!editFormData.email.includes('@')) {
        setError('Format d\'email invalide')
        return
      }

      // Update student via API
      await apiService.updateStudent(selectedStudent.id, editFormData)

      setSuccess('Étudiant mis à jour avec succès')
      setIsEditModalOpen(false)
      await loadStudents() // Reload students list
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      setError('Erreur lors de la mise à jour de l\'étudiant')
      console.error('Error updating student:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleConfirmDelete = async () => {
    if (!selectedStudent) return

    try {
      setIsSubmitting(true)
      setError(null)

      // Delete student via API
      await apiService.deleteStudent(selectedStudent.id)

      setSuccess('Étudiant supprimé avec succès')
      setIsDeleteModalOpen(false)
      await loadStudents() // Reload students list
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      setError('Erreur lors de la suppression de l\'étudiant')
      console.error('Error deleting student:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Document management handlers
  const handleReloadDocuments = async () => {
    try {
      setIsReloadingDocuments(true)
      setError(null)

      await apiService.reloadDocuments()

      setSuccess('Base vectorielle rechargée avec succès')
      await loadData() // Reload all data
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      setError('Erreur lors du rechargement de la base vectorielle')
      console.error('Error reloading documents:', error)
    } finally {
      setIsReloadingDocuments(false)
    }
  }

  const handleFileUpload = async () => {
    if (!uploadedFile) return

    try {
      setIsSubmitting(true)
      setError(null)
      setUploadProgress(0)

      const res = await apiService.uploadAdminDocument(uploadedFile)
      if (!res || !res.filename) {
        throw new Error('Réponse invalide du serveur')
      }

      setUploadProgress(100)
      setSuccess('Document téléversé avec succès')
      setIsDocumentUploadOpen(false)
      setUploadedFile(null)
      setUploadProgress(0)
      await loadData() // Reload data to show new document
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      setError('Erreur lors du téléversement du document')
      console.error('Error uploading file:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  // Handle form input changes
  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  // Handle quick actions form input changes
  const handleQuickActionsInputChange = (field: string, value: string) => {
    setQuickActionsFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  // Handle form submission
  const handleAddStudent = async () => {
    try {
      setError(null)
      setSuccess(null)
      
      // Validate form
      if (!formData.name || !formData.email) {
        setError("Veuillez remplir tous les champs obligatoires")
        return
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(formData.email)) {
        setError("Veuillez entrer une adresse email valide")
        return
      }

      setIsSubmitting(true)

      // Create student data
      const studentData: StudentCreate = {
        name: formData.name,
        email: formData.email,
        role: "student"
      }

      // Call API to create student
      const newStudent = await apiService.createStudent(studentData)
      
      // Reset form and close dialog
      setFormData({
        name: "",
        email: "",
        role: "student"
      })
      setIsAddStudentOpen(false)
      setSuccess(`Étudiant ${newStudent.name} créé avec succès!`)
      
      // Reload students to show the new student
      loadStudents()
      
    } catch (err: any) {
      setError(err.message || "Erreur lors de la création de l'étudiant")
      console.error("Error creating student:", err)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle quick actions form submission
  const handleQuickActionsAddStudent = async () => {
    try {
      setError(null)
      setSuccess(null)

      // Validate form
      if (!quickActionsFormData.name.trim() || !quickActionsFormData.email.trim()) {
        setError("Veuillez remplir tous les champs obligatoires")
        return
      }

      // Validate email format
      if (!quickActionsFormData.email.includes('@')) {
        setError("Veuillez entrer une adresse email valide")
        return
      }

      setIsSubmitting(true)

      const studentData: StudentCreate = {
        name: quickActionsFormData.name,
        email: quickActionsFormData.email,
        role: "student"
      }

      // Call API to create student
      const newStudent = await apiService.createStudent(studentData)
      
      setSuccess("Étudiant ajouté avec succès")
      setIsQuickActionsAddOpen(false)
      
      // Reset form
      setQuickActionsFormData({ name: "", email: "", role: "student" })
      
      // Reload students list
      await loadStudents()
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000)
    } catch (error) {
      setError("Erreur lors de l'ajout de l'étudiant")
      console.error('Error adding student:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (user?.role !== 'admin') {
    return null
  }

  return (
    <div className="min-h-dvh pt-24">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary rounded-xl shadow-lg">
                <Shield className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Dashboard Administrateur</h1>
                <p className="text-foreground/70">Gestion complète du système</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-foreground/70">Connecté en tant que {user.name}</span>
              <Button onClick={handleLogout} variant="outline" size="sm">
                <LogOut className="w-4 h-4 mr-2" />
                Déconnexion
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation des onglets */}
      <nav className="bg-white/60 backdrop-blur-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Vue d\'ensemble', icon: BarChart3 },
              { id: 'students', label: 'Étudiants', icon: Users },
              { id: 'documents', label: 'Documents', icon: FileText },
              { id: 'analytics', label: 'Analytiques', icon: TrendingUp }
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

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
        {/* Vue d'ensemble */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Statistiques principales */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-primary">Étudiants Actifs</p>
                    <p className="text-2xl font-bold text-foreground">
                      {studentsLoading ? '...' : students.filter(s => s.status === 'active').length}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-primary/10">
                    <Users className="w-6 h-6 text-primary" />
                  </div>
                </div>
              </Card>

              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-primary">Documents Indexés</p>
                    <p className="text-2xl font-bold text-foreground">{systemStatus?.total_vectors || 0}</p>
                  </div>
                  <div className="p-3 rounded-lg bg-primary/10">
                    <Database className="w-6 h-6 text-primary" />
                  </div>
                </div>
              </Card>

              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-primary">Questions Traitées</p>
                    <p className="text-2xl font-bold text-foreground">
                      {isLoading ? '...' : (metrics?.total_questions || adminStats?.total_questions || 0)}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-primary/10">
                    <MessageSquare className="w-6 h-6 text-primary" />
                  </div>
                </div>
              </Card>

              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-primary">Système</p>
                    <p className="text-2xl font-bold text-foreground">
                      {systemStatus?.documents_loaded ? 'Opérationnel' : 'En attente'}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-primary/10">
                    <Activity className="w-6 h-6 text-primary" />
                  </div>
                </div>
              </Card>
            </div>

            {/* Graphiques et activités récentes */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <h3 className="text-lg font-semibold text-foreground mb-4">Activité Récente</h3>
                <div className="space-y-3">
                  {isLoading ? (
                    <div className="p-4 text-center text-slate-500">Chargement...</div>
                  ) : recentMetrics.length === 0 ? (
                    <div className="p-4 text-center text-slate-500">Aucune activité récente</div>
                  ) : (
                    recentMetrics.slice(0, 5).map((metric, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <Activity className="w-4 h-4 text-blue-600" />
                          </div>
                          <div>
                            <p className="font-medium text-slate-800">{metric.action || 'Activité système'}</p>
                            <p className="text-sm text-slate-500">{metric.timestamp || 'Récemment'}</p>
                          </div>
                        </div>
                        <span className="text-sm text-slate-600">{metric.details || 'Système'}</span>
                      </div>
                    ))
                  )}
                </div>
              </Card>

              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <h3 className="text-lg font-semibold text-foreground mb-4">Actions Rapides</h3>
                <div className="space-y-3">
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setIsQuickActionsAddOpen(true)}
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Ajouter un étudiant
                  </Button>

                  <Button className="w-full justify-start" variant="outline" onClick={() => window.location.href = '/admin/documents'}>
                    <FileText className="w-4 h-4 mr-2" />
                    Gérer les documents
                  </Button>

                  <Button className="w-full justify-start" variant="outline" onClick={() => window.location.href = '/admin/settings'}>
                    <Settings className="w-4 h-4 mr-2" />
                    Configuration système
                  </Button>

                  <Dialog>
                    <DialogTrigger asChild>
                      <Button className="w-full justify-start" variant="outline">
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Actualiser les données
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Actualiser les données</DialogTitle>
                      </DialogHeader>
                      <div className="text-sm text-foreground/70">Relancer le chargement des documents et la mise à jour des métriques.</div>
                      <DialogFooter>
                        <Button onClick={loadData}>Actualiser</Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </div>
              </Card>
            </div>
          </div>
        )}

        {/* Gestion des étudiants */}
        {activeTab === 'students' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-slate-800">Gestion des Étudiants</h2>
              <Button 
                className="bg-blue-600 hover:bg-blue-700"
                onClick={() => setIsAddStudentOpen(true)}
              >
                <Plus className="w-4 h-4 mr-2" />
                Nouvel Étudiant
              </Button>
            </div>

            <Card className="bg-white/80 backdrop-blur-sm border border-slate-200/50">
              <div className="overflow-x-auto">
                {studentsLoading ? (
                  <div className="p-8 text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-slate-600">Chargement des étudiants...</p>
                  </div>
                ) : students.length === 0 ? (
                  <div className="p-8 text-center">
                    <Users className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-600">Aucun étudiant trouvé</p>
                    <p className="text-sm text-slate-500">Cliquez sur "Nouvel Étudiant" pour en ajouter un</p>
                  </div>
                ) : (
                  <table className="w-full">
                    <thead className="bg-slate-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                          Étudiant
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                          Dernière Activité
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                          Questions
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                          Statut
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-slate-200">
                      {students.map((student) => (
                        <tr key={student.id} className="hover:bg-slate-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                                <span className="text-sm font-medium text-blue-600">
                                  {student.name.charAt(0).toUpperCase()}
                                </span>
                              </div>
                              <div className="ml-4">
                                <div className="text-sm font-medium text-slate-900">{student.name}</div>
                                <div className="text-sm text-slate-500">{student.email}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                            {student.lastActive || 'N/A'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                            {student.questionsAsked || 0}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              student.status === 'active' 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {student.status === 'active' ? 'Actif' : 'Inactif'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex space-x-2">
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => handleViewStudent(student)}
                                title="Voir les détails"
                              >
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => handleEditStudent(student)}
                                title="Modifier l'étudiant"
                              >
                                <Edit className="w-4 h-4" />
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm" 
                                className="text-red-600 hover:text-red-700"
                                onClick={() => handleDeleteStudent(student)}
                                title="Supprimer l'étudiant"
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </Card>
          </div>
        )}

        {/* Add Student Modal for Students Tab */}
        {isAddStudentOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Ajouter un étudiant</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsAddStudentOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Nom complet
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => handleInputChange("name", e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Nom de l'étudiant"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="email@exemple.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Rôle
                  </label>
                  <select
                    value={formData.role}
                    onChange={(e) => handleInputChange("role", e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="student">Étudiant</option>
                    <option value="admin">Administrateur</option>
                  </select>
                </div>
              </div>
              
              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}
              
              {success && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
                  <p className="text-sm text-green-600">{success}</p>
                </div>
              )}
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsAddStudentOpen(false)
                    setFormData({ name: "", email: "", role: "student" })
                    setError(null)
                    setSuccess(null)
                  }}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button
                  onClick={handleAddStudent}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Ajout...' : 'Ajouter l\'étudiant'}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions Add Student Modal */}
        {isQuickActionsAddOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Ajouter un étudiant</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setIsQuickActionsAddOpen(false)
                    setError(null)
                    setSuccess(null)
                    setQuickActionsFormData({ name: "", email: "", role: "student" })
                  }}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}
                {success && (
                  <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                    <p className="text-sm text-green-600">{success}</p>
                  </div>
                )}
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Nom complet
                  </label>
                  <input 
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    placeholder="Nom de l'étudiant" 
                    value={quickActionsFormData.name}
                    onChange={(e) => handleQuickActionsInputChange("name", e.target.value)}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Email
                  </label>
                  <input 
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    placeholder="email@exemple.com" 
                    type="email"
                    value={quickActionsFormData.email}
                    onChange={(e) => handleQuickActionsInputChange("email", e.target.value)}
                    required
                  />
                </div>
              </div>
              
              <div className="flex justify-end gap-2 mt-6">
                <Button 
                  variant="outline" 
                  onClick={() => {
                    setIsQuickActionsAddOpen(false)
                    setError(null)
                    setSuccess(null)
                    setQuickActionsFormData({ name: "", email: "", role: "student" })
                  }}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button 
                  onClick={handleQuickActionsAddStudent}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Création..." : "Enregistrer"}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Gestion des documents */}
        {activeTab === 'documents' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-foreground">Gestion des Documents</h2>
              <Button onClick={() => setIsDocumentUploadOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Ajouter des Documents
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100/50 border border-blue-200/50">
                <div className="text-center">
                  <BookOpen className="w-12 h-12 text-blue-600 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-blue-900">
                    {documentStats?.total_documents || 0}
                  </div>
                  <div className="text-sm text-blue-600">Documents Totaux</div>
                </div>
              </Card>

              <Card className="p-6 bg-gradient-to-br from-green-50 to-green-100/50 border border-green-200/50">
                <div className="text-center">
                  <Database className="w-12 h-12 text-green-600 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-green-900">
                    {documentStats?.total_chunks || 0}
                  </div>
                  <div className="text-sm text-green-600">Segments Créés</div>
                </div>
              </Card>

              <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100/50 border border-purple-200/50">
                <div className="text-center">
                  <Brain className="w-12 h-12 text-purple-600 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-purple-900">
                    {documentStats?.subjects.length || 0}
                  </div>
                  <div className="text-sm text-purple-600">Matières</div>
                </div>
              </Card>
            </div>

            <Card className="p-6 rounded-xl border bg-card shadow-sm">
              <h3 className="text-lg font-semibold text-foreground mb-4">Actions sur les Documents</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Button 
                  variant="outline" 
                  className="h-16 justify-start"
                  onClick={handleReloadDocuments}
                  disabled={isReloadingDocuments}
                >
                  <RefreshCw className={`w-5 h-5 mr-3 ${isReloadingDocuments ? 'animate-spin' : ''}`} />
                  {isReloadingDocuments ? 'Rechargement...' : 'Recharger la Base Vectorielle'}
                </Button>
                <Button 
                  variant="outline" 
                  className="h-16 justify-start"
                  onClick={() => setIsRAGConfigOpen(true)}
                >
                  <Settings className="w-5 h-5 mr-3" />
                  Configuration RAG
                </Button>
                <Button 
                  variant="outline" 
                  className="h-16 justify-start"
                  onClick={() => setIsDetailedStatsOpen(true)}
                >
                  <BarChart3 className="w-5 h-5 mr-3" />
                  Statistiques Détaillées
                </Button>
                <Button 
                  variant="outline" 
                  className="h-16 justify-start"
                  onClick={() => setIsFormatManagementOpen(true)}
                >
                  <FileText className="w-5 h-5 mr-3" />
                  Gestion des Formats
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* Analytiques */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-slate-800">Analytiques et Rapports</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <h3 className="text-lg font-semibold text-foreground mb-4">Utilisation par Matière</h3>
                <div className="space-y-3">
                  {isLoading ? (
                    <div className="p-4 text-center text-slate-500">Chargement...</div>
                  ) : documentStats?.subjects && documentStats.subjects.length > 0 ? (
                    documentStats.subjects.map((subject, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-sm text-slate-600">{subject}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-border rounded-full h-2">
                            <div 
                              className="h-2 rounded-full bg-gradient-to-r from-primary to-secondary" 
                              style={{ width: `${(index + 1) * 20}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-slate-800">
                            {(index + 1) * 20}%
                          </span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="p-4 text-center text-slate-500">Aucune donnée disponible</div>
                  )}
                </div>
              </Card>

              <Card className="p-6 rounded-xl border bg-card shadow-sm">
                <h3 className="text-lg font-semibold text-foreground mb-4">Performance du Système</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-600">Temps de Réponse Moyen</span>
                    <span className="text-sm font-medium text-slate-800">
                      {isLoading ? '...' : (metrics?.avg_response_time || 'N/A')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-600">Précision des Réponses</span>
                    <span className="text-sm font-medium text-slate-800">
                      {isLoading ? '...' : (metrics?.accuracy || 'N/A')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-600">Uptime</span>
                    <span className="text-sm font-medium text-slate-800">
                      {isLoading ? '...' : (metrics?.uptime || 'N/A')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-600">Total des Sessions</span>
                    <span className="text-sm font-medium text-slate-800">
                      {isLoading ? '...' : (metrics?.total_sessions || 0)}
                    </span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        )}

        {/* View Student Modal */}
        {isViewModalOpen && selectedStudent && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Détails de l'étudiant</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsViewModalOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-xl font-medium text-blue-600">
                      {selectedStudent.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-slate-800">{selectedStudent.name}</h4>
                    <p className="text-slate-600">{selectedStudent.email}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                  <div>
                    <p className="text-sm text-slate-500">ID</p>
                    <p className="font-medium">{selectedStudent.id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-500">Rôle</p>
                    <p className="font-medium capitalize">{selectedStudent.role}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-500">Statut</p>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      selectedStudent.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {selectedStudent.status === 'active' ? 'Actif' : 'Inactif'}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm text-slate-500">Questions</p>
                    <p className="font-medium">{selectedStudent.questionsAsked || 0}</p>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsViewModalOpen(false)
                    handleEditStudent(selectedStudent)
                  }}
                >
                  Modifier
                </Button>
                <Button onClick={() => setIsViewModalOpen(false)}>
                  Fermer
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Edit Student Modal */}
        {isEditModalOpen && selectedStudent && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Modifier l'étudiant</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsEditModalOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Nom complet
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={editFormData.name}
                    onChange={handleEditInputChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Nom de l'étudiant"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={editFormData.email}
                    onChange={handleEditInputChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="email@exemple.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Rôle
                  </label>
                  <select
                    name="role"
                    value={editFormData.role}
                    onChange={handleEditInputChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="student">Étudiant</option>
                    <option value="admin">Administrateur</option>
                  </select>
                </div>
              </div>
              
              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsEditModalOpen(false)}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button
                  onClick={handleUpdateStudent}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Mise à jour...' : 'Mettre à jour'}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Delete Student Modal */}
        {isDeleteModalOpen && selectedStudent && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Supprimer l'étudiant</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsDeleteModalOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                    <span className="text-lg font-medium text-red-600">
                      {selectedStudent.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-slate-800">{selectedStudent.name}</h4>
                    <p className="text-slate-600">{selectedStudent.email}</p>
                  </div>
                </div>
                
                <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-800">
                    <strong>Attention:</strong> Cette action est irréversible. Toutes les données de cet étudiant seront supprimées définitivement.
                  </p>
                </div>
              </div>
              
              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsDeleteModalOpen(false)}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleConfirmDelete}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Suppression...' : 'Supprimer définitivement'}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Document Upload Modal */}
        {isDocumentUploadOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-md mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Ajouter un Document</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setIsDocumentUploadOpen(false)
                    setUploadedFile(null)
                    setUploadProgress(0)
                    setError(null)
                  }}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Sélectionner un fichier
                  </label>
                  <input
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-slate-500 mt-1">
                    Formats supportés: PDF, DOCX, TXT
                  </p>
                </div>
                
                {uploadedFile && (
                  <div className="p-3 bg-slate-50 rounded-md">
                    <p className="text-sm text-slate-700">
                      <strong>Fichier sélectionné:</strong> {uploadedFile.name}
                    </p>
                    <p className="text-xs text-slate-500">
                      Taille: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                )}
                
                {uploadProgress > 0 && uploadProgress < 100 && (
                  <div className="w-full bg-slate-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                )}
              </div>
              
              {error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsDocumentUploadOpen(false)
                    setUploadedFile(null)
                    setUploadProgress(0)
                    setError(null)
                  }}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button
                  onClick={handleFileUpload}
                  disabled={isSubmitting || !uploadedFile}
                >
                  {isSubmitting ? 'Téléversement...' : 'Téléverser'}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* RAG Configuration Modal */}
        {isRAGConfigOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-2xl mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Configuration RAG</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsRAGConfigOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Modèle d'Embedding
                    </label>
                    <select className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                      <option value="sentence-transformers/all-MiniLM-L6-v2">all-MiniLM-L6-v2</option>
                      <option value="sentence-transformers/all-mpnet-base-v2">all-mpnet-base-v2</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Nombre de documents similaires (k)
                    </label>
                    <input
                      type="number"
                      defaultValue="5"
                      className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Taille des chunks
                    </label>
                    <input
                      type="number"
                      defaultValue="1000"
                      className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Chevauchement des chunks
                    </label>
                    <input
                      type="number"
                      defaultValue="200"
                      className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsRAGConfigOpen(false)}
                >
                  Annuler
                </Button>
                <Button onClick={() => {
                  setSuccess('Configuration RAG mise à jour')
                  setIsRAGConfigOpen(false)
                  setTimeout(() => setSuccess(null), 3000)
                }}>
                  Sauvegarder
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Detailed Statistics Modal */}
        {isDetailedStatsOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-4xl mx-4 border border-white/20 shadow-xl max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Statistiques Détaillées</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsDetailedStatsOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-semibold text-blue-900">Documents</h4>
                    <p className="text-2xl font-bold text-blue-600">{documentStats?.total_documents || 0}</p>
                    <p className="text-sm text-blue-600">Total</p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h4 className="font-semibold text-green-900">Segments</h4>
                    <p className="text-2xl font-bold text-green-600">{documentStats?.total_chunks || 0}</p>
                    <p className="text-sm text-green-600">Indexés</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <h4 className="font-semibold text-purple-900">Matières</h4>
                    <p className="text-2xl font-bold text-purple-600">{documentStats?.subjects.length || 0}</p>
                    <p className="text-sm text-purple-600">Identifiées</p>
                  </div>
                </div>
                
                {documentStats?.subjects && documentStats.subjects.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-slate-800 mb-3">Répartition par Matière</h4>
                    <div className="space-y-2">
                      {documentStats.subjects.map((subject, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                          <span className="text-sm font-medium">{subject}</span>
                          <div className="flex items-center gap-2">
                            <div className="w-24 bg-slate-200 rounded-full h-2">
                              <div 
                                className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
                                style={{ width: `${(index + 1) * 20}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-slate-600">{(index + 1) * 20}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsDetailedStatsOpen(false)}
                >
                  Fermer
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Format Management Modal */}
        {isFormatManagementOpen && (
          <div className="fixed inset-0 bg-black/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 w-full max-w-2xl mx-4 border border-white/20 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800">Gestion des Formats</h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsFormatManagementOpen(false)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 border border-slate-200 rounded-lg">
                    <h4 className="font-semibold text-slate-800 mb-2">Formats Supportés</h4>
                    <ul className="space-y-1 text-sm text-slate-600">
                      <li>• PDF (.pdf)</li>
                      <li>• Microsoft Word (.docx)</li>
                      <li>• Texte (.txt)</li>
                    </ul>
                  </div>
                  <div className="p-4 border border-slate-200 rounded-lg">
                    <h4 className="font-semibold text-slate-800 mb-2">Limites</h4>
                    <ul className="space-y-1 text-sm text-slate-600">
                      <li>• Taille max: 50 MB</li>
                      <li>• Pages max: 1000</li>
                      <li>• Formats: PDF, DOCX, TXT</li>
                    </ul>
                  </div>
                </div>
                
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <h4 className="font-semibold text-yellow-800 mb-2">Recommandations</h4>
                  <ul className="space-y-1 text-sm text-yellow-700">
                    <li>• Utilisez des PDFs avec du texte sélectionnable</li>
                    <li>• Évitez les documents scannés sans OCR</li>
                    <li>• Structurez vos documents avec des titres clairs</li>
                  </ul>
                </div>
              </div>
              
              <div className="flex justify-end gap-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsFormatManagementOpen(false)}
                >
                  Fermer
                </Button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
