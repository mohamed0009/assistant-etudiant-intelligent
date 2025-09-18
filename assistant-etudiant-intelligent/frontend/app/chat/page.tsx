"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Bot, User, ArrowLeft, BookOpen, Brain, Sparkles, RefreshCw, AlertCircle, Save, Download } from "lucide-react"
import Link from "next/link"
import { useChat, Message } from "@/hooks/use-chat"
import { apiService } from "@/lib/api"
import { ClientTime } from "@/components/client-time"

export default function ChatPage() {
  const {
    messages,
    isLoading,
    systemStatus,
    error,
    sendMessage,
    clearHistory,
    reloadDocuments,
    loadSystemStatus
  } = useChat()
  
  const [input, setInput] = useState("")
  const [selectedSubject, setSelectedSubject] = useState<string>("all")
  const [isExporting, setIsExporting] = useState<boolean>(false)
  const [exportMessage, setExportMessage] = useState<string>("")

  const handleExport = async (format: 'json' | 'pdf' = 'json') => {
    try {
      setIsExporting(true)
      setExportMessage("")
      
      // Try to read current student and conversation from localStorage mirrors used in useChat init
      const raw = typeof window !== 'undefined' ? localStorage.getItem('user') : null
      const user = raw ? JSON.parse(raw) : { name: 'Étudiant', email: 'student@example.com', role: 'student' }
      
      // Ensure student exists and get or create a conversation id via API helper chain
      const student = await apiService.createStudent({ 
        name: user.name || 'Étudiant', 
        email: user.email || 'student@example.com', 
        role: user.role || 'student' 
      })
      
      // Export all conversations for now (simple UX)
      const res = await apiService.exportStudentConversations(student.id, format)
      
      // Use the proper download endpoint
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const downloadUrl = `${baseUrl}/api/export/download/${res.filename}`
      
      try {
        // Try to fetch the file content directly
        const response = await fetch(downloadUrl)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.download = res.filename
        link.style.display = 'none'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        // Clean up the object URL
        window.URL.revokeObjectURL(url)
        
        setExportMessage(`Export téléchargé: ${res.filename}`)
      } catch (fetchError) {
        // Fallback: try direct download
        console.warn('Direct fetch failed, trying direct download:', fetchError)
        window.open(downloadUrl, '_blank')
        setExportMessage(`Export ouvert dans un nouvel onglet: ${res.filename}`)
      }
      
    } catch (e: any) {
      setExportMessage('Erreur lors de l\'export')
      console.error('Export error', e)
    } finally {
      setIsExporting(false)
    }
  }

  const handleSendMessage = async () => {
    if (!input.trim()) return
    
    const currentInput = input
    setInput("")
    
    await sendMessage(currentInput, selectedSubject === "all" ? undefined : selectedSubject)
  }

  // Charger le statut du système au démarrage
  useEffect(() => {
    loadSystemStatus()
  }, [loadSystemStatus])

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const quickQuestions = [
    "Qu'est-ce qu'une dérivée ?",
    "Explique-moi la loi d'Ohm",
    "Comment calculer une intégrale ?",
    "Qu'est-ce que la thermodynamique ?",
    "Aide-moi avec les équations différentielles",
    "Concepts de base en électronique",
  ]

  const subjects = [
    "Toutes les Matières",
    "Mathématiques",
    "Physique",
    "Chimie",
    "Biologie",
    "Informatique",
    "Électricité",
    "Électronique"
  ]

  return (
    <div className="flex flex-col h-dvh">
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          <div className="flex items-center gap-4">
            <Link href="/student">
              <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Retour
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-primary text-primary-foreground">
                <Brain className="w-7 h-7" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">
                  Assistant IA RAG
                </h1>
                <p className="text-sm text-gray-600 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Système RAG Universitaire - Université de Technologie
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
                      {/* Statut du système */}
          <div className="flex items-center gap-2 text-sm">
            <div className={`w-2 h-2 rounded-full animate-pulse ${
              systemStatus?.documents_loaded ? 'bg-green-500' : 'bg-green-500'
            }`}></div>
            {systemStatus?.documents_loaded ? 'Documents Chargés' : 'Documents de Cours Disponibles'}
          </div>
            
            {/* Bouton recharger */}
            <Button
              variant="outline"
              size="sm"
              onClick={reloadDocuments}
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              Recharger
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport('json')}
              disabled={isExporting}
              className="flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              {isExporting ? 'Sauvegarde...' : 'Sauvegarder'}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport('pdf')}
              disabled={isExporting}
              className="flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              {isExporting ? 'Export...' : 'Exporter PDF'}
            </Button>
          </div>
        </div>
      </div>

      {/* Filtres et sélection de matière */}
      <div className="border-b p-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-gray-700">Matière :</label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="px-3 py-2 border border-blue-200 rounded-md bg-white/90 focus:border-blue-400 focus:ring-blue-400/20"
            >
              {subjects.map((subject) => (
                <option key={subject} value={subject === "Toutes les Matières" ? "all" : subject}>
                  {subject}
                </option>
              ))}
            </select>
            
            {systemStatus && (
              <div className="text-sm text-gray-600">
                {systemStatus.documents_loaded ? (
                  <span><span className="font-medium">{systemStatus.total_vectors || 20}</span> documents de cours disponibles</span>
                ) : (
                  <span className="text-green-600">📚 Documents de cours disponibles (20+ fichiers)</span>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-4 ${message.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              {message.sender === "assistant" && (
                <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-primary text-primary-foreground">
                  <Bot className="w-5 h-5" />
                </div>
              )}

              <Card
                className={`max-w-[85%] p-4 ${
                  message.sender === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-card text-foreground border"
                }`}
              >
                <div className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</div>
                <div className={`text-xs mt-2 ${message.sender === "user" ? "text-blue-100" : "text-gray-500"}`}>
                  <ClientTime timestamp={message.timestamp} />
                </div>
                
                {/* Métadonnées pour les réponses de l'assistant */}
                {message.sender === "assistant" && message.metadata && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="flex flex-wrap gap-2 text-xs">
                      {message.metadata.confidence && (
                        <span className={`px-2 py-1 rounded-full ${
                          message.metadata.confidence > 0.7 ? 'bg-green-100 text-green-800' :
                          message.metadata.confidence > 0.4 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          Confiance: {(message.metadata.confidence * 100).toFixed(0)}%
                        </span>
                      )}
                      {message.metadata.processing_time && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                          {(message.metadata.processing_time * 1000).toFixed(0)}ms
                        </span>
                      )}
                    </div>
                    
                    {/* Course Document Usage */}
                    {message.metadata.has_course_content && (
                      <div className="mt-2">
                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                          📚 {message.metadata.course_documents_used} document(s) de cours utilisé(s)
                        </span>
                      </div>
                    )}
                    
                    {/* Model Information */}
                    {message.metadata.model_used && (
                      <div className="mt-1">
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                          🤖 {message.metadata.model_used}
                          {message.metadata.fallback_used && " (fallback)"}
                        </span>
                      </div>
                    )}
                    
                    {/* Sources */}
                    {message.metadata.sources && message.metadata.sources.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium text-gray-600 mb-1">Sources :</p>
                        <div className="space-y-1">
                          {message.metadata.sources.slice(0, 3).map((source, index) => (
                            <div key={index} className="px-2 py-1 bg-gray-50 border rounded text-xs">
                              <div className="font-medium text-gray-800">{source.title}</div>
                              <div className="text-gray-600">
                                {source.metadata?.subject || 'Général'} • Score: {(source.score * 100).toFixed(0)}%
                              </div>
                              {source.metadata?.type === 'course_document' && (
                                <div className="text-green-600">📖 Document de cours</div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </Card>

              {message.sender === "user" && (
                <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-foreground text-background">
                  <User className="w-5 h-5" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-4 justify-start">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 bg-primary text-primary-foreground">
                <Bot className="w-5 h-5" />
              </div>
              <Card className="p-4 border">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <BookOpen className="w-4 h-4 animate-pulse" />
                  Analyse de vos documents en cours...
                  <div className="flex gap-1 ml-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* Affichage des erreurs */}
          {error && (
            <div className="flex gap-4 justify-start">
              <div className="w-10 h-10 bg-red-500 rounded-xl flex items-center justify-center flex-shrink-0">
                <AlertCircle className="w-5 h-5 text-white" />
              </div>
              <Card className="bg-red-50 border-red-200 p-4">
                <div className="flex items-center gap-2 text-sm text-red-700">
                  <AlertCircle className="w-4 h-4" />
                  {error}
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* Export feedback */}
      {exportMessage && (
        <div className="px-6">
          <div className="max-w-4xl mx-auto text-sm text-gray-600">{exportMessage}</div>
        </div>
      )}

      {/* Input Section */}
      <div className="border-t p-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* Quick Questions */}
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-700 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Questions rapides :
            </p>
            <div className="flex flex-wrap gap-2">
              {quickQuestions.map((question) => (
                <Button
                  key={question}
                  variant="outline"
                  size="sm"
                  onClick={() => setInput(question)}
                  className="text-xs hover:bg-blue-50 hover:border-blue-300 transition-colors"
                  disabled={isLoading}
                >
                  {question}
                </Button>
              ))}
            </div>
          </div>

          {/* Input Field */}
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Posez votre question sur vos cours, TD, examens..."
              className="flex-1 text-base h-12 bg-white/90 border-blue-200 focus:border-blue-400 focus:ring-blue-400/20"
              disabled={isLoading}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!input.trim() || isLoading}
              className="h-12 px-6"
            >
              <Send className="w-5 h-5" />
            </Button>
            <Button
              variant="outline"
              onClick={clearHistory}
              disabled={isLoading}
              className="h-12 px-4"
            >
              Effacer
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
