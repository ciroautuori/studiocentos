import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard/admin/users')({
  component: UsersPage,
})

function UsersPage() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">👥 Gestione Utenti</h1>
      <p className="text-gray-600 mb-6">Pannello di gestione utenti della piattaforma ISS</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-semibold text-blue-800">Utenti Totali</h3>
          <p className="text-2xl font-bold text-blue-600">1,247</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="font-semibold text-green-800">Utenti Attivi</h3>
          <p className="text-2xl font-bold text-green-600">892</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="font-semibold text-yellow-800">In Attesa</h3>
          <p className="text-2xl font-bold text-yellow-600">23</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg border">
        <h2 className="text-xl font-semibold mb-4">Lista Utenti</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Mario Rossi</p>
              <p className="text-sm text-gray-600">mario.rossi@email.it</p>
            </div>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Attivo</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Anna Verdi</p>
              <p className="text-sm text-gray-600">anna.verdi@email.it</p>  
            </div>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Attivo</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <div>
              <p className="font-medium">Giuseppe Bianchi</p>
              <p className="text-sm text-gray-600">giuseppe.bianchi@email.it</p>
            </div>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">Pending</span>
          </div>
        </div>
      </div>
    </div>
  )
}
