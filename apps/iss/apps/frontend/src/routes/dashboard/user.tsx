import { createFileRoute } from '@tanstack/react-router'
import { DashboardLayout } from '@/components/dashboard/DashboardLayout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Calendar,
  Heart,
  Trophy,
  TrendingUp,
  Clock,
  GraduationCap,
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

  const activeCourses = [
    { title: "Gestione Progetti Sociali", progress: 75, nextLesson: "Domani", instructor: "Prof. Bianchi" },
    { title: "Comunicazione Digitale", progress: 45, nextLesson: "Martedì", instructor: "Dott.ssa Verde" },
    { title: "Leadership Sociale", progress: 30, nextLesson: "Giovedì", instructor: "Prof. Rossi" }
  ]

  return (
    <DashboardLayout
      userRole="user"
      title="Dashboard Utente"
      description="Benvenuto nella tua area personale per crescita e partecipazione sociale"
      action={
        <Button className="bg-green-600 hover:bg-green-700">
          <Plus className="h-4 w-4 mr-2" />
          Nuova Attività
        </Button>
      }
    >
      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Corsi Completati</CardTitle>
            <GraduationCap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{userStats.completedCourses}/{userStats.totalCourses}</div>
            <Progress value={(userStats.completedCourses / userStats.totalCourses) * 100} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-1">
              {Math.round((userStats.completedCourses / userStats.totalCourses) * 100)}% completato
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Eventi Partecipati</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{userStats.eventsAttended}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 inline mr-1" />
              +3 questo mese
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ore Volontariato</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{userStats.volunteeringHours}h</div>
            <p className="text-xs text-muted-foreground">
              Contributo alla comunità
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Livello & Punti</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Livello {userStats.level}</div>
            <Progress value={(userStats.points / userStats.nextLevelPoints) * 100} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-1">
              {userStats.points}/{userStats.nextLevelPoints} punti
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Active Courses */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Corsi in Corso</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {activeCourses.map((course, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="text-lg">{course.title}</CardTitle>
                <CardDescription>Istruttore: {course.instructor}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span>Progresso</span>
                    <span>{course.progress}%</span>
                  </div>
                  <Progress value={course.progress} />
                  <div className="flex items-center justify-between text-sm">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      Prossima lezione: {course.nextLesson}
                    </span>
                  </div>
                  <Button size="sm" className="w-full">
                    Continua Corso
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Attività Recenti</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { title: "Corso di Innovazione Sociale", status: "completato", date: "2 giorni fa" },
              { title: "Workshop Sostenibilità", status: "partecipato", date: "1 settimana fa" },
              { title: "Assistenza Anziani", status: "volontariato", date: "2 settimane fa" },
              { title: "Badge Volontario Attivo", status: "achievement", date: "3 settimane fa" }
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between border-b pb-2">
                <div>
                  <p className="font-medium">{activity.title}</p>
                  <p className="text-sm text-muted-foreground">{activity.status}</p>
                </div>
                <Badge variant="outline">{activity.date}</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
