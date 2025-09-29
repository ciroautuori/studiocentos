import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export const Route = createFileRoute('/partners')({
  component: PartnersPage,
})

function PartnersPage() {
  const [partners, setPartners] = useState([])
  const [testimonials, setTestimonials] = useState([])

  useEffect(() => {
    // Mock data partners
    setPartners([
      {
        id: 1,
        nome_organizzazione: "Università di Salerno",
        tipo: "istituzione_accademica",
        livello: "strategico",
        settore: "educazione",
        descrizione_breve: "Partnership per formazione e ricerca nel digitale",
        citta: "Salerno",
        logo_url: null,
        sito_web: "https://www.unisa.it",
        partner_strategico: true
      },
      {
        id: 2,
        nome_organizzazione: "Regione Campania",
        tipo: "ente_pubblico",
        livello: "istituzionale",
        settore: "pubblica_amministrazione",
        descrizione_breve: "Supporto istituzionale per progetti di innovazione sociale",
        citta: "Napoli",
        logo_url: null,
        sito_web: "https://www.regione.campania.it",
        partner_strategico: true
      },
      {
        id: 3,
        nome_organizzazione: "TechForGood Italia",
        tipo: "azienda_privata",
        livello: "operativo",
        settore: "tecnologia",
        descrizione_breve: "Soluzioni tecnologiche per il terzo settore",
        citta: "Milano",
        logo_url: null,
        sito_web: "https://www.techforgood.it",
        partner_strategico: false
      }
    ])

    // Mock data testimonials
    setTestimonials([
      {
        id: 1,
        nome_autore: "Prof. Mario Bianchi",
        ruolo_autore: "Direttore Dipartimento Informatica",
        organizzazione: "Università di Salerno",
        contenuto: "La collaborazione con ISS ha portato risultati straordinari nella formazione digitale dei cittadini campani.",
        rating: 5,
        verificato: true,
        data_creazione: "2025-09-10"
      },
      {
        id: 2,
        nome_autore: "Dott.ssa Anna Rossi",
        ruolo_autore: "Assessore Innovazione",
        organizzazione: "Regione Campania",
        contenuto: "ISS rappresenta un modello di eccellenza per l'innovazione sociale in Italia.",
        rating: 5,
        verificato: true,
        data_creazione: "2025-09-05"
      }
    ])
  }, [])

  const getLivelloColor = (livello) => {
    switch (livello) {
      case 'strategico': return 'bg-red-100 text-red-800'
      case 'istituzionale': return 'bg-blue-100 text-blue-800'
      case 'operativo': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTipoColor = (tipo) => {
    switch (tipo) {
      case 'istituzione_accademica': return 'bg-purple-100 text-purple-800'
      case 'ente_pubblico': return 'bg-blue-100 text-blue-800'
      case 'azienda_privata': return 'bg-orange-100 text-orange-800'
      case 'ong': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const renderStars = (rating) => {
    return '⭐'.repeat(rating)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
      <div className="bg-gradient-to-r from-[#7a2426] to-[#a53327] text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">
            🤝 Partner & <span className="text-[#f4af00]">Collaborazioni</span>
          </h1>
          <p className="text-xl">La rete che rende possibile l'innovazione sociale</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Partner Strategici */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">🌟 Partner Strategici</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {partners.filter(p => p.partner_strategico).map((partner) => (
              <Card key={partner.id} className="p-6 bg-white/90 border-l-4 border-[#f4af00]">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold">{partner.nome_organizzazione}</h3>
                  <div className="flex gap-2">
                    <Badge className={getLivelloColor(partner.livello)}>
                      {partner.livello}
                    </Badge>
                    <Badge className={getTipoColor(partner.tipo)}>
                      {partner.tipo.replace('_', ' ')}
                    </Badge>
                  </div>
                </div>
                
                <p className="text-gray-600 mb-4">{partner.descrizione_breve}</p>
                
                <div className="flex justify-between items-center">
                  <div className="text-sm text-gray-500">
                    📍 {partner.citta} • 🏢 {partner.settore}
                  </div>
                  <Button className="bg-[#7a2426] hover:bg-[#a53327]">
                    Scopri di più
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Altri Partner */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">🤝 Altri Partner</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {partners.filter(p => !p.partner_strategico).map((partner) => (
              <Card key={partner.id} className="p-4 bg-white/90">
                <div className="flex justify-between items-start mb-3">
                  <h4 className="font-bold text-lg">{partner.nome_organizzazione}</h4>
                  <Badge className={getLivelloColor(partner.livello)} size="sm">
                    {partner.livello}
                  </Badge>
                </div>
                
                <p className="text-gray-600 text-sm mb-3">{partner.descrizione_breve}</p>
                
                <div className="text-xs text-gray-500">
                  📍 {partner.citta}
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Testimonials */}
        <div>
          <h2 className="text-2xl font-bold mb-6">💬 Cosa Dicono di Noi</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.id} className="p-6 bg-white/90">
                <div className="flex items-center mb-4">
                  <div className="text-2xl mr-3">
                    {renderStars(testimonial.rating)}
                  </div>
                  {testimonial.verificato && (
                    <Badge className="bg-green-100 text-green-800">
                      ✓ Verificato
                    </Badge>
                  )}
                </div>
                
                <blockquote className="text-gray-700 italic mb-4">
                  "{testimonial.contenuto}"
                </blockquote>
                
                <div className="border-t pt-4">
                  <div className="font-semibold">{testimonial.nome_autore}</div>
                  <div className="text-sm text-gray-600">{testimonial.ruolo_autore}</div>
                  <div className="text-sm text-gray-500">{testimonial.organizzazione}</div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
