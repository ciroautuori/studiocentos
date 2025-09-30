import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { issService } from '@/services/api'
import type { Corso } from '@/types/api'

export const Route = createFileRoute('/corsi')({
  component: CorsiPage,
})

function CorsiPage() {
  const [corsi, setCorsi] = useState<Corso[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadCorsi = async () => {
      try {
        const response = await issService.searchCorsi({ limit: 20 })
        setCorsi(response.items || [])
      } catch (err) {
        console.error('Errore caricamento corsi:', err)
      } finally {
        setLoading(false)
      }
    }

    loadCorsi()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🎓 Formazione Digitale <span className="text-[#f4af00]">GRATUITA</span>
          </h1>
          <p className="text-xl">Corsi professionali per tutti</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {corsi.map((corso) => (
            <Card key={corso.id} className="p-6 bg-white/90">
              <h3 className="text-xl font-bold mb-2">{corso.titolo}</h3>
              <p className="text-gray-600 mb-4">{corso.descrizione}</p>
              <div className="flex justify-between items-center">
                <Badge className="bg-green-100 text-green-800">GRATUITO</Badge>
                <Button className="bg-[#7a2426] hover:bg-[#a53327]">
                  Iscriviti
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
