import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export const Route = createFileRoute('/progetti')({
  component: ProgettiPage,
})

function ProgettiPage() {
  const [progetti, setProgetti] = useState([])

  useEffect(() => {
    // Mock data
    setProgetti([
      {
        id: 1,
        nome: "Digital Bridge Campania",
        descrizione_breve: "Ridurre il digital divide nelle aree rurali campane",
        stato: "in_corso",
        budget_totale: 150000,
        data_inizio: "2025-01-15",
        team_size: 8,
        impatto_sociale: "2000+ cittadini raggiunti"
      },
      {
        id: 2,
        nome: "APS Tech Hub",
        descrizione_breve: "Piattaforma tecnologica per il terzo settore",
        stato: "in_corso",
        budget_totale: 80000,
        data_inizio: "2025-03-01",
        team_size: 5,
        impatto_sociale: "500+ APS supportate"
      }
    ])
  }, [])

  const getStatoColor = (stato) => {
    switch (stato) {
      case 'in_corso': return 'bg-blue-100 text-blue-800'
      case 'completato': return 'bg-green-100 text-green-800'
      case 'pianificato': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-green-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🚀 Progetti <span className="text-[#f4af00]">ISS</span>
          </h1>
          <p className="text-xl">Innovazione sociale per la Campania</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {progetti.map((progetto) => (
            <Card key={progetto.id} className="p-6 bg-white/90">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold">{progetto.nome}</h3>
                <Badge className={getStatoColor(progetto.stato)}>
                  {progetto.stato.replace('_', ' ')}
                </Badge>
              </div>
              
              <p className="text-gray-600 mb-4">{progetto.descrizione_breve}</p>
              
              <div className="space-y-2 mb-4">
                <div className="text-sm text-gray-600">
                  💰 Budget: €{progetto.budget_totale.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600">
                  👥 Team: {progetto.team_size} persone
                </div>
                <div className="text-sm text-gray-600">
                  📈 {progetto.impatto_sociale}
                </div>
              </div>
              
              <Button className="w-full bg-[#7a2426] hover:bg-[#a53327]">
                Scopri di più
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
