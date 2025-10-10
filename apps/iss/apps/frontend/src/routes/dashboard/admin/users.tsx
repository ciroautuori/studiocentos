import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  Users, 
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Edit,
  Trash2,
  Mail,
  Phone,
  Calendar
} from 'lucide-react'
import { useState, useEffect } from 'react'

export const Route = createFileRoute('/dashboard/admin/users')({
  component: UsersManagement,
})

function UsersManagement() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  // Mock data - in realtà verrebbe dalle API
  const mockUsers = [
    {
      id: 1,
      nome: "Mario",
      cognome: "Rossi",
      email: "mario.rossi@email.it",
      telefono: "333-1234567",
      role: "cittadino",
      status: "ACTIVE",
      created_at: "2025-01-15",
      last_login: "2025-09-24"
    },
    {
      id: 2,
      nome: "Anna",
      cognome: "Verdi",
      email: "anna.verdi@email.it",
      telefono: "333-7654321",
      role: "volontario",
      status: "ACTIVE",
      created_at: "2025-02-20",
      last_login: "2025-09-23"
    },
    {
      id: 3,
      nome: "Luigi",
      cognome: "Bianchi",
      email: "luigi.bianchi@partner.it",
      telefono: "333-9876543",
      role: "aps_responsabile",
      status: "PENDING",
      created_at: "2025-03-10",
      last_login: "2025-09-20"
    },
    {
      id: 4,
      nome: "Sofia",
      cognome: "Neri",
      email: "sofia.neri@email.it",
      telefono: "333-5555555",
      role: "moderator",
      status: "ACTIVE",
      created_at: "2025-01-05",
      last_login: "2025-09-24"
    },
    {
      id: 5,
      nome: "Admin",
      cognome: "ISS",
      email: "admin@iss-aps.it",
      telefono: null,
      role: "admin",
      status: "ACTIVE",
      created_at: "2024-12-01",
      last_login: "2025-09-24"
    }
  ]

  useEffect(() => {
    // Simula caricamento API
    setTimeout(() => {
      setUsers(mockUsers)
      setLoading(false)
    }, 1000)
  }, [])

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'bg-red-100 text-red-800'
      case 'moderator':
        return 'bg-yellow-100 text-yellow-800'
      case 'aps_responsabile':
        return 'bg-purple-100 text-purple-800'
      case 'volontario':
        return 'bg-blue-100 text-blue-800'
      case 'cittadino':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'bg-green-100 text-green-800'
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800'
      case 'SUSPENDED':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredUsers = users.filter((user: any) =>
    user.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.cognome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const stats = {
    total: users.length,
    active: users.filter((u: any) => u.status === 'ACTIVE').length,
    pending: users.filter((u: any) => u.status === 'PENDING').length,
    admins: users.filter((u: any) => u.role === 'admin').length
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Gestione Utenti</h1>
          <p className="text-muted-foreground">Gestisci tutti gli utenti della piattaforma ISS</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nuovo Utente
        </Button>
      </div>
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Utenti Totali</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-muted-foreground">Registrati sulla piattaforma</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Utenti Attivi</CardTitle>
            <Users className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.active}</div>
            <p className="text-xs text-muted-foreground">Account verificati e attivi</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">In Attesa</CardTitle>
            <Users className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
            <p className="text-xs text-muted-foreground">Richiedono approvazione</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Amministratori</CardTitle>
            <Users className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.admins}</div>
            <p className="text-xs text-muted-foreground">Con privilegi amministrativi</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardHeader>
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <CardTitle>Lista Utenti</CardTitle>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Cerca utenti..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              <Button variant="outline">
                <Filter className="h-4 w-4 mr-2" />
                Filtri
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-16 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {filteredUsers.map((user: any) => (
                <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                      <Users className="h-5 w-5 text-gray-600" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium">{user.nome} {user.cognome}</h3>
                        <Badge className={getRoleColor(user.role)}>
                          {user.role}
                        </Badge>
                        <Badge className={getStatusColor(user.status)}>
                          {user.status}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Mail className="h-3 w-3" />
                          {user.email}
                        </span>
                        {user.telefono && (
                          <span className="flex items-center gap-1">
                            <Phone className="h-3 w-3" />
                            {user.telefono}
                          </span>
                        )}
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          Registrato: {new Date(user.created_at).toLocaleDateString('it-IT')}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Mail className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                    {user.role !== 'admin' && (
                      <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
