import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useEffect } from 'react'

export const Route = createFileRoute('/dashboard/')({
  component: DashboardOverview,
})

function DashboardOverview() {
  const navigate = useNavigate()

  useEffect(() => {
    // Reindirizza automaticamente alla dashboard admin per il testing
    navigate({ to: '/dashboard/admin' })
  }, [navigate])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Reindirizzamento...</h2>
        <p className="text-muted-foreground">Caricamento dashboard professionale</p>
      </div>
    </div>
  )
}
