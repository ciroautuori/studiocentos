import { createFileRoute } from '@tanstack/react-router'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Building, 
  Users, 
  TrendingUp,
  DollarSign,
  Target,
  Clock,
  BarChart3,
  Handshake,
  PlusCircle
} from 'lucide-react'

export const Route = createFileRoute('/dashboard/partner')({
  component: PartnerDashboard,
})

function PartnerDashboard() {
  const partnerStats = {
    activeProjects: 7,
    completedProjects: 12,
    totalBudget: 450000,
    teamMembers: 25,
    impact: 85
  }

  const activeProjects = [
    { name: "Progetto Inclusione Digitale", progress: 75, budget: 85000, deadline: "15 Nov 2025", team: 8 },
    { name: "Workshop Sostenibilità", progress: 45, budget: 35000, deadline: "30 Dic 2025", team: 5 },
    { name: "Formazione Giovani", progress: 90, budget: 60000, deadline: "10 Gen 2026", team: 12 }
  ]

  return (
    <DashboardLayout
      userRole="partner"
      title="Dashboard Partner"
      description="Area riservata per la gestione delle partnership e collaborazioni"
      action={
        <Button className="bg-purple-600 hover:bg-purple-700">
          <PlusCircle className="h-4 w-4 mr-2" />
          Nuovo Progetto
        </Button>
      }
    >

  const quickActions = [
    {
      title: "Nuovo Progetto",
      description: "Avvia una nuova collaborazione",
      icon: PlusCircle,
      onClick: () => console.log("Nuovo progetto")
    },
    {
      title: "Gestione Team",
      description: "Organizza il tuo team",
      icon: Users,
      onClick: () => console.log("Gestione team")
    },
    {
      title: "Analytics",
      description: "Visualizza report e metriche",
      icon: BarChart3,
      onClick: () => console.log("Analytics")
    },
    {
      title: "Collaborazioni",
      description: "Gestisci partnership attive",
      icon: Handshake,
      onClick: () => console.log("Collaborazioni")
    }
  ]

  const activeProjects = [
    { name: "Progetto Inclusione Digitale", progress: 75, budget: 85000, deadline: "15 Nov 2025", team: 8 },
    { name: "Workshop Sostenibilità", progress: 45, budget: 35000, deadline: "30 Dic 2025", team: 5 },
    { name: "Formazione Giovani", progress: 90, budget: 60000, deadline: "10 Gen 2026", team: 12 }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-purple-600">Dashboard Partner</h1>
          <p className="text-muted-foreground">
            Area riservata per la gestione delle partnership e collaborazioni
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Building className="h-4 w-4 mr-2" />
            Profilo Organizzazione
          </Button>
          <Button size="sm" className="bg-purple-600 hover:bg-purple-700">
            <PlusCircle className="h-4 w-4 mr-2" />
            Nuovo Progetto
          </Button>
        </div>
      </div>

      {/* Partner Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Progetti Attivi</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{partnerStats.activeProjects}</div>
            <p className="text-xs text-muted-foreground">
              {partnerStats.completedProjects} completati
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Budget Totale</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">€{partnerStats.totalBudget.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 inline mr-1" />
              +15% rispetto al trimestre scorso
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Team Members</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{partnerStats.teamMembers}</div>
            <p className="text-xs text-muted-foreground">
              Collaboratori attivi
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Impact Score</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{partnerStats.impact}%</div>
            <Progress value={partnerStats.impact} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-1">
              Impatto sociale misurato
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Azioni Rapide</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <Card key={index} className="cursor-pointer hover:shadow-md transition-shadow" onClick={action.onClick}>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-purple-100 text-purple-600">
                    <action.icon className="h-5 w-5" />
                  </div>
                  <div>
                    <CardTitle className="text-sm">{action.title}</CardTitle>
                    <p className="text-xs text-muted-foreground">{action.description}</p>
                  </div>
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>

      {/* Active Projects */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Progetti Attivi</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {activeProjects.map((project, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="text-lg">{project.name}</CardTitle>
                <CardDescription>Budget: €{project.budget.toLocaleString()}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span>Progresso</span>
                    <span>{project.progress}%</span>
                  </div>
                  <Progress value={project.progress} />
                  <div className="flex items-center justify-between text-sm">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      Scadenza: {project.deadline}
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {project.team} membri
                    </span>
                  </div>
                  <Button size="sm" className="w-full">
                    Gestisci Progetto
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Partnership Overview */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Partnership Attive</h2>
        <Card>
          <CardHeader>
            <CardTitle>Collaborazioni in Corso</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { partner: "ISS Salerno", type: "Formazione", status: "Attiva", value: "€45,000" },
                { partner: "Comune di Salerno", type: "Progetti Sociali", status: "In Sviluppo", value: "€80,000" },
                { partner: "Università Campus", type: "Ricerca", status: "Attiva", value: "€25,000" },
                { partner: "Fondazione Sud", type: "Innovazione", status: "Pianificazione", value: "€60,000" }
              ].map((partnership, index) => (
                <div key={index} className="flex items-center justify-between border-b pb-2">
                  <div className="flex items-center gap-3">
                    <div className="p-1 rounded-full bg-purple-100">
                      <Handshake className="h-3 w-3 text-purple-600" />
                    </div>
                    <div>
                      <p className="font-medium">{partnership.partner}</p>
                      <p className="text-sm text-muted-foreground">{partnership.type} • {partnership.value}</p>
                    </div>
                  </div>
                  <Badge 
                    variant={partnership.status === 'Attiva' ? 'default' : 'secondary'}
                  >
                    {partnership.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
