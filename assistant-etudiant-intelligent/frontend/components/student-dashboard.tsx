"use client"

import { useState } from "react"
import { StudentAssistant } from "@/components/student-assistant"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { LayoutDashboard, MessageSquare, BookOpen, Calendar, User, LogOut, Bell, Clock, TrendingUp } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"

export function StudentDashboard() {
  const [activeView, setActiveView] = useState<"assistant" | "dashboard">("dashboard")
  const { auth, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-lg">U</span>
              </div>
              <div>
                <h1 className="text-xl font-semibold text-slate-900">Assistant Étudiant Intelligent</h1>
                <p className="text-sm text-slate-600">Université de Technologie</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex gap-2">
                <Button
                  variant={activeView === "dashboard" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setActiveView("dashboard")}
                  className="h-9"
                >
                  <LayoutDashboard className="h-4 w-4 mr-2" />
                  Dashboard
                </Button>
                <Button
                  variant={activeView === "assistant" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setActiveView("assistant")}
                  className="h-9"
                >
                  <MessageSquare className="h-4 w-4 mr-2" />
                  Assistant IA
                </Button>
              </div>

              <div className="flex items-center gap-3">
                <Button variant="ghost" size="sm" className="relative">
                  <Bell className="h-4 w-4" />
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </Button>

                <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-900">{auth.user?.name}</p>
                    <p className="text-xs text-slate-500">
                      {auth.user?.studentId} • {auth.user?.department}
                    </p>
                  </div>
                  <Button variant="ghost" size="sm" onClick={logout}>
                    <LogOut className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      {activeView === "assistant" ? (
        <StudentAssistant />
      ) : (
        <div className="max-w-7xl mx-auto px-6 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-slate-900 mb-2">Bonjour, {auth.user?.name?.split(" ")[0]} 👋</h2>
            <p className="text-slate-600">Voici un aperçu de votre progression académique</p>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                  <Badge variant="secondary" className="bg-blue-200 text-blue-800">
                    Actif
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-900 mb-1">6</div>
                <p className="text-sm text-blue-700">Cours suivis</p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <Badge variant="secondary" className="bg-green-200 text-green-800">
                    +2.3
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-900 mb-1">14.2</div>
                <p className="text-sm text-green-700">Moyenne générale</p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <Clock className="h-5 w-5 text-orange-600" />
                  <Badge variant="secondary" className="bg-orange-200 text-orange-800">
                    Urgent
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-900 mb-1">3</div>
                <p className="text-sm text-orange-700">Devoirs à rendre</p>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <MessageSquare className="h-5 w-5 text-purple-600" />
                  <Badge variant="secondary" className="bg-purple-200 text-purple-800">
                    Nouveau
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-900 mb-1">127</div>
                <p className="text-sm text-purple-700">Questions posées</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Schedule */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Planning de la semaine
                </CardTitle>
                <CardDescription>Vos cours et examens à venir</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { time: "08:00 - 10:00", subject: "Mathématiques Appliquées", room: "Amphi A", type: "cours" },
                    { time: "10:15 - 12:15", subject: "Programmation Avancée", room: "Salle Info 2", type: "tp" },
                    { time: "14:00 - 16:00", subject: "Physique Quantique", room: "Amphi B", type: "cours" },
                    { time: "16:15 - 18:15", subject: "Projet Tutoré", room: "Salle Projet", type: "projet" },
                  ].map((event, index) => (
                    <div key={index} className="flex items-center gap-4 p-3 bg-slate-50 rounded-lg">
                      <div className="text-sm font-medium text-slate-600 w-24">{event.time}</div>
                      <div className="flex-1">
                        <p className="font-medium text-slate-900">{event.subject}</p>
                        <p className="text-sm text-slate-600">{event.room}</p>
                      </div>
                      <Badge
                        variant="outline"
                        className={
                          event.type === "cours"
                            ? "border-blue-200 text-blue-700"
                            : event.type === "tp"
                              ? "border-green-200 text-green-700"
                              : "border-purple-200 text-purple-700"
                        }
                      >
                        {event.type.toUpperCase()}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Actions rapides</CardTitle>
                <CardDescription>Accès direct aux fonctionnalités</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  className="w-full justify-start bg-transparent"
                  variant="outline"
                  onClick={() => setActiveView("assistant")}
                >
                  <MessageSquare className="h-4 w-4 mr-2" />
                  Poser une question à l'IA
                </Button>
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <BookOpen className="h-4 w-4 mr-2" />
                  Consulter mes cours
                </Button>
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <Calendar className="h-4 w-4 mr-2" />
                  Voir mon planning
                </Button>
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <User className="h-4 w-4 mr-2" />
                  Mon profil
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
