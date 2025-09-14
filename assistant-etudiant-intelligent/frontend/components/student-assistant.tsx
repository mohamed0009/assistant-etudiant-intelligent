"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  Upload,
  Send,
  BookOpen,
  FileText,
  MessageCircle,
  GraduationCap,
  Shield,
  Clock,
  Home,
  Sparkles,
  Brain,
  Zap,
} from "lucide-react"
import Link from "next/link"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
  sources?: string[]
}

interface Document {
  id: string
  name: string
  type: string
  size: number
  uploadDate: Date
  processed: boolean
}

export function StudentAssistant() {
  const simulatedUser = { name: "Étudiant" }

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content: `Bonjour ${simulatedUser.name} ! 🎓 Je suis votre assistant IA personnel, spécialement conçu pour vous accompagner dans vos études. Téléchargez vos cours et posez-moi toutes vos questions académiques - je suis là pour vous aider à réussir !`,
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [documents, setDocuments] = useState<Document[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [showWelcome, setShowWelcome] = useState(true)
  const [showSidebar, setShowSidebar] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setShowWelcome(false), 3000)
    return () => clearTimeout(timer)
  }, [])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: inputValue,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: `Excellente question ! Basé sur vos documents téléchargés, voici ce que je peux vous expliquer sur "${inputValue}". Cette information provient de vos cours et TD.`,
        timestamp: new Date(),
        sources: documents.length > 0 ? [documents[0].name] : undefined,
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files) return

    Array.from(files).forEach((file) => {
      const newDoc: Document = {
        id: Date.now().toString() + Math.random(),
        name: file.name,
        type: file.type,
        size: file.size,
        uploadDate: new Date(),
        processed: false,
      }

      setDocuments((prev) => [...prev, newDoc])

      setTimeout(() => {
        setDocuments((prev) => prev.map((doc) => (doc.id === newDoc.id ? { ...doc, processed: true } : doc)))
      }, 2000)
    })
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-indigo-400/20 to-blue-400/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {showWelcome && (
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/95 to-indigo-700/95 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="text-center text-white animate-fade-in">
            <div className="mb-6">
              <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                <Brain className="w-10 h-10 text-white" />
              </div>
              <h1 className="text-4xl font-bold mb-2">Assistant IA Universitaire</h1>
              <p className="text-xl text-blue-100">Votre compagnon d'études intelligent</p>
            </div>
            <div className="flex items-center justify-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4" />
                <span>IA Avancée</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="w-4 h-4" />
                <span>Réponses Instantanées</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4" />
                <span>100% Sécurisé</span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex h-full relative z-10">
        <div
          className={`${showSidebar ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0 fixed lg:relative z-30 w-80 h-full transition-transform duration-300 ease-in-out lg:block border-r border-white/20 bg-white/90 backdrop-blur-xl shadow-2xl`}
        >
          <div className="lg:hidden absolute top-4 right-4 z-40">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowSidebar(false)}
              className="bg-white/80 backdrop-blur-sm"
            >
              ✕
            </Button>
          </div>

          <div className="p-4 lg:p-6 h-full overflow-y-auto">
            <div className="flex items-center justify-between mb-4 lg:mb-6">
              <Link href="/dashboard">
                <Button
                  variant="outline"
                  size="sm"
                  className="shadow-lg hover:shadow-xl transition-all bg-white/50 backdrop-blur-sm border-white/30 hover:bg-white/70"
                >
                  <Home className="h-4 w-4 mr-2" />
                  Dashboard
                </Button>
              </Link>
            </div>

            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-white/20">
              <div className="p-3 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl shadow-xl animate-pulse">
                <GraduationCap className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg lg:text-xl font-bold text-slate-900 text-balance">Assistant IA</h1>
                <p className="text-sm text-blue-600 font-semibold">Système RAG Universitaire</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="p-3 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl border border-green-200/50 shadow-lg hover:shadow-xl transition-all hover:scale-105">
                <div className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-green-600 animate-pulse" />
                  <span className="text-xs font-bold text-slate-700">Sécurisé</span>
                </div>
              </div>
              <div className="p-3 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl border border-blue-200/50 shadow-lg hover:shadow-xl transition-all hover:scale-105">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-blue-600 animate-pulse" />
                  <span className="text-xs font-bold text-slate-700">24/7</span>
                </div>
              </div>
            </div>

            <Card className="mb-6 border-0 shadow-xl bg-gradient-to-br from-white/90 to-blue-50/50 backdrop-blur-sm hover:shadow-2xl transition-all">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2 text-slate-800 font-bold">
                  <div className="p-1 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg shadow-md">
                    <Upload className="h-4 w-4 text-white" />
                  </div>
                  Gestion Documentaire
                </CardTitle>
              </CardHeader>
              <CardContent>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  variant="outline"
                  className="w-full h-12 border-blue-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02] font-bold text-blue-700 hover:text-blue-800"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Importer des documents
                </Button>
                <p className="text-xs text-slate-600 mt-3 text-center leading-relaxed">
                  Formats acceptés : PDF, DOC, DOCX, TXT
                  <br />
                  <span className="font-bold text-blue-600">(max 10MB par fichier)</span>
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-xl bg-gradient-to-br from-white/90 to-slate-50/50 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center gap-2 text-slate-800 font-bold">
                  <div className="p-1 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg shadow-md">
                    <FileText className="h-4 w-4 text-white" />
                  </div>
                  Base Documentaire ({documents.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-48">
                  {documents.length === 0 ? (
                    <div className="text-center py-8">
                      <div className="p-4 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center shadow-lg">
                        <FileText className="h-8 w-8 text-blue-600" />
                      </div>
                      <p className="font-bold text-slate-700 mb-1">Aucun document importé</p>
                      <p className="text-xs text-slate-500 leading-relaxed text-balance">
                        Commencez par télécharger vos supports de cours pour une assistance personnalisée
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {documents.map((doc) => (
                        <div
                          key={doc.id}
                          className="p-4 rounded-xl bg-gradient-to-r from-white/80 to-blue-50/30 border border-blue-200/30 shadow-lg hover:shadow-xl transition-all hover:scale-[1.02]"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <p className="text-sm font-bold truncate text-slate-800 flex-1 mr-2">{doc.name}</p>
                            <Badge
                              variant={doc.processed ? "default" : "secondary"}
                              className={
                                doc.processed
                                  ? "bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white shadow-lg"
                                  : "bg-gradient-to-r from-amber-100 to-orange-100 text-amber-800 border-amber-200 shadow-lg animate-pulse"
                              }
                            >
                              {doc.processed ? "✓ Indexé" : "⏳ Traitement..."}
                            </Badge>
                          </div>
                          <p className="text-xs text-slate-600 font-semibold">
                            {formatFileSize(doc.size)} • {doc.uploadDate.toLocaleDateString("fr-FR")}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </div>

        {showSidebar && (
          <div className="lg:hidden fixed inset-0 bg-black/50 z-20" onClick={() => setShowSidebar(false)} />
        )}

        <div className="flex-1 flex flex-col bg-white/70 backdrop-blur-xl">
          <div className="border-b border-white/30 p-4 bg-gradient-to-r from-white/90 to-blue-50/50 backdrop-blur-xl shadow-xl sticky top-0 z-40">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowSidebar(true)}
                  className="lg:hidden bg-white/80 backdrop-blur-sm shadow-lg"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Documents
                </Button>

                <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg shadow-lg">
                  <MessageCircle className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h2 className="font-bold text-slate-900 text-balance">Chat Assistant IA</h2>
                  <p className="text-sm text-blue-600 font-bold">Posez vos questions ici</p>
                </div>
              </div>

              <div className="hidden sm:flex items-center gap-3">
                <Badge
                  variant="outline"
                  className="border-blue-300 text-blue-700 shadow-lg bg-white/50 backdrop-blur-sm font-semibold"
                >
                  <BookOpen className="h-3 w-3 mr-1" />
                  {documents.filter((d) => d.processed).length} documents
                </Badge>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-lg"></div>
                  <span className="text-sm text-slate-700 font-bold">En ligne</span>
                </div>
              </div>
            </div>
          </div>

          {messages.length === 1 && documents.length === 0 && (
            <div className="p-6 bg-gradient-to-r from-blue-100 to-indigo-100 border-b border-blue-200">
              <div className="text-center max-w-2xl mx-auto">
                <div className="mb-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-xl">
                    <MessageCircle className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Commencez votre conversation !</h3>
                  <p className="text-slate-700 mb-4">
                    Posez directement vos questions ou téléchargez vos documents pour une assistance personnalisée.
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button
                    onClick={() => setShowSidebar(true)}
                    className="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 shadow-lg"
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Télécharger des documents
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setInputValue("Bonjour, pouvez-vous m'aider avec mes études ?")}
                    className="border-blue-300 text-blue-700 hover:bg-blue-50"
                  >
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Commencer à chatter
                  </Button>
                </div>
              </div>
            </div>
          )}

          <ScrollArea className="flex-1 p-4 lg:p-6">
            <div className="space-y-6 max-w-4xl mx-auto">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[85%] sm:max-w-[80%] rounded-2xl p-4 lg:p-5 shadow-xl hover:shadow-2xl transition-all hover:scale-[1.02] ${
                      message.type === "user"
                        ? "bg-gradient-to-br from-blue-600 to-indigo-700 text-white"
                        : "bg-white/90 backdrop-blur-sm border border-white/50"
                    }`}
                  >
                    <p className="text-sm leading-relaxed text-balance font-medium">{message.content}</p>
                    {message.sources && (
                      <div className="mt-4 pt-4 border-t border-white/30">
                        <p className="text-xs text-slate-500 mb-3 font-bold">Sources référencées :</p>
                        <div className="flex flex-wrap gap-2">
                          {message.sources.map((source, index) => (
                            <Badge
                              key={index}
                              variant="outline"
                              className="text-xs border-blue-300 text-blue-700 shadow-lg bg-blue-50/50 font-semibold"
                            >
                              📄 {source}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    <p className="text-xs text-slate-400 mt-3 font-semibold">
                      {message.timestamp.toLocaleTimeString("fr-FR")}
                    </p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white/90 backdrop-blur-sm border border-white/50 rounded-2xl p-4 lg:p-5 max-w-[80%] shadow-xl">
                    <div className="flex items-center gap-3">
                      <div className="animate-spin h-5 w-5 border-2 border-blue-300 border-t-blue-600 rounded-full"></div>
                      <p className="text-sm text-slate-700 font-bold">Analyse en cours...</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="border-t border-white/30 p-4 lg:p-6 bg-gradient-to-r from-white/95 to-blue-50/50 backdrop-blur-xl shadow-xl">
            <div className="max-w-4xl mx-auto">
              <div className="mb-4 text-center">
                <div className="inline-flex items-center gap-3 bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-8 py-4 rounded-2xl shadow-xl animate-pulse">
                  <MessageCircle className="h-6 w-6" />
                  <span className="font-bold text-xl">💬 Tapez votre question ici !</span>
                  <Sparkles className="h-6 w-6" />
                </div>
              </div>

              <div className="relative mb-4">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-2xl blur-lg opacity-40 animate-pulse"></div>
                <div className="relative flex flex-col sm:flex-row gap-3 p-4 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border-4 border-blue-300">
                  <div className="flex-1 relative">
                    <Input
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      placeholder="💭 Exemple: Expliquez-moi les lois de Kirchhoff en électricité..."
                      onKeyPress={(e) => e.key === "Enter" && !e.shiftKey && handleSendMessage()}
                      className="h-16 text-lg border-3 border-blue-400 focus:border-blue-600 shadow-xl bg-white/95 backdrop-blur-sm font-medium rounded-xl px-6 placeholder:text-slate-500"
                    />
                  </div>
                  <Button
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim() || isLoading}
                    className="h-16 px-8 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-[1.05] font-bold text-lg rounded-xl"
                  >
                    <Send className="h-6 w-6 sm:mr-3" />
                    <span className="hidden sm:inline text-lg">Envoyer</span>
                  </Button>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm font-bold text-slate-700 mb-3 text-center">Questions rapides :</p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputValue("Expliquez-moi les théorèmes de Thévenin et Norton")}
                    className="bg-white/80 hover:bg-blue-50 border-blue-200 text-blue-700 shadow-lg hover:shadow-xl transition-all font-semibold"
                  >
                    Théorèmes électriques
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputValue("Comment résoudre les circuits RLC ?")}
                    className="bg-white/80 hover:bg-blue-50 border-blue-200 text-blue-700 shadow-lg hover:shadow-xl transition-all font-semibold"
                  >
                    Circuits RLC
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputValue("Différences entre transformateurs idéaux et réels")}
                    className="bg-white/80 hover:bg-blue-50 border-blue-200 text-blue-700 shadow-lg hover:shadow-xl transition-all font-semibold"
                  >
                    Transformateurs
                  </Button>
                </div>
              </div>

              <div className="text-center">
                <p className="text-xs text-slate-600 leading-relaxed text-balance font-medium">
                  <span className="font-bold text-blue-600">💡 Astuce :</span> Plus votre question est précise, plus ma
                  réponse sera adaptée à vos besoins !
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
