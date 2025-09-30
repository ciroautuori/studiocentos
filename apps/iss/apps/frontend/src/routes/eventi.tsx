import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { issService } from '@/services/api'
import type { Evento } from '@/types/api'

export const Route = createFileRoute('/eventi')({
  component: EventiPage,
})

function EventiPage() {
  const [eventi, setEventi] = useState<Evento[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadEventi = async () => {
      try {
        const response = await issService.searchEventi({ limit: 20 })
        setEventi(response.items || [])
      } catch (err) {
        console.error('Errore caricamento eventi:', err)
      } finally {
        setLoading(false)
      }
    }

    loadEventi()
  }, [])

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-purple-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🎪 Eventi & Workshop <span className="text-[#f4af00]">GRATUITI</span>
          </h1>
          <p className="text-xl">100% accessibili per tutti</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {eventi.map((evento) => (
            <Card key={evento.id} className="p-6 bg-white/90">
              <h3 className="text-xl font-bold mb-2">{evento.titolo}</h3>
              <p className="text-gray-600 mb-4">{evento.descrizione}</p>
              <div className="space-y-2 mb-4">
                <div className="text-sm text-gray-600">
                  📅 {formatDate(evento.data_inizio)}
                </div>
                <div className="text-sm text-gray-600">
                  📍 {evento.luogo}
                </div>
                <div className="text-sm text-gray-600">
                  👥 {evento.posti_disponibili} posti disponibili
                </div>
              </div>
              <div className="flex justify-between items-center">
                <Badge className="bg-green-100 text-green-800">GRATUITO</Badge>
                <Button className="bg-[#7a2426] hover:bg-[#a53327]">
                  Partecipa
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
