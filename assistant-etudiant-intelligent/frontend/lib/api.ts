const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface QuestionRequest {
  question: string;
  subject_filter?: string;
  save?: boolean;
  conversation_id?: number;
  student_id?: number;
  create_conversation?: boolean;
  title?: string;
}

export interface QuestionResponse {
  answer: string;
  confidence: number;
  sources: Array<{
    title: string;
    content: string;
    score: number;
    metadata: {
      subject: string;
      type: string;
      source?: string;
      model?: string;
    };
  }>;
  processing_time: number;
  query: string;
  conversation_id?: number;
  user_message_id?: number;
  assistant_message_id?: number;
  model_used?: string;
  ollama_response_time?: number;
  tokens_generated?: number;
  source_scores?: number[];
  metadata?: {
    subject: string;
    timestamp: string;
    ollama_used: boolean;
    model: string;
    course_documents_used: number;
    has_course_content: boolean;
  };
  response_quality?: {
    relevance: number;
    completeness: number;
    clarity: number;
  };
  fallback_used?: boolean;
}

export interface SystemStatus {
  documents_loaded: boolean;
  total_vectors: number;
  model: string;
  llm_configured: boolean;
}

export interface DocumentStats {
  total_documents: number;
  total_chunks: number;
  subjects: string[];
  last_updated?: string | number;
}

export interface SubjectOut {
  id: string;
  name: string;
  code: string;
  description: string;
  documents_count: number;
  questions_count: number;
  color: string;
}

export interface StudentUsageStats {
  total_questions: number;
  total_conversations: number;
  total_documents: number;
  last_activity: string;
  favorite_subjects: string[];
}

export interface DocumentOut {
  id: string;
  name: string;
  type: string;
  size: string;
  uploaded_at: string;
  status: string;
  source: string;
  subject?: string;
}

export interface SystemSettings {
  openai_key?: string;
  use_openai: boolean;
  top_k: number;
  model_name: string;
  chunk_size: number;
  chunk_overlap: number;
}

// DB-backed models
export interface StudentCreate { name: string; email: string; role?: 'student' | 'admin' }
export interface StudentOut { id: number; name: string; email: string; role: string }
export interface StudentUpdate { name?: string; email?: string; role?: string }

export interface ConversationCreate { student_id: number; title?: string }
export interface ConversationOut { id: number; student_id: number; title: string }

export interface MessageCreate {
  conversation_id: number;
  sender: 'user' | 'assistant';
  content: string;
  confidence?: string;
  response_time?: string;
}
export interface MessageOut {
  id: number;
  conversation_id: number;
  sender: 'user' | 'assistant';
  content: string;
  confidence?: string;
  response_time?: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Vérifier le statut du système
  async getStatus(): Promise<SystemStatus> {
    return this.request<SystemStatus>('/api/status');
  }

  // Obtenir les statistiques des documents
  async getStats(): Promise<DocumentStats> {
    return this.request<DocumentStats>('/api/documents/stats');
  }

  // Poser une question
  async askQuestion(request: QuestionRequest): Promise<QuestionResponse> {
    // Map frontend request to backend format - the backend expects a simple dict
    const backendRequest = {
      question: request.question,
      subject_filter: request.subject_filter
    };
    
    const response = await this.request<any>('/api/ask', {
      method: 'POST',
      body: JSON.stringify(backendRequest),
    });
    
    // Normalize sources to ensure metadata exists with safe defaults
    const normalizedSources = Array.isArray(response.sources)
      ? response.sources.map((src: any) => ({
          title: typeof src?.title === 'string' ? src.title : (src?.metadata?.source || 'Source'),
          content: typeof src?.content === 'string' ? src.content : '',
          score: typeof src?.score === 'number' ? src.score : 0,
          metadata: {
            subject: typeof src?.metadata?.subject === 'string' ? src.metadata.subject : 'Général',
            type: typeof src?.metadata?.type === 'string' ? src.metadata.type : (src?.metadata?.source ? 'course_document' : 'unknown'),
            source: typeof src?.metadata?.source === 'string' ? src.metadata.source : undefined,
            model: typeof src?.metadata?.model === 'string' ? src.metadata.model : undefined,
          },
        }))
      : [];
    
    // Map backend response to frontend format
    return {
      answer: response.answer,
      confidence: response.confidence,
      sources: normalizedSources,
      processing_time: response.processing_time,
      query: response.query,
      conversation_id: response.conversation_id,
      user_message_id: response.user_message_id,
      assistant_message_id: response.assistant_message_id,
    };
  }

  // Obtenir les questions suggérées
  async getSuggestions(subject?: string): Promise<string[]> {
    // This endpoint doesn't exist in the backend API yet
    // Fallback to some default suggestions
    return Promise.resolve([
      "Qu'est-ce que la loi d'Ohm?",
      "Comment calculer une dérivée?",
      "Expliquez le théorème de Pythagore",
      "Qu'est-ce qu'un transistor?"
    ]);
  }

