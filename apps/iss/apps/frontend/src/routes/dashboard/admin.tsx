import { createFileRoute } from '@tanstack/react-router'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { StatCard } from '@/components/dashboard/StatCard'
import { ChartCard } from '@/components/dashboard/ChartCard'
import { QuickAction } from '@/components/dashboard/QuickAction'
import { Button } from '@/components/ui/button'
import { 
  Users, 
  Activity,
  FileText,
  Calendar,
  Shield,
  Plus,
  Settings
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

  // Dati mock per grafici
  const userGrowthData = [
    { name: 'Gen', value: 400 },
    { name: 'Feb', value: 300 },
    { name: 'Mar', value: 600 },
    { name: 'Apr', value: 800 },
    { name: 'Mag', value: 500 },
    { name: 'Giu', value: 700 }
  ]

  const projectsData = [
    { name: 'Attivi', value: 25 },
    { name: 'Completati', value: 15 },
    { name: 'In Pausa', value: 5 }
  ]

  const handleQuickAction = (action: string) => {
    console.log(`Quick action: ${action}`)
  }

  return (
    <DashboardLayout 
      title="Dashboard Admin" 
      description="Pannello di controllo amministrativo completo"
      userRole="admin"
      action={
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nuova Azione
        </Button>
      }
    >
      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Utenti Totali"
          value={stats.totalUsers.toLocaleString()}
          change="+12.5%"
          trend="up"
          icon={Users}
        />
        <StatCard
          title="Utenti Attivi"
          value={stats.activeUsers.toLocaleString()}
          change="+8.2%"
          trend="up"
          icon={Activity}
        />
        <StatCard
          title="Progetti"
          value={stats.totalProjects}
          change="+5.1%"
          trend="up"
          icon={FileText}
        />
        <StatCard
          title="Eventi"
          value={stats.totalEvents}
          change="-2.1%"
          trend="down"
          icon={Calendar}
        />
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <ChartCard
          title="Crescita Utenti"
          description="Andamento registrazioni mensili"
          data={userGrowthData}
          type="line"
        />
        <ChartCard
          title="Distribuzione Progetti"
          description="Status progetti attuali"
          data={projectsData}
          type="pie"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <QuickAction
          title="Gestione Utenti"
          description="Aggiungi, modifica, elimina utenti"
          icon={Users}
          onClick={() => handleQuickAction('users')}
          variant="primary"
        />
        <QuickAction
          title="Gestione Bandi"
          description="Pubblica e gestisci bandi"
          icon={FileText}
          onClick={() => handleQuickAction('bandi')}
          variant="secondary"
        />
        <QuickAction
          title="Sistema"
          description="Configurazioni e backup"
          icon={Settings}
          onClick={() => handleQuickAction('system')}
          variant="default"
        />
        <QuickAction
          title="Sicurezza"
          description="Log di accesso e audit"
          icon={Shield}
          onClick={() => handleQuickAction('security')}
          variant="destructive"
        />
      </div>
    </DashboardLayout>
  )
}
