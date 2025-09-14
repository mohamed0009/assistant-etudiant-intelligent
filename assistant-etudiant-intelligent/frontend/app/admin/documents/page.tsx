"use client"

import { useEffect, useRef, useState } from "react"
import Link from "next/link"
import { apiService } from "@/lib/api"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { RefreshCw, Upload, Trash2, ArrowLeft, Shield } from "lucide-react"

type AdminDoc = { filename: string; size: number; modified: number }

export default function AdminDocumentsPage() {
  const [docs, setDocs] = useState<AdminDoc[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const fileRef = useRef<HTMLInputElement>(null)
  const [user, setUser] = useState<{ name?: string } | null>(null)

  const loadDocs = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const res = await apiService.listAdminDocuments()
      setDocs(res.documents)
    } catch (e: any) {
      setError("Impossible de charger les documents")
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpload = async (file?: File) => {
    if (!file) return
    try {
      setIsLoading(true)
      await apiService.uploadAdminDocument(file)
      await loadDocs()
    } catch (e: any) {
      setError("Échec du téléversement")
      setIsLoading(false)
    }
  }

  const handleDelete = async (filename: string) => {
    try {
      setIsLoading(true)
      await apiService.deleteAdminDocument(filename)
      await loadDocs()
    } catch (e: any) {
      setError("Échec de la suppression")
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadDocs()
    try {
      const stored = localStorage.getItem('user')
      if (stored) setUser(JSON.parse(stored))
    } catch (_) {}
  }, [])

  const formatSize = (bytes: number) => {
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
  }

  return (
    <div className="min-h-dvh pt-24">
      <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="max-w-7xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary rounded-xl shadow-lg">
                <Shield className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Gestion des Documents</h1>
                <p className="text-foreground/70">Téléverser, lister et supprimer les fichiers de la base</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-foreground/70">{user?.name ? `Connecté en tant que ${user.name}` : ''}</span>
              <Link href="/admin">
                <Button variant="outline"><ArrowLeft className="w-4 h-4 mr-2" />Retour</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>
      <div className="max-w-7xl mx-auto px-4 space-y-6">
        <div className="flex items-center justify-end">
          <div className="flex items-center gap-3">
            <Button onClick={loadDocs} variant="outline"><RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''} mr-2`} />Actualiser</Button>
            <Button onClick={() => fileRef.current?.click()}><Upload className="w-4 h-4 mr-2" />Téléverser</Button>
            <input ref={fileRef} type="file" className="hidden" accept=".pdf,.doc,.docx,.txt" onChange={(e)=>handleUpload(e.target.files?.[0])} />
          </div>
        </div>

        <Card className="p-6 rounded-xl border bg-card shadow-sm">
          {error && <div className="mb-4 text-sm text-red-600">{error}</div>}
          {isLoading ? (
            <div className="py-12 text-center text-foreground/70">Chargement...</div>
          ) : docs.length === 0 ? (
            <div className="py-12 text-center text-foreground/70">Aucun document</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-sm text-foreground/70 border-b">
                    <th className="py-3 px-4">Fichier</th>
                    <th className="py-3 px-4">Taille</th>
                    <th className="py-3 px-4">Modifié</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {docs.map((d) => (
                    <tr key={d.filename} className="border-b last:border-0">
                      <td className="py-3 px-4 font-medium text-foreground">{d.filename}</td>
                      <td className="py-3 px-4 text-foreground/70">{formatSize(d.size)}</td>
                      <td className="py-3 px-4 text-foreground/70">{new Date(d.modified * 1000).toLocaleString()}</td>
                      <td className="py-3 px-4 text-right">
                        <Button variant="outline" className="text-red-600 hover:text-red-700" onClick={() => handleDelete(d.filename)}>
                          <Trash2 className="w-4 h-4 mr-2" />Supprimer
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}


