import { createFileRoute } from '@tanstack/react-router'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { StatCard } from '@/components/dashboard/StatCard'
import { ChartCard } from '@/components/dashboard/ChartCard'
import { QuickAction } from '@/components/dashboard/QuickAction'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Calendar,
  Heart,
  Trophy,
  GraduationCap,
  BookOpen,
  Mail,
  Plus
} from 'lucide-react'

export const Route = createFileRoute('/dashboard/user')({
  component: UserDashboard,
})

function UserDashboard() {
  const userStats = {
    completedCourses: 8,
    totalCourses: 12,
    eventsAttended: 15,
    volunteeringHours: 45,
    points: 2840,
    level: 4,
    nextLevelPoints: 3000
  }

  // Dati per grafici
  const progressData = [
    { name: 'Gen', value: 20 },
    { name: 'Feb', value: 35 },
    { name: 'Mar', value: 50 },
    { name: 'Apr', value: 65 },
    { name: 'Mag', value: 80 },
    { name: 'Giu', value: 95 }
  ]

  const activitiesData = [
    { name: 'Corsi', value: 8 },
    { name: 'Eventi', value: 15 },
    { name: 'Volontariato', value: 12 }
  ]

  const handleQuickAction = (action: string) => {
    console.log(`User quick action: ${action}`)
  }

  const completionPercentage = (userStats.completedCourses / userStats.totalCourses) * 100
  const levelProgress = (userStats.points / userStats.nextLevelPoints) * 100

  return (
    <DashboardLayout 
      title="Dashboard Utente" 
      description="Il tuo spazio personalizzato per corsi ed eventi"
      userRole="user"
      action={
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nuova Attività
        </Button>
      }
    >
      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Corsi Completati"
          value={`${userStats.completedCourses}/${userStats.totalCourses}`}
          change={`${completionPercentage.toFixed(0)}%`}
          trend="up"
          icon={GraduationCap}
        />
        <StatCard
          title="Eventi Partecipati"
          value={userStats.eventsAttended}
          change="+3 questo mese"
          trend="up"
          icon={Calendar}
        />
        <StatCard
          title="Ore Volontariato"
          value={userStats.volunteeringHours}
          change="+12 ore"
          trend="up"
          icon={Heart}
        />
        <StatCard
          title="Punti Esperienza"
          value={userStats.points.toLocaleString()}
          change={`Livello ${userStats.level}`}
          trend="up"
          icon={Trophy}
        />
      </div>

      {/* Progress Section */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GraduationCap className="h-5 w-5" />
              Progresso Corsi
            </CardTitle>
            <CardDescription>
              {userStats.completedCourses} di {userStats.totalCourses} corsi completati
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={completionPercentage} className="mb-2" />
            <p className="text-sm text-muted-foreground">
              {completionPercentage.toFixed(0)}% completato
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="h-5 w-5" />
              Avanzamento Livello
            </CardTitle>
            <CardDescription>
              {userStats.points} / {userStats.nextLevelPoints} punti per il livello {userStats.level + 1}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={levelProgress} className="mb-2" />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Livello {userStats.level}</span>
              <Badge variant="secondary">
                {userStats.nextLevelPoints - userStats.points} punti mancanti
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <ChartCard
          title="Progresso Mensile"
          description="Avanzamento nei corsi"
          data={progressData}
          type="line"
        />
        <ChartCard
          title="Attività per Tipo"
          description="Distribuzione delle tue attività"
          data={activitiesData}
          type="pie"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <QuickAction
          title="I Miei Corsi"
          description="Visualizza corsi attivi e completati"
          icon={BookOpen}
          onClick={() => handleQuickAction('courses')}
          variant="primary"
        />
        <QuickAction
          title="Prossimi Eventi"
          description="Eventi a cui partecipare"
          icon={Calendar}
          onClick={() => handleQuickAction('events')}
          variant="secondary"
        />
        <QuickAction
          title="Volontariato"
          description="Opportunità di volontariato"
          icon={Heart}
          onClick={() => handleQuickAction('volunteer')}
          variant="default"
        />
        <QuickAction
          title="Messaggi"
          description="4 messaggi non letti"
          icon={Mail}
          onClick={() => handleQuickAction('messages')}
          variant="destructive"
        />
      </div>
    </DashboardLayout>
  )
}
