import { createFileRoute } from '@tanstack/react-router'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { StatCard } from '@/components/dashboard/StatCard'
import { ChartCard } from '@/components/dashboard/ChartCard'
import { QuickAction } from '@/components/dashboard/QuickAction'
import { Button } from '@/components/ui/button'
import { 
  Building,
  Users,
  FileText,
  BarChart3,
  Target,
  TrendingUp,
  Handshake,
  Mail,
  Plus,
  FolderOpen
} from 'lucide-react'

export const Route = createFileRoute('/dashboard/partner')({
  component: PartnerDashboard,
})

function PartnerDashboard() {
  const partnerStats = {
    totalProjects: 25,
    activeCollaborations: 8,
    teamMembers: 45,
    completedProjects: 67,
    revenue: 156000,
    growth: 18.5
  }

  // Dati per grafici
  const projectsData = [
    { name: 'Gen', value: 12 },
    { name: 'Feb', value: 19 },
    { name: 'Mar', value: 25 },
    { name: 'Apr', value: 22 },
    { name: 'Mag', value: 30 },
    { name: 'Giu', value: 35 }
  ]

  const collaborationsData = [
    { name: 'APS Locali', value: 15 },
    { name: 'Enti Pubblici', value: 8 },
    { name: 'Aziende', value: 12 },
    { name: 'Fondazioni', value: 5 }
  ]

  const handleQuickAction = (action: string) => {
    console.log(`Partner quick action: ${action}`)
  }

  return (
    <DashboardLayout 
      title="Dashboard Partner" 
      description="Gestisci collaborazioni e progetti partnership"
      userRole="partner"
      action={
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nuovo Progetto
        </Button>
      }
    >
      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Progetti Attivi"
          value={partnerStats.totalProjects}
          change="+15.2%"
          trend="up"
          icon={Target}
        />
        <StatCard
          title="Collaborazioni"
          value={partnerStats.activeCollaborations}
          change="+3 questo mese"
          trend="up"
          icon={Handshake}
        />
        <StatCard
          title="Team Members"
          value={partnerStats.teamMembers}
          change="+8 new"
          trend="up"
          icon={Users}
        />
        <StatCard
          title="Progetti Completati"
          value={partnerStats.completedProjects}
          change={`+${partnerStats.growth}%`}
          trend="up"
          icon={FileText}
        />
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <ChartCard
          title="Crescita Progetti"
          description="Andamento progetti mensili"
          data={projectsData}
          type="line"
        />
        <ChartCard
          title="Tipologie Collaborazioni"
          description="Distribuzione partner per categoria"
          data={collaborationsData}
          type="pie"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <QuickAction
          title="I Miei Progetti"
          description="Gestisci i tuoi progetti attivi"
          icon={Target}
          onClick={() => handleQuickAction('projects')}
          variant="primary"
        />
        <QuickAction
          title="Team Management"
          description="Gestisci membri del team"
          icon={Users}
          onClick={() => handleQuickAction('team')}
          variant="secondary"
        />
        <QuickAction
          title="Documenti"
          description="Contratti e documentazione"
          icon={FolderOpen}
          onClick={() => handleQuickAction('documents')}
          variant="default"
        />
        <QuickAction
          title="Analytics"
          description="Report e statistiche avanzate"
          icon={BarChart3}
          onClick={() => handleQuickAction('analytics')}
          variant="destructive"
        />
      </div>
    </DashboardLayout>
  )
}
