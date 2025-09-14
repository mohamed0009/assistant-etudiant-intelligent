// Données simulées pour enrichir l'interface utilisateur

export interface MockDocument {
  id: string
  name: string
  type: string
  size: string
  subject: string
  description: string
  tags: string[]
  uploadedAt: string
  source: 'backend' | 'student'
}

export interface MockSubject {
  id: string
  name: string
  code: string
  description: string
  documentsCount: number
  questionsCount: number
  color: string
}

export interface MockUsageStats {
  totalQuestions: number
  satisfactionRate: number
  subjectsConsulted: number
  totalUsageTime: string
  lastActivity: string
  favoriteSubjects: string[]
}

export const mockSubjects: MockSubject[] = [
  {
    id: '1',
    name: 'Mathématiques',
    code: 'MATH101',
    description: 'Calcul différentiel et intégral, Algèbre linéaire',
    documentsCount: 12,
    questionsCount: 45,
    color: 'rose'
  },
  {
    id: '2',
    name: 'Physique',
    code: 'PHYS101',
    description: 'Mécanique classique, Électromagnétisme',
    documentsCount: 8,
    questionsCount: 38,
    color: 'blue'
  },
  {
    id: '3',
    name: 'Informatique',
    code: 'INFO101',
    description: 'Algorithmes, Structures de données, Programmation',
    documentsCount: 15,
    questionsCount: 32,
    color: 'green'
  },
  {
    id: '4',
    name: 'Chimie',
    code: 'CHIM101',
    description: 'Chimie générale, Thermodynamique',
    documentsCount: 6,
    questionsCount: 24,
    color: 'purple'
  },
  {
    id: '5',
    name: 'Biologie',
    code: 'BIO101',
    description: 'Biologie cellulaire, Génétique',
    documentsCount: 9,
    questionsCount: 18,
    color: 'emerald'
  },
  {
    id: '6',
    name: 'Économie',
    code: 'ECO101',
    description: 'Microéconomie, Macroéconomie',
    documentsCount: 7,
    questionsCount: 21,
    color: 'amber'
  }
]

export const mockUsageStats: MockUsageStats = {
  totalQuestions: 127,
  satisfactionRate: 89,
  subjectsConsulted: 15,
  totalUsageTime: '24h',
  lastActivity: '2024-01-15T14:30:00Z',
  favoriteSubjects: ['Mathématiques', 'Physique', 'Informatique']
}

export const mockRecentQuestions = [
  {
    id: '1',
    question: 'Comment résoudre une équation différentielle du premier ordre ?',
    subject: 'Mathématiques',
    timestamp: '2024-01-15T14:25:00Z',
    status: 'answered'
  },
  {
    id: '2',
    question: 'Quelle est la différence entre un algorithme de tri O(n²) et O(n log n) ?',
    subject: 'Informatique',
    timestamp: '2024-01-15T13:45:00Z',
    status: 'answered'
  },
  {
    id: '3',
    question: 'Expliquez le principe de conservation de l\'énergie en mécanique',
    subject: 'Physique',
    timestamp: '2024-01-15T12:15:00Z',
    status: 'answered'
  },
  {
    id: '4',
    question: 'Comment calculer le déterminant d\'une matrice 3x3 ?',
    subject: 'Mathématiques',
    timestamp: '2024-01-15T11:30:00Z',
    status: 'answered'
  }
]

export const mockSystemInfo = {
  version: '2.1.0',
  lastUpdate: '2024-01-15T10:00:00Z',
  uptime: '72h 15m',
  apiStatus: 'healthy',
  databaseStatus: 'connected',
  vectorIndexStatus: 'optimized'
}

export const getSubjectColor = (color: string) => {
  const colors: { [key: string]: string } = {
    rose: 'bg-rose-100 text-rose-800',
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
    purple: 'bg-purple-100 text-purple-800',
    emerald: 'bg-emerald-100 text-emerald-800',
    amber: 'bg-amber-100 text-amber-800'
  }
  return colors[color] || 'bg-gray-100 text-gray-800'
}

export const getSubjectIconColor = (color: string) => {
  const colors: { [key: string]: string } = {
    rose: 'text-rose-600',
    blue: 'text-blue-600',
    green: 'text-green-600',
    purple: 'text-purple-600',
    emerald: 'text-emerald-600',
    amber: 'text-amber-600'
  }
  return colors[color] || 'text-gray-600'
}

