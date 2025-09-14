import { useState, useCallback, useRef, useEffect } from 'react';
import { apiService, QuestionRequest, QuestionResponse, StudentOut, ConversationOut } from '@/lib/api';

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  metadata?: {
    confidence?: number;
    sources?: Array<{
      content: string;
      source: string;
      subject: string;
    }>;
    processing_time?: number;
  };
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  systemStatus: {
    documents_loaded: boolean;
    total_vectors: number;
    model: string;
    llm_configured: boolean;
  } | null;
  error: string | null;
}

export function useChat() {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    systemStatus: null,
    error: null,
  });

  const studentRef = useRef<StudentOut | null>(null);
  const conversationRef = useRef<ConversationOut | null>(null);

  // Init student + conversation
  useEffect(() => {
    const init = async () => {
      try {
        // Récupérer utilisateur depuis localStorage
        const raw = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
        const user = raw ? JSON.parse(raw) : { name: 'Étudiant', email: 'student@example.com', role: 'student' };

        // Créer/obtenir l'étudiant
        const student = await apiService.createStudent({ name: user.name || 'Étudiant', email: user.email || 'student@example.com', role: user.role || 'student' });
        studentRef.current = student;

        // Créer une conversation
        const conv = await apiService.createConversation({ student_id: student.id, title: 'Conversation' });
        conversationRef.current = conv;
      } catch (e) {
        console.error('Init chat persistence failed:', e);
      }
    };
    init();
  }, []);

  // Generate dynamic welcome message based on system status
  const generateWelcomeMessage = useCallback((status: any) => {
    if (status?.documents_loaded && status?.total_vectors > 0) {
      return `Bonjour ! Je suis votre assistant IA universitaire. J'ai accès à ${status.total_vectors} documents de cours et je peux vous aider avec vos questions académiques. Posez-moi n'importe quelle question !`;
    } else {
      return `Bonjour ! Je suis votre assistant IA universitaire. Actuellement, je n'ai pas encore accès à vos documents de cours, mais je peux vous aider avec des questions générales sur les matières universitaires. Utilisez le bouton "Recharger" pour mettre à jour la base de connaissances.`;
    }
  }, []);

  // Charger le statut du système
  const loadSystemStatus = useCallback(async () => {
    try {
      const status = await apiService.getStatus();
      setState(prev => {
        const newState = { ...prev, systemStatus: status };
        
        // Add welcome message if no messages exist
        if (prev.messages.length === 0) {
          newState.messages = [{
            id: 'welcome',
            content: generateWelcomeMessage(status),
            sender: 'assistant',
            timestamp: new Date(),
          }];
        }
        
        return newState;
      });
    } catch (error) {
      console.error('Erreur lors du chargement du statut:', error);
      setState(prev => ({ ...prev, error: 'Impossible de vérifier le statut du système' }));
    }
  }, [generateWelcomeMessage]);

  // Envoyer un message
  const sendMessage = useCallback(async (content: string, subjectFilter?: string) => {
    if (!content.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
    };

    // Ajouter le message utilisateur
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      // Sauvegarder le message utilisateur s'il y a une conversation
      if (conversationRef.current) {
        await apiService.addMessage({
          conversation_id: conversationRef.current.id,
          sender: 'user',
          content,
        });
      }

      // Envoyer la question à l'API
      const request: QuestionRequest = {
        question: content,
        subject_filter: subjectFilter,
        save: true,
        conversation_id: conversationRef.current?.id,
        student_id: studentRef.current?.id,
      };

      const response: QuestionResponse = await apiService.askQuestion(request);

      // Créer le message de l'assistant
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.answer,
        sender: 'assistant',
        timestamp: new Date(),
        metadata: {
          confidence: response.confidence,
          sources: response.sources,
          processing_time: response.processing_time,
        },
      };

      // Ajouter la réponse + sauvegarder
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        isLoading: false,
      }));

      // conversationRef may be created server-side by /api/ask response
      if (response.conversation_id && (!conversationRef.current || conversationRef.current.id !== response.conversation_id)) {
        conversationRef.current = { id: response.conversation_id, student_id: studentRef.current!.id, title: 'Conversation' };
      }

    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Désolé, une erreur s\'est produite lors du traitement de votre question. Veuillez réessayer.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        error: 'Erreur de communication avec le serveur',
      }));
    }
  }, []);

  // Effacer l'historique (ne supprime pas la conversation DB ici)
  const clearHistory = useCallback(() => {
    setState(prev => ({
      ...prev,
      messages: [
        {
          id: '1',
          content: 'Bonjour ! Je suis votre assistant IA universitaire. Posez-moi n\'importe quelle question sur vos études, même si je n\'ai pas encore accès à vos documents de cours.',
          sender: 'assistant',
          timestamp: new Date(),
        },
      ],
      error: null,
    }));
  }, []);

  // Recharger les documents
  const reloadDocuments = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      await apiService.reloadDocuments();
      await loadSystemStatus();
      setState(prev => ({ ...prev, isLoading: false }));
    } catch (error) {
      console.error('Erreur lors du rechargement:', error);
      setState(prev => ({ 
        ...prev, 
        isLoading: false, 
        error: 'Erreur lors du rechargement des documents' 
      }));
    }
  }, [loadSystemStatus]);

  return {
    ...state,
    sendMessage,
    clearHistory,
    reloadDocuments,
    loadSystemStatus,
  };
}
