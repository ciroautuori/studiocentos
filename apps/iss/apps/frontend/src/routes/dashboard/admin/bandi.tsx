import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard/admin/bandi')({
  component: BandiPage,
})

function BandiPage() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">📋 Gestione Bandi</h1>
      <p className="text-gray-600 mb-6">Pannello di gestione bandi e finanziamenti</p>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-semibold text-blue-800">Bandi Totali</h3>
          <p className="text-2xl font-bold text-blue-600">45</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="font-semibold text-green-800">Bandi Attivi</h3>
          <p className="text-2xl font-bold text-green-600">23</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="font-semibold text-yellow-800">In Scadenza</h3>
          <p className="text-2xl font-bold text-yellow-600">8</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="font-semibold text-purple-800">Importo Totale</h3>
          <p className="text-2xl font-bold text-purple-600">€2.1M</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg border">
        <h2 className="text-xl font-semibold mb-4">Bandi Recenti</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Bando Inclusione Digitale 2025</p>
              <p className="text-sm text-gray-600">Regione Campania • €50,000</p>
            </div>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Attivo</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Sostegno APS Locali</p>
              <p className="text-sm text-gray-600">Comune di Salerno • €25,000</p>
            </div>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Attivo</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Hackathon Sociale 2025</p>
              <p className="text-sm text-gray-600">CSV Salerno • €10,000</p>
            </div>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">Scadenza vicina</span>
          </div>
        </div>
      </div>
    </div>
  )
}
