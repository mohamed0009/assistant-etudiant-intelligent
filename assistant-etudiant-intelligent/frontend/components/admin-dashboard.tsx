"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Users,
  MessageSquare,
  Settings,
  LogOut,
  Bell,
  Shield,
  Database,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  Plus,
  Search,
  Edit,
  Trash2,
  UserCheck,
  UserX,
  Mail,
} from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import { apiService, StudentCreate, StudentOut } from "@/lib/api"

// Extended student interface for admin dashboard with additional properties
interface ExtendedStudent extends StudentOut {
  studentId?: string
  department?: string
  status?: 'active' | 'inactive'
  lastLogin?: string
  questionsAsked?: number
}

// Mock student data
const mockStudents = [
  {
    id: "1",
    name: "Marie Dupont",
    email: "marie.dupont@univ-tech.fr",
    studentId: "ET2024001",
    department: "Informatique",
    status: "active",
    lastLogin: "2024-01-15 14:30",
    questionsAsked: 45,
  },
  {
    id: "2",
    name: "Pierre Martin",
    email: "pierre.martin@univ-tech.fr",
    studentId: "ET2024002",
    department: "Électronique",
    status: "active",
    lastLogin: "2024-01-15 09:15",
    questionsAsked: 32,
  },
  {
    id: "3",
    name: "Sophie Bernard",
    email: "sophie.bernard@univ-tech.fr",
    studentId: "ET2024003",
    department: "Physique",
    status: "inactive",
    lastLogin: "2024-01-10 16:45",
    questionsAsked: 18,
  },
  {
    id: "4",
    name: "Lucas Moreau",
    email: "lucas.moreau@univ-tech.fr",
    studentId: "ET2024004",
    department: "Informatique",
    status: "active",
    lastLogin: "2024-01-15 11:20",
    questionsAsked: 67,
  },
]

