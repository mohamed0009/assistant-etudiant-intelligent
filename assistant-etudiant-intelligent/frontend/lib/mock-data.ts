/**
 * Mock data utilities for the frontend
 * Provides color schemes and icons for different subjects
 */

export const SUBJECT_COLORS = {
  'Mathématiques': {
    primary: '#3B82F6',
    secondary: '#DBEAFE',
    accent: '#1D4ED8'
  },
  'Physique': {
    primary: '#EF4444',
    secondary: '#FEE2E2',
    accent: '#DC2626'
  },
  'Chimie': {
    primary: '#10B981',
    secondary: '#D1FAE5',
    accent: '#059669'
  },
  'Biologie': {
    primary: '#8B5CF6',
    secondary: '#EDE9FE',
    accent: '#7C3AED'
  },
  'Informatique': {
    primary: '#F59E0B',
    secondary: '#FEF3C7',
    accent: '#D97706'
  },
  'Électronique': {
    primary: '#06B6D4',
    secondary: '#CFFAFE',
    accent: '#0891B2'
  },
  'Géologie': {
    primary: '#84CC16',
    secondary: '#ECFCCB',
    accent: '#65A30D'
  },
  'Astronomie': {
    primary: '#8B5A2B',
    secondary: '#FEF3C7',
    accent: '#92400E'
  },
  'Psychologie': {
    primary: '#EC4899',
    secondary: '#FCE7F3',
    accent: '#DB2777'
  },
  'Général': {
    primary: '#6B7280',
    secondary: '#F3F4F6',
    accent: '#4B5563'
  }
} as const

export const SUBJECT_ICONS = {
  'Mathématiques': 'Calculator',
  'Physique': 'Zap',
  'Chimie': 'FlaskConical',
  'Biologie': 'Dna',
  'Informatique': 'Laptop',
  'Électronique': 'Cpu',
  'Géologie': 'Mountain',
  'Astronomie': 'Telescope',
  'Psychologie': 'Brain',
  'Général': 'BookOpen'
} as const

/**
 * Get color scheme for a subject
 */
export function getSubjectColor(subject: string): {
  primary: string
  secondary: string
  accent: string
} {
  const normalizedSubject = subject || 'Général'
  return SUBJECT_COLORS[normalizedSubject as keyof typeof SUBJECT_COLORS] || SUBJECT_COLORS.Général
}

/**
 * Get icon color for a subject
 */
export function getSubjectIconColor(subject: string): string {
  const colors = getSubjectColor(subject)
  return colors.primary
}

/**
 * Get icon name for a subject
 */
export function getSubjectIcon(subject: string): string {
  const normalizedSubject = subject || 'Général'
  return SUBJECT_ICONS[normalizedSubject as keyof typeof SUBJECT_ICONS] || SUBJECT_ICONS.Général
}

/**
 * Mock data for testing
 */
export const MOCK_STUDENTS = [
  {
    id: 1,
    name: 'Alice Martin',
    email: 'alice.martin@univ.fr',
    role: 'student',
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    id: 2,
    name: 'Bob Dupont',
    email: 'bob.dupont@univ.fr',
    role: 'student',
    created_at: '2024-01-16T14:30:00Z'
  }
]

export const MOCK_CONVERSATIONS = [
  {
    id: 1,
    student_id: 1,
    title: 'Questions sur les équations différentielles',
    subject: 'Mathématiques',
    created_at: '2024-01-20T09:00:00Z',
    updated_at: '2024-01-20T10:30:00Z',
    message_count: 5
  },
  {
    id: 2,
    student_id: 1,
    title: 'Problèmes de mécanique quantique',
    subject: 'Physique',
    created_at: '2024-01-21T14:00:00Z',
    updated_at: '2024-01-21T15:45:00Z',
    message_count: 8
  }
]

export const MOCK_DOCUMENTS = [
  {
    id: 'doc_1',
    name: 'cours_algebre_lineaire.txt',
    type: 'txt',
    size: '2.5 MB',
    uploaded_at: '2024-01-15T10:00:00Z',
    status: 'active',
    source: 'uploaded',
    subject: 'Mathématiques'
  },
  {
    id: 'doc_2',
    name: 'cours_physique_quantique.pdf',
    type: 'pdf',
    size: '5.2 MB',
    uploaded_at: '2024-01-16T14:30:00Z',
    status: 'active',
    source: 'uploaded',
    subject: 'Physique'
  }
]

export const MOCK_SYSTEM_STATUS = {
  status: 'healthy',
  ollama_available: true,
  models_loaded: 3,
  vector_store_ready: true,
  documents_loaded: 15,
  uptime: '2 days, 5 hours',
  last_update: '2024-01-22T08:00:00Z'
}

export const MOCK_DOCUMENT_STATS = {
  total_documents: 15,
  total_size: '45.2 MB',
  subjects: [
    { name: 'Mathématiques', count: 4, size: '12.1 MB' },
    { name: 'Physique', count: 3, size: '8.5 MB' },
    { name: 'Chimie', count: 2, size: '6.2 MB' },
    { name: 'Biologie', count: 2, size: '5.8 MB' },
    { name: 'Informatique', count: 2, size: '7.1 MB' },
    { name: 'Général', count: 2, size: '5.5 MB' }
  ],
  recent_uploads: 3,
  processing_queue: 0
}

export const MOCK_STUDENT_USAGE = {
  total_questions: 45,
  total_conversations: 8,
  favorite_subjects: [
    { name: 'Mathématiques', count: 15 },
    { name: 'Physique', count: 12 },
    { name: 'Chimie', count: 8 }
  ],
  recent_activity: [
    {
      date: '2024-01-22',
      questions: 3,
      conversations: 1
    },
    {
      date: '2024-01-21',
      questions: 5,
      conversations: 2
    },
    {
      date: '2024-01-20',
      questions: 2,
      conversations: 1
    }
  ],
  average_response_time: '2.3s',
  satisfaction_score: 4.2
}

