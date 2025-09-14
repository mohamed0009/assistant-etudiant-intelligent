"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { 
  MessageSquare,
  Download,
  RefreshCw,
  BookOpen,
  User,
  Clock,
  Save,
  Copy
} from "lucide-react"
import { apiService, ConversationOut, MessageOut, StudentOut } from "@/lib/api"

export default function MyConversationsPage() {
  const [student, setStudent] = useState<StudentOut | null>(null)
  const [conversations, setConversations] = useState<ConversationOut[]>([])
  const [selected, setSelected] = useState<ConversationOut | null>(null)
  const [messages, setMessages] = useState<MessageOut[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [filter, setFilter] = useState<string>("")

  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true)
        const raw = typeof window !== 'undefined' ? localStorage.getItem('user') : null
        const user = raw ? JSON.parse(raw) : { name: 'Étudiant', email: 'student@example.com', role: 'student' }
        const s = await apiService.createStudent({ name: user.name || 'Étudiant', email: user.email || 'student@example.com', role: user.role || 'student' })
        setStudent(s)
        const convs = await apiService.listStudentConversations(s.id)
        setConversations(convs)
        if (convs.length > 0) {
          setSelected(convs[0])
          const msgs = await apiService.listMessages(convs[0].id)
          setMessages(msgs)
        }
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [])

  const refresh = async () => {
    if (!student) return
    setLoading(true)
    try {
      const convs = await apiService.listStudentConversations(student.id)
      setConversations(convs)
      if (selected) {
        const fresh = convs.find(c => c.id === selected.id) || null
        setSelected(fresh)
        if (fresh) {
          const msgs = await apiService.listMessages(fresh.id)
          setMessages(msgs)
        } else {
          setMessages([])
        }
      }
    } finally {
      setLoading(false)
    }
  }

  const openConversation = async (conv: ConversationOut) => {
    setSelected(conv)
    setLoading(true)
    try {
      const msgs = await apiService.listMessages(conv.id)
      setMessages(msgs)
    } finally {
      setLoading(false)
    }
  }

  const exportServer = async (format: 'json' | 'csv') => {
    if (!selected) return
    const res = await apiService.exportConversation(selected.id, format)
    const downloadUrl = `${(process as any).env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/export/download/${encodeURIComponent(res.filename)}`
    if (typeof window !== 'undefined') {
      window.open(downloadUrl, '_blank')
    }
  }

  const renameSelected = async () => {
    if (!selected) return
    const title = prompt('Nouveau titre de la conversation', selected.title)
    if (!title) return
    const updated = await apiService.updateConversationTitle(selected.id, title)
    setSelected(updated)
    await refresh()
  }

  const duplicateSelected = async () => {
    if (!selected) return
    const title = prompt('Titre de la copie', `${selected.title} (copie)`)
    if (!title) return
    await apiService.duplicateConversation(selected.id, title)
    await refresh()
  }

  const filteredConvs = conversations.filter(c => !filter || c.title.toLowerCase().includes(filter.toLowerCase()) || String(c.id).includes(filter))

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-xl bg-slate-900 text-white">
              <MessageSquare className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Mes Conversations</h1>
              <p className="text-slate-600">Consulter et exporter vos échanges avec l'assistant</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={refresh} disabled={loading}>
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} /> Rafraîchir
            </Button>
            <Button onClick={() => exportServer('json')} disabled={!selected}>
              <Download className="w-4 h-4 mr-2" /> Export JSON
            </Button>
            <Button onClick={() => exportServer('csv')} variant="secondary" disabled={!selected}>
              <Download className="w-4 h-4 mr-2" /> Export CSV
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Conversations</span>
                <Badge variant="secondary">{conversations.length}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-3">
                <Input placeholder="Filtrer par titre ou ID" value={filter} onChange={e => setFilter(e.target.value)} />
              </div>
              <div className="space-y-2 max-h-[70vh] overflow-auto pr-1">
                {filteredConvs.map(conv => (
                  <button key={conv.id} onClick={() => openConversation(conv)} className={`w-full text-left p-3 rounded-lg border ${selected?.id === conv.id ? 'border-slate-900 bg-slate-50' : 'border-slate-200 hover:bg-slate-50'}`}>
                    <div className="flex items-center justify-between">
                      <div className="font-medium">{conv.title}</div>
                      <Badge variant={selected?.id === conv.id ? 'default' : 'outline'}>#{conv.id}</Badge>
                    </div>
                    <div className="text-xs text-slate-500 mt-1">Conversation</div>
                  </button>
                ))}
                {filteredConvs.length === 0 && (
                  <div className="text-sm text-slate-500">Aucune conversation</div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4" />
                  {selected ? selected.title : 'Sélectionnez une conversation'}
                </span>
                {selected && (
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={renameSelected}>
                      <Save className="w-4 h-4 mr-1" /> Renommer
                    </Button>
                    <Button variant="outline" size="sm" onClick={duplicateSelected}>
                      <Copy className="w-4 h-4 mr-1" /> Dupliquer
                    </Button>
                  </div>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {selected ? (
                <div className="space-y-4 max-h-[70vh] overflow-auto pr-1">
                  {messages.map((m) => (
                    <div key={m.id} className={`p-3 rounded-lg border ${m.sender === 'user' ? 'border-blue-200 bg-blue-50' : 'border-slate-200 bg-white'}`}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <Badge variant={m.sender === 'user' ? 'default' : 'secondary'}>
                            {m.sender === 'user' ? 'Vous' : 'Assistant'}
                          </Badge>
                        </div>
                        <div className="text-xs text-slate-500 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <span>—</span>
                        </div>
                      </div>
                      <div className="text-sm whitespace-pre-wrap">{m.content}</div>
                      {(m.confidence || m.response_time) && (
                        <div className="mt-2 text-xs text-slate-500">
                          {m.confidence && (<span>Confiance: {m.confidence} </span>)}
                          {m.response_time && (<span>· Temps: {m.response_time}s</span>)}
                        </div>
                      )}
                    </div>
                  ))}
                  {messages.length === 0 && (
                    <div className="text-sm text-slate-500">Aucun message</div>
                  )}
                </div>
              ) : (
                <div className="text-sm text-slate-500">Choisissez une conversation dans la liste à gauche.</div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

