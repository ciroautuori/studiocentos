import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  BarChart3,
  CheckCircle,
  Activity,
  DollarSign,
  TrendingUp,
  Plus,
  Database,
  Settings,
  FileText,
  Calendar,
  Heart,
  Building,
  Shield,
  Bell,
  MoreHorizontal,
  Edit,
  Trash2,
  Mail,
  Phone
} from 'lucide-react'

export const Route = createFileRoute('/dashboard/admin')({
  component: AdminDashboard,
})

function AdminDashboard() {
  const stats = {
    totalUsers: 1247,
    activeUsers: 892,
    totalProjects: 45,
    totalEvents: 23,
    revenue: 125000,
    growth: 12.5
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="w-64 border-r bg-background flex flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-red-100 text-red-600">
              <Shield className="h-4 w-4" />
            </div>
            <div>
              <p className="text-sm font-medium">Admin</p>
              <p className="text-xs text-muted-foreground">Dashboard</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex-1 px-3 py-4 overflow-y-auto">
          <nav className="space-y-1">
            <a href="/dashboard/admin" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm bg-accent text-accent-foreground font-medium">
              <BarChart3 className="h-4 w-4" />
              <span>Dashboard</span>
            </a>
            <a href="/dashboard/admin/users" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Users className="h-4 w-4" />
              <span>Gestione Utenti</span>
              <Badge variant="secondary" className="h-5 text-xs ml-auto">5</Badge>
            </a>
            <a href="/dashboard/admin/bandi" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <FileText className="h-4 w-4" />
              <span>Gestione Bandi</span>
              <Badge variant="secondary" className="h-5 text-xs ml-auto">3</Badge>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Calendar className="h-4 w-4" />
              <span>Eventi & Corsi</span>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Heart className="h-4 w-4" />
              <span>Volontariato</span>
              <Badge variant="secondary" className="h-5 text-xs ml-auto">12</Badge>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Building className="h-4 w-4" />
              <span>Partner</span>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Database className="h-4 w-4" />
              <span>Sistema</span>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Shield className="h-4 w-4" />
              <span>Sicurezza</span>
              <Badge variant="secondary" className="h-5 text-xs ml-auto">2</Badge>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Bell className="h-4 w-4" />
              <span>Notifiche</span>
              <Badge variant="secondary" className="h-5 text-xs ml-auto">8</Badge>
            </a>
            <a href="#" className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground">
              <Settings className="h-4 w-4" />
              <span>Impostazioni</span>
            </a>
          </nav>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex h-16 items-center justify-between px-6">
            <h2 className="text-lg font-semibold">Dashboard Amministratore</h2>
            <Button className="bg-red-600 hover:bg-red-700">
              <Plus className="h-4 w-4 mr-2" />
              Nuova Azione
            </Button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          <div className="container mx-auto p-6">
            <div className="space-y-6">
              {/* Page Header */}
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Dashboard Amministratore</h1>
                <p className="text-muted-foreground">
                  Pannello di controllo per la gestione completa della piattaforma ISS
                </p>
              </div>

              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Utenti Totali</CardTitle>
                    <Users className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.totalUsers}</div>
                    <p className="text-xs text-muted-foreground">
                      <TrendingUp className="h-3 w-3 inline mr-1" />
                      +{stats.growth}% dal mese scorso
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Utenti Attivi</CardTitle>
                    <Activity className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.activeUsers}</div>
                    <p className="text-xs text-muted-foreground">
                      {Math.round((stats.activeUsers / stats.totalUsers) * 100)}% del totale
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Progetti Attivi</CardTitle>
                    <BarChart3 className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stats.totalProjects}</div>
                    <p className="text-xs text-muted-foreground">
                      In corso di realizzazione
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Budget Totale</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">€{stats.revenue.toLocaleString()}</div>
                    <p className="text-xs text-muted-foreground">
                      Valore progetti attivi
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* System Status */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="border-green-200 bg-green-50">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-green-800">Sistema</CardTitle>
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-900">Operativo</div>
                    <p className="text-xs text-green-600">Tutti i servizi attivi</p>
                  </CardContent>
                </Card>

                <Card className="border-blue-200 bg-blue-50">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-blue-800">Database</CardTitle>
                    <Database className="h-4 w-4 text-blue-600" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-blue-900">98.5%</div>
                    <p className="text-xs text-blue-600">Performance ottimale</p>
                  </CardContent>
                </Card>

                <Card className="border-orange-200 bg-orange-50">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-orange-800">API</CardTitle>
                    <Activity className="h-4 w-4 text-orange-600" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-orange-900">2.1s</div>
                    <p className="text-xs text-orange-600">Tempo risposta medio</p>
                  </CardContent>
                </Card>
              </div>

              {/* Recent Activity */}
              <Card>
                <CardHeader>
                  <CardTitle>Attività Recenti</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { action: "Nuovo utente registrato", user: "Mario Rossi", time: "2 minuti fa" },
                      { action: "Progetto approvato", user: "Sistema", time: "15 minuti fa" },
                      { action: "Backup completato", user: "Sistema", time: "1 ora fa" },
                      { action: "Utente sospeso", user: "Admin", time: "2 ore fa" }
                    ].map((activity, index) => (
                      <div key={index} className="flex items-center justify-between border-b pb-2">
                        <div>
                          <p className="font-medium">{activity.action}</p>
                          <p className="text-sm text-muted-foreground">da {activity.user}</p>
                        </div>
                        <Badge variant="outline">{activity.time}</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
