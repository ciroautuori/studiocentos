import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export const Route = createFileRoute('/news')({
  component: NewsPage,
})

function NewsPage() {
  const [articoli, setArticoli] = useState([])

  useEffect(() => {
    // Mock data
    setArticoli([
      {
        id: 1,
        titolo: "Nuovi Corsi di Alfabetizzazione Digitale",
        contenuto_breve: "Partono a ottobre i nuovi corsi gratuiti per cittadini over 65",
        categoria: "formazione",
        data_pubblicazione: "2025-09-20T10:00:00",
        autore: "Redazione ISS",
        likes: 45,
        commenti: 12,
        in_evidenza: true
      },
      {
        id: 2,
        titolo: "Partnership con Università di Salerno",
        contenuto_breve: "Siglato accordo per stage e tirocini nel settore digitale",
        categoria: "partnership",
        data_pubblicazione: "2025-09-18T15:30:00",
        autore: "Maria Rossi",
        likes: 32,
        commenti: 8,
        in_evidenza: false
      },
      {
        id: 3,
        titolo: "Hackathon Sociale: I Vincitori",
        contenuto_breve: "Premiate le migliori soluzioni tech per il terzo settore campano",
        categoria: "eventi",
        data_pubblicazione: "2025-09-15T09:15:00",
        autore: "Giuseppe Verdi",
        likes: 67,
        commenti: 23,
        in_evidenza: true
      }
    ])
  }, [])

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  const getCategoriaColor = (categoria) => {
    switch (categoria) {
      case 'formazione': return 'bg-blue-100 text-blue-800'
      case 'partnership': return 'bg-purple-100 text-purple-800'
      case 'eventi': return 'bg-green-100 text-green-800'
      case 'progetti': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-cyan-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            📰 News & <span className="text-[#f4af00]">Blog</span>
          </h1>
          <p className="text-xl">Tutte le novità dal mondo ISS</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Articoli in evidenza */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6">📌 In Evidenza</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {articoli.filter(art => art.in_evidenza).map((articolo) => (
              <Card key={articolo.id} className="p-6 bg-white/90 border-l-4 border-[#f4af00]">
                <div className="flex justify-between items-start mb-4">
                  <Badge className={getCategoriaColor(articolo.categoria)}>
                    {articolo.categoria}
                  </Badge>
                  <span className="text-sm text-gray-500">
                    {formatDate(articolo.data_pubblicazione)}
                  </span>
                </div>
                
                <h3 className="text-xl font-bold mb-3">{articolo.titolo}</h3>
                <p className="text-gray-600 mb-4">{articolo.contenuto_breve}</p>
                
                <div className="flex justify-between items-center">
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>❤️ {articolo.likes}</span>
                    <span>💬 {articolo.commenti}</span>
                    <span>✍️ {articolo.autore}</span>
                  </div>
                  <Button className="bg-[#7a2426] hover:bg-[#a53327]">
                    Leggi tutto
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Altri articoli */}
        <div>
          <h2 className="text-2xl font-bold mb-6">📚 Altri Articoli</h2>
          <div className="space-y-4">
            {articoli.filter(art => !art.in_evidenza).map((articolo) => (
              <Card key={articolo.id} className="p-6 bg-white/90">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-4 mb-2">
                      <Badge className={getCategoriaColor(articolo.categoria)}>
                        {articolo.categoria}
                      </Badge>
                      <span className="text-sm text-gray-500">
                        {formatDate(articolo.data_pubblicazione)}
                      </span>
                    </div>
                    
                    <h3 className="text-lg font-bold mb-2">{articolo.titolo}</h3>
                    <p className="text-gray-600 mb-3">{articolo.contenuto_breve}</p>
                    
                    <div className="flex gap-4 text-sm text-gray-500">
                      <span>❤️ {articolo.likes}</span>
                      <span>💬 {articolo.commenti}</span>
                      <span>✍️ {articolo.autore}</span>
                    </div>
                  </div>
                  
                  <Button className="ml-4 bg-[#7a2426] hover:bg-[#a53327]">
                    Leggi
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