export function AdminDashboard() {
  const [activeTab, setActiveTab] = useState("overview")
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedDepartment, setSelectedDepartment] = useState("all")
  const [isAddStudentOpen, setIsAddStudentOpen] = useState(false)
  const [students, setStudents] = useState<ExtendedStudent[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  
  // Form state for adding student
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    studentId: "",
    department: "",
  })
  
  const { user, logout } = useAuth()

  // Load students on component mount
  useEffect(() => {
    loadStudents()
  }, [])

  // Load students from API
  const loadStudents = async () => {
    try {
      setIsLoading(true)
      const studentsData = await apiService.listStudents()
      // Convert StudentOut to ExtendedStudent with default values
      const extendedStudents: ExtendedStudent[] = studentsData.map(student => ({
        ...student,
        studentId: `ET${student.id.toString().padStart(6, '0')}`,
        department: 'Informatique', // Default department
        status: 'active' as const,
        lastLogin: new Date().toLocaleString('fr-FR'),
        questionsAsked: 0
      }))
      setStudents(extendedStudents)
    } catch (err) {
      setError("Erreur lors du chargement des étudiants")
      console.error("Error loading students:", err)
    } finally {
      setIsLoading(false)
    }
  }

  // Handle form input changes
  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
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
      if (!formData.firstName || !formData.lastName || !formData.email) {
        setError("Veuillez remplir tous les champs obligatoires")
        return
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(formData.email)) {
        setError("Veuillez entrer une adresse email valide")
        return
      }

      setIsLoading(true)

      // Create student data
      const studentData: StudentCreate = {
        name: `${formData.firstName} ${formData.lastName}`,
        email: formData.email,
        role: "student"
      }

      // Call API to create student
      const newStudent = await apiService.createStudent(studentData)
      
      // Convert to ExtendedStudent and add to local state
      const extendedNewStudent: ExtendedStudent = {
        ...newStudent,
        studentId: formData.studentId || `ET${newStudent.id.toString().padStart(6, '0')}`,
        department: formData.department || 'Informatique',
        status: 'active' as const,
        lastLogin: new Date().toLocaleString('fr-FR'),
        questionsAsked: 0
      }
      setStudents(prev => [...prev, extendedNewStudent])
      
      // Reset form and close dialog
      setFormData({
        firstName: "",
        lastName: "",
        email: "",
        studentId: "",
        department: "",
      })
      setIsAddStudentOpen(false)
      setSuccess(`Étudiant ${newStudent.name} créé avec succès!`)
      
    } catch (err: any) {
      setError(err.message || "Erreur lors de la création de l'étudiant")
      console.error("Error creating student:", err)
    } finally {
      setIsLoading(false)
    }
  }

  // Filter students (using real data when available, mock data as fallback)
  const allStudents: ExtendedStudent[] = students.length > 0 ? students : mockStudents.map(s => ({
    id: parseInt(s.id),
    name: s.name,
    email: s.email,
    role: "student",
    studentId: s.studentId,
    department: s.department,
    status: s.status as 'active' | 'inactive',
    lastLogin: s.lastLogin,
    questionsAsked: s.questionsAsked
  }))

  const filteredStudents = allStudents.filter((student) => {
    const matchesSearch =
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (student.studentId && student.studentId.toLowerCase().includes(searchTerm.toLowerCase()))
    return matchesSearch
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 rounded-xl flex items-center justify-center shadow-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-slate-900">Panneau d'Administration</h1>
                <p className="text-sm text-slate-600">Université de Technologie - Gestion Système</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" className="relative">
                <Bell className="h-4 w-4" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </Button>

              <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
                <div className="text-right">
                  <p className="text-sm font-medium text-slate-900">{user?.name}</p>
                  <p className="text-xs text-slate-500">Administrateur Système</p>
                </div>
                <Button variant="ghost" size="sm" onClick={logout}>
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-white/50 backdrop-blur-sm">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Vue d'ensemble
            </TabsTrigger>
            <TabsTrigger value="students" className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              Étudiants
            </TabsTrigger>
            <TabsTrigger value="rag" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Système RAG
            </TabsTrigger>
            <TabsTrigger value="analytics" className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Analytiques
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              Paramètres
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* System Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <Badge className="bg-green-200 text-green-800">Opérationnel</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-900 mb-1">99.9%</div>
                  <p className="text-sm text-green-700">Disponibilité système</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <Users className="h-5 w-5 text-blue-600" />
                    <Badge className="bg-blue-200 text-blue-800">Actifs</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-900 mb-1">1,247</div>
                  <p className="text-sm text-blue-700">Étudiants connectés</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <MessageSquare className="h-5 w-5 text-purple-600" />
                    <Badge className="bg-purple-200 text-purple-800">+15%</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-purple-900 mb-1">8,432</div>
                  <p className="text-sm text-purple-700">Questions traitées</p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <Database className="h-5 w-5 text-orange-600" />
                    <Badge className="bg-orange-200 text-orange-800">Stable</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-900 mb-1">2.4TB</div>
                  <p className="text-sm text-orange-700">Documents indexés</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    Activité récente
                  </CardTitle>
                  <CardDescription>Dernières actions système</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { time: "Il y a 2 min", action: "Nouveau document indexé", user: "Système", status: "success" },
                      { time: "Il y a 5 min", action: "Connexion étudiant", user: "Marie Dupont", status: "info" },
                      { time: "Il y a 12 min", action: "Mise à jour modèle IA", user: "Admin", status: "warning" },
                      { time: "Il y a 18 min", action: "Sauvegarde automatique", user: "Système", status: "success" },
                    ].map((activity, index) => (
                      <div key={index} className="flex items-center gap-4 p-3 bg-slate-50 rounded-lg">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.status === "success"
                              ? "bg-green-500"
                              : activity.status === "warning"
                                ? "bg-orange-500"
                                : "bg-blue-500"
                          }`}
                        />
                        <div className="flex-1">
                          <p className="font-medium text-slate-900">{activity.action}</p>
                          <p className="text-sm text-slate-600">
                            {activity.user} • {activity.time}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5" />
                    Alertes système
                  </CardTitle>
                  <CardDescription>Notifications importantes</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center gap-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <AlertTriangle className="h-4 w-4 text-yellow-600" />
                      <div className="flex-1">
                        <p className="font-medium text-yellow-900">Maintenance programmée</p>
                        <p className="text-sm text-yellow-700">Dimanche 3h-5h du matin</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <Clock className="h-4 w-4 text-blue-600" />
                      <div className="flex-1">
                        <p className="font-medium text-blue-900">Mise à jour disponible</p>
                        <p className="text-sm text-blue-700">Version 2.1.3 du modèle IA</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="students" className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Gestion des étudiants</h2>
                <p className="text-slate-600">Administration des comptes étudiants</p>
              </div>
              <Dialog open={isAddStudentOpen} onOpenChange={setIsAddStudentOpen}>
                <DialogTrigger asChild>
                  <Button className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="h-4 w-4 mr-2" />
                    Ajouter un étudiant
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-md">
                  <DialogHeader>
                    <DialogTitle>Ajouter un nouvel étudiant</DialogTitle>
                    <DialogDescription>Créer un nouveau compte étudiant dans le système</DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    {/* Error/Success Messages */}
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
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName">Prénom *</Label>
                        <Input 
                          id="firstName" 
                          placeholder="Marie" 
                          value={formData.firstName}
                          onChange={(e) => handleInputChange("firstName", e.target.value)}
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName">Nom *</Label>
                        <Input 
                          id="lastName" 
                          placeholder="Dupont" 
                          value={formData.lastName}
                          onChange={(e) => handleInputChange("lastName", e.target.value)}
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email universitaire *</Label>
                      <Input 
                        id="email" 
                        type="email" 
                        placeholder="marie.dupont@univ-tech.fr" 
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        required
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="studentId">Numéro étudiant</Label>
                        <Input 
                          id="studentId" 
                          placeholder="ET2024005" 
                          value={formData.studentId}
                          onChange={(e) => handleInputChange("studentId", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="department">Département</Label>
                        <Select value={formData.department} onValueChange={(value) => handleInputChange("department", value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Sélectionner" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="informatique">Informatique</SelectItem>
                            <SelectItem value="electronique">Électronique</SelectItem>
                            <SelectItem value="physique">Physique</SelectItem>
                            <SelectItem value="mathematiques">Mathématiques</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    <div className="flex justify-end gap-2 pt-4">
                      <Button 
                        variant="outline" 
                        onClick={() => {
                          setIsAddStudentOpen(false)
                          setError(null)
                          setSuccess(null)
                          setFormData({
                            firstName: "",
                            lastName: "",
                            email: "",
                            studentId: "",
                            department: "",
                          })
                        }}
                        disabled={isLoading}
                      >
                        Annuler
                      </Button>
                      <Button 
                        onClick={handleAddStudent}
                        disabled={isLoading}
                      >
                        {isLoading ? "Création..." : "Créer le compte"}
                      </Button>
                    </div>
                  </div>
                </DialogContent>
              </Dialog>
            </div>

            {/* Search and Filters */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                    <Input
                      placeholder="Rechercher par nom, email ou numéro étudiant..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
                    <SelectTrigger className="w-full sm:w-48">
                      <SelectValue placeholder="Département" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Tous les départements</SelectItem>
                      <SelectItem value="Informatique">Informatique</SelectItem>
                      <SelectItem value="Électronique">Électronique</SelectItem>
                      <SelectItem value="Physique">Physique</SelectItem>
                      <SelectItem value="Mathématiques">Mathématiques</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* Students Table */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Liste des étudiants ({filteredStudents.length})</span>
                  <div className="flex gap-2">
                    <Badge variant="outline" className="text-green-700 border-green-200">
                      {mockStudents.filter((s) => s.status === "active").length} Actifs
                    </Badge>
                    <Badge variant="outline" className="text-slate-700 border-slate-200">
                      {mockStudents.filter((s) => s.status === "inactive").length} Inactifs
                    </Badge>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Étudiant</TableHead>
                        <TableHead>Département</TableHead>
                        <TableHead>Statut</TableHead>
                        <TableHead>Dernière connexion</TableHead>
                        <TableHead>Questions posées</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredStudents.map((student) => (
                        <TableRow key={student.id}>
                          <TableCell>
                            <div>
                              <div className="font-medium text-slate-900">{student.name}</div>
                              <div className="text-sm text-slate-500">{student.email}</div>
                              <div className="text-xs text-slate-400">{student.studentId || 'N/A'}</div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="text-slate-700">
                              {student.department || 'N/A'}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <Badge
                              variant={student.status === "active" ? "default" : "secondary"}
                              className={
                                student.status === "active"
                                  ? "bg-green-100 text-green-800 border-green-200"
                                  : "bg-slate-100 text-slate-800 border-slate-200"
                              }
                            >
                              {student.status === "active" ? (
                                <>
                                  <UserCheck className="h-3 w-3 mr-1" />
                                  Actif
                                </>
                              ) : (
                                <>
                                  <UserX className="h-3 w-3 mr-1" />
                                  Inactif
                                </>
                              )}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-sm text-slate-600">{student.lastLogin || 'N/A'}</TableCell>
                          <TableCell>
                            <div className="text-center">
                              <span className="font-medium text-slate-900">{student.questionsAsked || 0}</span>
                            </div>
                          </TableCell>
                          <TableCell className="text-right">
                            <div className="flex items-center justify-end gap-2">
                              <Button variant="ghost" size="sm">
                                <Mail className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="rag" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* RAG System Status */}
              <Card className="lg:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5" />
                    État du Système RAG
                  </CardTitle>
                  <CardDescription>Surveillance en temps réel du système d'IA</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="text-sm font-medium text-green-900">Modèle IA</span>
                      </div>
                      <div className="text-2xl font-bold text-green-900">Actif</div>
                      <div className="text-xs text-green-700">sentence-transformers/all-MiniLM-L6-v2</div>
                    </div>

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Database className="h-4 w-4 text-blue-600" />
                        <span className="text-sm font-medium text-blue-900">Base Vectorielle</span>
                      </div>
                      <div className="text-2xl font-bold text-blue-900">2.4TB</div>
                      <div className="text-xs text-blue-700">156,432 vecteurs indexés</div>
                    </div>

                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Activity className="h-4 w-4 text-purple-600" />
                        <span className="text-sm font-medium text-purple-900">Performance</span>
                      </div>
                      <div className="text-2xl font-bold text-purple-900">0.3s</div>
                      <div className="text-xs text-purple-700">Temps de réponse moyen</div>
                    </div>

                    <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <Clock className="h-4 w-4 text-orange-600" />
                        <span className="text-sm font-medium text-orange-900">Dernière Sync</span>
                      </div>
                      <div className="text-2xl font-bold text-orange-900">2min</div>
                      <div className="text-xs text-orange-700">Synchronisation réussie</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Document Management */}
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center gap-2">
                      <Database className="h-5 w-5" />
                      Gestion des Documents
                    </span>
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                      <Plus className="h-4 w-4 mr-2" />
                      Ajouter Documents
                    </Button>
                  </CardTitle>
                  <CardDescription>Documents indexés dans le système RAG</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      {
                        name: "Cours_Mathematiques_L3.pdf",
                        size: "2.4 MB",
                        status: "indexed",
                        date: "2024-01-15",
                        chunks: 45,
                      },
                      {
                        name: "TD_Physique_Quantique.pdf",
                        size: "1.8 MB",
                        status: "processing",
                        date: "2024-01-15",
                        chunks: 32,
                      },
                      {
                        name: "Examens_Corriges_2023.pdf",
                        size: "5.2 MB",
                        status: "indexed",
                        date: "2024-01-14",
                        chunks: 78,
                      },
                      {
                        name: "Manuel_Programmation_C++.pdf",
                        size: "12.1 MB",
                        status: "indexed",
                        date: "2024-01-14",
                        chunks: 156,
                      },
                      {
                        name: "Projet_Electronique.pdf",
                        size: "3.7 MB",
                        status: "failed",
                        date: "2024-01-13",
                        chunks: 0,
                      },
                    ].map((doc, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                        <div className="flex-1">
                          <div className="font-medium text-slate-900">{doc.name}</div>
                          <div className="text-sm text-slate-600">
                            {doc.size} • {doc.date} • {doc.chunks} segments
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <Badge
                            variant="outline"
                            className={
                              doc.status === "indexed"
                                ? "border-green-200 text-green-700 bg-green-50"
                                : doc.status === "processing"
                                  ? "border-orange-200 text-orange-700 bg-orange-50"
                                  : "border-red-200 text-red-700 bg-red-50"
                            }
                          >
                            {doc.status === "indexed" ? "Indexé" : doc.status === "processing" ? "En cours" : "Échec"}
                          </Badge>
                          <div className="flex gap-1">
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" className="text-red-600">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* System Controls */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5" />
                    Contrôles Système
                  </CardTitle>
                  <CardDescription>Actions de maintenance</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button className="w-full justify-start bg-transparent" variant="outline">
                    <Database className="h-4 w-4 mr-2" />
                    Réindexer la base
                  </Button>
                  <Button className="w-full justify-start bg-transparent" variant="outline">
                    <Activity className="h-4 w-4 mr-2" />
                    Optimiser les vecteurs
                  </Button>
                  <Button className="w-full justify-start bg-transparent" variant="outline">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Test de performance
                  </Button>
                  <Button className="w-full justify-start bg-transparent" variant="outline">
                    <AlertTriangle className="h-4 w-4 mr-2" />
                    Vider le cache
                  </Button>

                  <div className="pt-4 border-t border-slate-200">
                    <h4 className="text-sm font-medium text-slate-900 mb-3">Configuration IA</h4>
                    <div className="space-y-3">
                      <div>
                        <Label className="text-xs text-slate-600">Température</Label>
                        <div className="flex items-center gap-2 mt-1">
                          <Input type="range" min="0" max="1" step="0.1" defaultValue="0.7" className="flex-1" />
                          <span className="text-xs text-slate-500 w-8">0.7</span>
                        </div>
                      </div>
                      <div>
                        <Label className="text-xs text-slate-600">Top-K</Label>
                        <Input type="number" defaultValue="5" className="mt-1" />
                      </div>
                      <div>
                        <Label className="text-xs text-slate-600">Seuil de similarité</Label>
                        <Input type="number" step="0.01" defaultValue="0.75" className="mt-1" />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Query Analytics */}
              <Card className="lg:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Analytiques des Requêtes
                  </CardTitle>
                  <CardDescription>Analyse des questions posées par les étudiants</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-medium text-slate-900 mb-3">Questions les plus fréquentes</h4>
                      <div className="space-y-3">
                        {[
                          {
                            question: "Comment résoudre une équation différentielle ?",
                            count: 45,
                            subject: "Mathématiques",
                          },
                          { question: "Qu'est-ce que la mécanique quantique ?", count: 38, subject: "Physique" },
                          {
                            question: "Comment implémenter un algorithme de tri ?",
                            count: 32,
                            subject: "Informatique",
                          },
                          { question: "Expliquer les lois de Kirchhoff", count: 28, subject: "Électronique" },
                        ].map((item, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <div className="flex-1">
                              <div className="font-medium text-slate-900 text-sm">{item.question}</div>
                              <div className="text-xs text-slate-600">{item.subject}</div>
                            </div>
                            <Badge variant="outline" className="text-slate-700">
                              {item.count}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-slate-900 mb-3">Performance par matière</h4>
                      <div className="space-y-3">
                        {[
                          { subject: "Mathématiques", accuracy: 94, queries: 234 },
                          { subject: "Physique", accuracy: 91, queries: 189 },
                          { subject: "Informatique", accuracy: 96, queries: 156 },
                          { subject: "Électronique", accuracy: 88, queries: 123 },
                        ].map((item, index) => (
                          <div key={index} className="p-3 bg-slate-50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-medium text-slate-900 text-sm">{item.subject}</span>
                              <span className="text-sm text-slate-600">{item.accuracy}% précision</span>
                            </div>
                            <div className="w-full bg-slate-200 rounded-full h-2">
                              <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${item.accuracy}%` }} />
                            </div>
                            <div className="text-xs text-slate-500 mt-1">{item.queries} requêtes</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Analytiques et rapports</CardTitle>
                <CardDescription>Statistiques d'utilisation détaillées</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600">Module d'analytiques en cours de développement...</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Paramètres système</CardTitle>
                <CardDescription>Configuration générale de la plateforme</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600">Paramètres système en cours de développement...</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