  // Recharger les documents
  async reloadDocuments(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/api/documents/validate', {
      method: 'POST',
    });
  }

  // Vérification de santé
  async healthCheck(): Promise<{ status: string; documents_loaded: boolean; rag_engine_ready: boolean }> {
    return this.request('/api/status');
  }

  // -------- Metrics --------
  async getMetrics(): Promise<any> {
    return this.request('/api/metrics');
  }

  // -------- Students / Conversations / Messages --------
  async createStudent(payload: StudentCreate): Promise<StudentOut> {
    return this.request<StudentOut>('/api/students', { method: 'POST', body: JSON.stringify(payload) });
    }

  async listStudents(): Promise<StudentOut[]> {
    return this.request<StudentOut[]>('/api/students');
  }

  async updateStudent(studentId: number, payload: StudentUpdate): Promise<StudentOut> {
    return this.request<StudentOut>(`/api/students/${studentId}`, { method: 'PUT', body: JSON.stringify(payload) });
  }

  async deleteStudent(studentId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/api/students/${studentId}`, { method: 'DELETE' });
  }

  async getStudent(studentId: number): Promise<StudentOut> {
    return this.request<StudentOut>(`/api/students/${studentId}`);
  }

  async createConversation(payload: ConversationCreate): Promise<ConversationOut> {
    return this.request<ConversationOut>('/api/conversations', { method: 'POST', body: JSON.stringify(payload) });
  }

  async listStudentConversations(studentId: number): Promise<ConversationOut[]> {
    return this.request<ConversationOut[]>(`/api/students/${studentId}/conversations`);
  }

  async addMessage(payload: MessageCreate): Promise<MessageOut> {
    return this.request<MessageOut>('/api/messages', { method: 'POST', body: JSON.stringify(payload) });
  }

  async listMessages(conversationId: number): Promise<MessageOut[]> {
    return this.request<MessageOut[]>(`/api/conversations/${conversationId}/messages`);
  }

  // Conversation utilities
  async updateConversationTitle(conversationId: number, title: string): Promise<ConversationOut> {
    return this.request<ConversationOut>(`/api/conversations/${conversationId}/title`, {
      method: 'PUT',
      body: JSON.stringify({ title }),
    });
  }

  async duplicateConversation(conversationId: number, newTitle: string): Promise<ConversationOut> {
    return this.request<ConversationOut>(`/api/conversations/${conversationId}/duplicate`, {
      method: 'POST',
      body: JSON.stringify({ new_title: newTitle }),
    });
  }

  // Exports
  async exportConversation(conversationId: number, format: 'json' | 'csv' = 'json'):
    Promise<{ message: string; filepath: string; filename: string; messages_count: number }>
  {
    return this.request(`/api/conversations/${conversationId}/export?format=${format}`);
  }

  async exportStudentConversations(studentId: number, format: 'json' | 'csv' | 'pdf' = 'json'):
    Promise<{ message: string; filepath: string; filename: string; conversations_count: number }>
  {
    return this.request(`/api/students/${studentId}/conversations/export?format=${format}`);
  }

  // -------- Admin Documents --------
  async listAdminDocuments(): Promise<{ documents: Array<{ filename: string; size: number; modified: number }>; total: number } > {
    return this.request('/api/admin/documents');
  }

  async uploadAdminDocument(file: File): Promise<{ message: string; filename: string }> {
    const url = `${this.baseUrl}/api/admin/documents/upload`;
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(url, { method: 'POST', body: form });
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return res.json();
  }

  async deleteAdminDocument(filename: string): Promise<{ message: string; filename: string }> {
    return this.request(`/api/admin/documents/${encodeURIComponent(filename)}`, { method: 'DELETE' });
  }

  // -------- Student Dashboard Data --------
  async getStudentSubjects(): Promise<SubjectOut[]> {
    return this.request('/api/student/subjects');
  }

  async getStudentUsageStats(studentId: number): Promise<StudentUsageStats> {
    return this.request(`/api/student/${studentId}/usage-stats`);
  }

  // -------- Document Management --------
  async getAllDocuments(): Promise<DocumentOut[]> {
    return this.request('/api/documents');
  }

  async getStudentDocuments(studentId: number): Promise<DocumentOut[]> {
    return this.request(`/api/student/${studentId}/documents`);
  }

  // -------- Admin Settings --------
  async getSystemSettings(): Promise<SystemSettings> {
    return this.request('/api/admin/settings');
  }

  async updateSystemSettings(settings: SystemSettings): Promise<SystemSettings> {
    return this.request('/api/admin/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  }
}

export const apiService = new ApiService();
