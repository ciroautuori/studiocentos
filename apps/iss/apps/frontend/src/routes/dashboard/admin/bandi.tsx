import { createFileRoute } from '@tanstack/react-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  FileText, 
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Edit,
  Trash2,
  Eye,
  Calendar,
  Euro,
  Users,
  Clock
} from 'lucide-react'
import { useState, useEffect } from 'react'
import { bandoService } from '@/services/api'
import type { Bando } from '@/types/api'

export const Route = createFileRoute('/dashboard/admin/bandi')({
  component: BandiManagement,
})

function BandiManagement() {
  const [bandi, setBandi] = useState<Bando[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadBandi = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await bandoService.search({ limit: 50 })
        setBandi(response.results || response.bandi || [])
      } catch (err: any) {
        console.error('Errore caricamento bandi:', err)
        setError('Errore nel caricamento dei bandi')
      } finally {
        setLoading(false)
      }
    }

    loadBandi()
  }, [])

  const getStatoColor = (stato: string) => {
    switch (stato) {
      case 'ATTIVO':
        return 'bg-green-100 text-green-800'
      case 'SCADUTO':
        return 'bg-red-100 text-red-800'
      case 'SOSPESO':
        return 'bg-yellow-100 text-yellow-800'
      case 'BOZZA':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getCategoriaColor = (categoria: string) => {
    switch (categoria) {
      case 'Innovazione':
        return 'bg-blue-100 text-blue-800'
      case 'Sociale':
        return 'bg-purple-100 text-purple-800'
      case 'Digitale':
        return 'bg-cyan-100 text-cyan-800'
      case 'Giovani':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredBandi = bandi.filter((bando: Bando) =>
    bando.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bando.descrizione?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bando.ente?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const stats = {
    total: bandi.length,
    attivi: bandi.filter((b: Bando) => b.status === 'attivo').length,
    scaduti: bandi.filter((b: Bando) => b.status === 'scaduto').length,
    importoTotale: bandi.reduce((sum: number, b: Bando) => sum + (parseFloat(b.importo?.replace(/[^0-9.-]/g, '') || '0') || 0), 0),
    candidatureTotali: 0 // Non disponibile nel modello attuale
  }

  const isScadenzaVicina = (scadenza: string) => {
    const oggi = new Date()
    const dataScadenza = new Date(scadenza)
    const diffTime = dataScadenza.getTime() - oggi.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays <= 30 && diffDays > 0
  }

  return (
    <DashboardLayout
      userRole="admin"
      title="Gestione Bandi"
      description="Gestisci tutti i bandi e le opportunità di finanziamento"
      action={
        <Button className="bg-red-600 hover:bg-red-700">
          <Plus className="h-4 w-4 mr-2" />
          Nuovo Bando
        </Button>
      }
    >
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bandi Totali</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-muted-foreground">Pubblicati sulla piattaforma</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bandi Attivi</CardTitle>
            <FileText className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.attivi}</div>
            <p className="text-xs text-muted-foreground">Aperti per candidature</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Importo Totale</CardTitle>
            <Euro className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">€{stats.importoTotale.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Valore complessivo</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Candidature</CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">{stats.candidatureTotali}</div>
            <p className="text-xs text-muted-foreground">Richieste ricevute</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Scaduti</CardTitle>
            <Clock className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.scaduti}</div>
            <p className="text-xs text-muted-foreground">Termine scaduto</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardHeader>
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <CardTitle>Lista Bandi</CardTitle>
            <div className="flex gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Cerca bandi..."
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
              {[...Array(4)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-24 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {filteredBandi.map((bando: Bando) => (
                <div key={bando.id} className="border rounded-lg p-6 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-lg font-semibold">{bando.title}</h3>
                        <Badge className={getStatoColor(bando.status?.toUpperCase() || 'ATTIVO')}>
                          {bando.status?.toUpperCase() || 'ATTIVO'}
                        </Badge>
                        <Badge className={getCategoriaColor(bando.categoria || 'Generale')}>
                          {bando.categoria || 'Generale'}
                        </Badge>
                        {bando.scadenza && isScadenzaVicina(bando.scadenza) && (
                          <Badge className="bg-orange-100 text-orange-800">
                            <Clock className="h-3 w-3 mr-1" />
                            Scadenza vicina
                          </Badge>
                        )}
                      </div>
                      <p className="text-muted-foreground mb-3">{bando.descrizione}</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="font-medium">Importo:</span>
                          <p className="text-green-600 font-semibold">{bando.importo || 'Non specificato'}</p>
                        </div>
                        <div>
                          <span className="font-medium">Scadenza:</span>
                          <p className={bando.scadenza && isScadenzaVicina(bando.scadenza) ? 'text-orange-600 font-semibold' : ''}>
                            {bando.scadenza ? new Date(bando.scadenza).toLocaleDateString('it-IT') : bando.scadenza_raw || 'Non specificata'}
                          </p>
                        </div>
                        <div>
                          <span className="font-medium">Ente:</span>
                          <p>{bando.ente}</p>
                        </div>
                        <div>
                          <span className="font-medium">Fonte:</span>
                          <p className="text-blue-600 font-semibold">{bando.fonte}</p>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
