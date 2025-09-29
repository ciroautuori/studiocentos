import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useEffect } from 'react'

export const Route = createFileRoute('/dashboard/')({
  component: DashboardOverview,
})

function DashboardOverview() {
  const navigate = useNavigate()

  useEffect(() => {
    // Reindirizza automaticamente alla dashboard admin per il testing
    navigate({ to: '/dashboard/admin' })
  }, [navigate])

  const dashboardTypes = [
    {
      title: "Dashboard Utente",
      description: "Area personale per utenti registrati",
      href: "/dashboard/user",
      icon: Users,
      color: "bg-green-50 border-green-200 hover:bg-green-100",
      iconColor: "text-green-600"
    },
    {
      title: "Dashboard Admin",
      description: "Pannello di controllo amministrativo",
      href: "/dashboard/admin", 
      icon: Users, // Dovrebbe essere Shield ma non è importato
      color: "bg-red-50 border-red-200 hover:bg-red-100",
      iconColor: "text-red-600"
    },
    {
      title: "Dashboard Partner",
      description: "Area riservata ai partner ISS",
      href: "/dashboard/partner",
      icon: Users, // Dovrebbe essere Handshake ma non è importato
      color: "bg-purple-50 border-purple-200 hover:bg-purple-100", 
      iconColor: "text-purple-600"
    }
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pt-20">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Dashboard ISS</h1>
          <p className="text-gray-600 text-lg">Seleziona il tipo di dashboard per accedere alla tua area riservata</p>
        </div>
        
        {/* Dashboard Types */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          {dashboardTypes.map((dashboard, index) => (
            <Card 
              key={index}
              className={`cursor-pointer transition-all duration-300 hover:shadow-lg ${dashboard.color}`}
              onClick={() => window.location.href = dashboard.href}
            >
              <CardHeader className="text-center pb-4">
                <div className={`w-16 h-16 mx-auto rounded-full bg-white flex items-center justify-center mb-4 shadow-sm`}>
                  <dashboard.icon className={`h-8 w-8 ${dashboard.iconColor}`} />
                </div>
                <CardTitle className="text-xl font-bold">{dashboard.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600 mb-4">{dashboard.description}</p>
                <div className="text-sm text-gray-500">
                  Clicca per accedere →
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick Stats */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-center mb-8">Statistiche Generali</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Utenti Registrati</CardTitle>
                <Users className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1,247</div>
                <p className="text-xs text-green-600 mt-1">+12% questo mese</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Corsi Attivi</CardTitle>
                <BookOpen className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">8</div>
                <p className="text-xs text-blue-600 mt-1">Tutti operativi</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Eventi Programmati</CardTitle>
                <Calendar className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">15</div>
                <p className="text-xs text-purple-600 mt-1">Prossimo: 28 Set</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Progetti Attivi</CardTitle>
                <Rocket className="h-4 w-4 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-orange-600 mt-1">In sviluppo</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
