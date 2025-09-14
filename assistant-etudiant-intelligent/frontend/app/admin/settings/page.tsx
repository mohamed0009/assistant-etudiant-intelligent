"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowLeft, Shield, Save } from "lucide-react"
import { apiService, SystemSettings } from "@/lib/api"

export default function AdminSettingsPage() {
  const [user, setUser] = useState<{ name?: string } | null>(null)
  const [settings, setSettings] = useState<SystemSettings | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    const loadData = async () => {
      try {
        const stored = localStorage.getItem('user')
        if (stored) setUser(JSON.parse(stored))
        
        const systemSettings = await apiService.getSystemSettings()
        setSettings(systemSettings)
      } catch (error) {
        console.error('Erreur lors du chargement des paramètres:', error)
      } finally {
        setIsLoading(false)
      }
    }
    
    loadData()
  }, [])

  const saveSettings = async () => {
    if (!settings) return
    
    try {
      setIsSaving(true)
      await apiService.updateSystemSettings(settings)
      alert('Paramètres enregistrés avec succès!')
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error)
      alert('Erreur lors de la sauvegarde des paramètres')
    } finally {
      setIsSaving(false)
    }
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
                <h1 className="text-2xl font-bold text-foreground">Configuration système</h1>
                <p className="text-foreground/70">Paramètres RAG et intégrations</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-foreground/70">{user?.name ? `Connecté en tant que ${user.name}` : ''}</span>
              <Link href="/admin"><Button variant="outline"><ArrowLeft className="w-4 h-4 mr-2" />Retour</Button></Link>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 space-y-6">
        <Card className="p-6 rounded-xl border bg-card shadow-sm">
          <h2 className="text-lg font-semibold text-foreground mb-4">Modèle et Recherche</h2>
          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-slate-600">Chargement des paramètres...</p>
            </div>
          ) : settings ? (
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm text-foreground/70">Utiliser OpenAI</label>
                <div className="flex items-center gap-3">
                  <input 
                    type="checkbox" 
                    checked={settings.use_openai} 
                    onChange={(e) => setSettings({...settings, use_openai: e.target.checked})} 
                  />
                  <span className="text-sm">Activer l'usage d'OpenAI au lieu d'HuggingFace</span>
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm text-foreground/70">k (documents retournés)</label>
                <Input 
                  type="number" 
                  value={settings.top_k} 
                  onChange={(e) => setSettings({...settings, top_k: parseInt(e.target.value || '0')})} 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm text-foreground/70">Taille des chunks</label>
                <Input 
                  type="number" 
                  value={settings.chunk_size} 
                  onChange={(e) => setSettings({...settings, chunk_size: parseInt(e.target.value || '0')})} 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm text-foreground/70">Chevauchement des chunks</label>
                <Input 
                  type="number" 
                  value={settings.chunk_overlap} 
                  onChange={(e) => setSettings({...settings, chunk_overlap: parseInt(e.target.value || '0')})} 
                />
              </div>
              <div className="space-y-2 md:col-span-2">
                <label className="text-sm text-foreground/70">Clé OpenAI (optionnel)</label>
                <Input 
                  type="password" 
                  placeholder="sk-..." 
                  value={settings.openai_key || ''} 
                  onChange={(e) => setSettings({...settings, openai_key: e.target.value})} 
                />
              </div>
              <div className="space-y-2 md:col-span-2">
                <label className="text-sm text-foreground/70">Modèle d'embedding</label>
                <Input 
                  value={settings.model_name} 
                  onChange={(e) => setSettings({...settings, model_name: e.target.value})} 
                />
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-red-600">Erreur lors du chargement des paramètres</p>
            </div>
          )}
          <div className="mt-6">
            <Button 
              onClick={saveSettings} 
              disabled={isSaving || !settings}
            >
              <Save className="w-4 h-4 mr-2" />
              {isSaving ? 'Enregistrement...' : 'Enregistrer'}
            </Button>
          </div>
        </Card>
      </div>
    </div>
  )
}



