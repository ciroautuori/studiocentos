import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export const Route = createFileRoute('/volontariato')({
  component: VolontariatoPage,
})

function VolontariatoPage() {
  const [opportunita, setOpportunita] = useState([])

  useEffect(() => {
    const loadOpportunita = async () => {
      try {
        // TODO: Implement API call when available
        // const response = await apiService.getOpportunitaVolontariato({ limit: 20 })
        // setOpportunita(response.items || [])
        
        // Fallback data per ora
        setOpportunita([
          {
            id: 1,
            titolo: "Supporto Digitale Anziani",
            descrizione_breve: "Aiuta gli anziani ad usare smartphone e computer",
            tipo_impegno: "continuativo",
            ore_settimanali: 4,
            skills_richieste: ["Pazienza", "Comunicazione", "Informatica base"],
            luogo: "Salerno",
            candidature_aperte: true,
            match_score: 95
          },
          {
            id: 2,
            titolo: "Sviluppatore Web Volontario", 
            descrizione_breve: "Sviluppa siti web per piccole APS campane",
            tipo_impegno: "progetto",
            ore_settimanali: 6,
            skills_richieste: ["React", "JavaScript", "CSS"],
            luogo: "Remote",
            candidature_aperte: true,
            match_score: 88
          }
        ])
      } catch (err) {
        console.error('Errore caricamento volontariato:', err)
      }
    }
    
    loadOpportunita()
  }, [])

  const getTipoColor = (tipo) => {
    switch (tipo) {
      case 'continuativo': return 'bg-blue-100 text-blue-800'
      case 'progetto': return 'bg-purple-100 text-purple-800'
      case 'evento': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-orange-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🤝 Volontariato <span className="text-[#f4af00]">Digitale</span>
          </h1>
          <p className="text-xl">Metti le tue competenze al servizio del sociale</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {opportunita.map((opp) => (
            <Card key={opp.id} className="p-6 bg-white/90">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold">{opp.titolo}</h3>
                <div className="flex gap-2">
                  <Badge className={getTipoColor(opp.tipo_impegno)}>
                    {opp.tipo_impegno}
                  </Badge>
                  {opp.match_score > 80 && (
                    <Badge className="bg-green-100 text-green-800">
                      {opp.match_score}% Match
                    </Badge>
                  )}
                </div>
              </div>
              
              <p className="text-gray-600 mb-4">{opp.descrizione_breve}</p>
              
              <div className="space-y-2 mb-4">
                <div className="text-sm text-gray-600">
                  ⏰ {opp.ore_settimanali} ore/settimana
                </div>
                <div className="text-sm text-gray-600">
                  📍 {opp.luogo}
                </div>
                <div className="text-sm text-gray-600">
                  🛠️ Skills: {opp.skills_richieste.join(', ')}
                </div>
              </div>
              
              <Button 
                className="w-full bg-[#7a2426] hover:bg-[#a53327]"
                disabled={!opp.candidature_aperte}
              >
                {opp.candidature_aperte ? 'Candidati' : 'Candidature chiuse'}
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
