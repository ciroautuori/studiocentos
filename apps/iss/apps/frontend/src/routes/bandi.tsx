import { createFileRoute } from '@tanstack/react-router';
import { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { BandoCard } from '@/components/bandi/BandoCard';
import { BandoSearchBar } from '@/components/bandi/BandoSearchBar';
import { BandoFilters } from '@/components/bandi/BandoFilters';
import { BandoExport } from '@/components/bandi/BandoExport';
import { BandoStats } from '@/components/bandi/BandoStats';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { bandoAPI } from '@/services/api';
import { Bando, BandoFilters as BandoFiltersType } from '@/types/api';
import { Loader2, Search, Filter, Download, Map, Grid, List } from 'lucide-react';
import { cn } from '@/utils/cn';

// Validation schema per filtri
const filtersSchema = {
  search: '',
  fonte: 'all',
  categoria: 'all',
  status: 'all',
  importo_min: 0,
  importo_max: 1000000,
  data_scadenza_da: '',
  data_scadenza_a: '',
  sort_by: 'relevance',
  sort_order: 'desc',
  per_page: 20,
  page: 1,
} as const;

export const Route = createFileRoute('/bandi')({
  component: BandiPage,
  validateSearch: (search: Record<string, unknown>): BandoFiltersType => {
    return {
      search: (search.search as string) || filtersSchema.search,
      fonte: (search.fonte as string) || filtersSchema.fonte,
      categoria: (search.categoria as string) || filtersSchema.categoria,
      status: (search.status as string) || filtersSchema.status,
      importo_min: Number(search.importo_min) || filtersSchema.importo_min,
      importo_max: Number(search.importo_max) || filtersSchema.importo_max,
      data_scadenza_da: (search.data_scadenza_da as string) || filtersSchema.data_scadenza_da,
      data_scadenza_a: (search.data_scadenza_a as string) || filtersSchema.data_scadenza_a,
      sort_by: (search.sort_by as string) || filtersSchema.sort_by,
      sort_order: (search.sort_order as string) || filtersSchema.sort_order,
      per_page: Number(search.per_page) || filtersSchema.per_page,
      page: Number(search.page) || filtersSchema.page,
    };
  },
});

function BandiPage() {
  const navigate = Route.useNavigate();
  const filters = Route.useSearch();
  
  // States locali
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedBandi, setSelectedBandi] = useState<string[]>([]);
  const [savedBandi, setSavedBandi] = useState<Set<string>>(new Set());

  // Query bandi con cache intelligente
  const {
    data: bandiResponse,
    isLoading,
    error,
    isPlaceholderData
  } = useQuery({
    queryKey: ['bandi', filters],
    queryFn: () => bandoAPI.search(filters),
    placeholderData: (previousData) => previousData,
    staleTime: 5 * 60 * 1000, // 5 minuti
  });

  // Statistiche bandi
  const { data: stats } = useQuery({
    queryKey: ['bandi-stats'],
    queryFn: () => bandoAPI.getStats(),
    staleTime: 15 * 60 * 1000, // 15 minuti
  });

  // Memoized computations
  const bandi = bandiResponse?.items || [];
  const totalCount = bandiResponse?.total || 0;
  const hasNextPage = (bandiResponse?.page || 0) < (bandiResponse?.pages || 0);
  const currentPage = filters.page;

  // Handler aggiornamento filtri
  const updateFilters = (newFilters: Partial<BandoFiltersType>) => {
    navigate({
      search: {
        ...filters,
        ...newFilters,
        page: 1, // Reset page quando cambiano filtri
      },
    });
  };

  // Handler paginazione
  const handlePageChange = (page: number) => {
    navigate({
      search: {
        ...filters,
        page,
      },
    });
  };

  // Salva/rimuovi bando
  const toggleSaveBando = async (bandoId: string) => {
    try {
      if (savedBandi.has(bandoId)) {
        await bandoAPI.unsave(bandoId);
        setSavedBandi(prev => {
          const next = new Set(prev);
          next.delete(bandoId);
          return next;
        });
      } else {
        await bandoAPI.save(bandoId);
        setSavedBandi(prev => new Set(prev).add(bandoId));
      }
    } catch (error) {
      console.error('Errore salvataggio bando:', error);
    }
  };

  // Selezione multipla per export
  const toggleSelectBando = (bandoId: string) => {
    setSelectedBandi(prev => 
      prev.includes(bandoId) 
        ? prev.filter(id => id !== bandoId)
        : [...prev, bandoId]
    );
  };

  const selectAllBandi = () => {
    setSelectedBandi(bandi.map(b => b.id));
  };

  const clearSelection = () => {
    setSelectedBandi([]);
  };

  // Skip links per accessibilità
  const SkipLinks = () => (
    <div className="sr-only focus-within:not-sr-only">
      <a 
        href="#bandi-search" 
        className="absolute top-4 left-4 z-50 bg-iss-bordeaux-800 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-iss-gold-500"
      >
        Salta alla ricerca bandi
      </a>
      <a 
        href="#bandi-results" 
        className="absolute top-4 left-48 z-50 bg-iss-bordeaux-800 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-iss-gold-500"
      >
        Salta ai risultati
      </a>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <SkipLinks />
      
      {/* Header sezione */}
      <section className="bg-white border-b border-gray-200">
        <div className="container py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                🎯 Hub Bandi APS
              </h1>
              <p className="text-lg text-gray-600">
                Trova i bandi di finanziamento perfetti per la tua associazione
              </p>
            </div>
            
            {stats && (
              <BandoStats stats={stats} />
            )}
          </div>

          {/* Barra ricerca principale */}
          <div id="bandi-search">
            <BandoSearchBar 
              value={filters.search}
              onSearch={(search) => updateFilters({ search })}
              onAdvancedSearch={() => setShowFilters(!showFilters)}
              isLoading={isLoading}
            />
          </div>
        </div>
      </section>

      {/* Filtri avanzati */}
      {showFilters && (
        <section className="bg-white border-b border-gray-200" aria-label="Filtri di ricerca avanzata">
          <div className="container py-6">
            <BandoFilters
              filters={filters}
              onFiltersChange={updateFilters}
              onReset={() => updateFilters(filtersSchema)}
            />
          </div>
        </section>
      )}

      {/* Toolbar risultati */}
      <section className="bg-white border-b border-gray-200">
        <div className="container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600" role="status" aria-live="polite">
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Caricamento bandi...
                  </span>
                ) : (
                  <span>
                    {totalCount.toLocaleString('it-IT')} bandi trovati
                    {filters.search && ` per "${filters.search}"`}
                  </span>
                )}
              </div>

              {/* Selezione multipla */}
              {selectedBandi.length > 0 && (
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">
                    {selectedBandi.length} selezionati
                  </Badge>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={clearSelection}
                    aria-label="Deseleziona tutti i bandi"
                  >
                    Deseleziona tutti
                  </Button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              {/* Export */}
              <BandoExport
                selectedBandi={selectedBandi.length > 0 ? selectedBandi : bandi.map(b => b.id)}
                filters={filters}
              />

              {/* Selezione tutti */}
              {bandi.length > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={selectAllBandi}
                  disabled={selectedBandi.length === bandi.length}
                  aria-label="Seleziona tutti i bandi visibili"
                >
                  Seleziona tutti
                </Button>
              )}

              {/* Toggle view */}
              <div className="flex items-center border rounded-lg">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                  aria-label="Vista griglia"
                  aria-pressed={viewMode === 'grid'}
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                  aria-label="Vista lista"
                  aria-pressed={viewMode === 'list'}
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Risultati */}
      <main className="container py-8" id="bandi-results">
        {error ? (
          <Card className="border-red-200 bg-red-50">
            <CardContent className="p-6 text-center">
              <div className="text-red-600 mb-2">
                ❌ Errore durante il caricamento dei bandi
              </div>
              <p className="text-red-700 mb-4">
                {error.message || 'Si è verificato un errore imprevisto'}
              </p>
              <Button 
                onClick={() => window.location.reload()}
                variant="outline"
              >
                Riprova
              </Button>
            </CardContent>
          </Card>
        ) : isLoading && !isPlaceholderData ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-3 bg-gray-200 rounded"></div>
                    <div className="h-3 bg-gray-200 rounded w-5/6"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : bandi.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Search className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Nessun bando trovato
              </h3>
              <p className="text-gray-600 mb-6">
                Prova a modificare i filtri di ricerca o controlla più tardi per nuovi bandi.
              </p>
              <div className="flex gap-4 justify-center">
                <Button 
                  onClick={() => updateFilters(filtersSchema)}
                  variant="outline"
                >
                  Rimuovi filtri
                </Button>
                <Button 
                  onClick={() => setShowFilters(true)}
                >
                  Modifica ricerca
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <>
            {/* Grid/List view */}
            <div 
              className={cn(
                viewMode === 'grid' 
                  ? 'grid gap-6 md:grid-cols-2 lg:grid-cols-3' 
                  : 'space-y-6'
              )}
              role="region"
              aria-label="Risultati ricerca bandi"
              aria-live="polite"
            >
              {bandi.map((bando) => (
                <BandoCard
                  key={bando.id}
                  bando={bando}
                  isSelected={selectedBandi.includes(bando.id)}
                  isSaved={savedBandi.has(bando.id)}
                  onSelect={() => toggleSelectBando(bando.id)}
                  onSave={() => toggleSaveBando(bando.id)}
                  viewMode={viewMode}
                />
              ))}
            </div>

            {/* Paginazione */}
            {totalCount > filters.per_page && (
              <div className="mt-8 flex items-center justify-center gap-4">
                <Button
                  variant="outline"
                  disabled={currentPage === 1}
                  onClick={() => handlePageChange(currentPage - 1)}
                  aria-label="Pagina precedente"
                >
                  Precedente
                </Button>
                
                <div className="flex items-center gap-2">
                  {Array.from({ 
                    length: Math.min(5, Math.ceil(totalCount / filters.per_page)) 
                  }).map((_, i) => {
                    const page = i + 1;
                    return (
                      <Button
                        key={page}
                        variant={page === currentPage ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => handlePageChange(page)}
                        aria-label={`Pagina ${page}`}
                        aria-current={page === currentPage ? 'page' : undefined}
                      >
                        {page}
                      </Button>
                    );
                  })}
                </div>

                <Button
                  variant="outline"
                  disabled={!hasNextPage}
                  onClick={() => handlePageChange(currentPage + 1)}
                  aria-label="Pagina successiva"
                >
                  Successiva
                </Button>
              </div>
            )}
          </>
        )}
      </main>

      {/* Live region per annunci screen reader */}
      <div 
        role="status" 
        aria-live="polite" 
        aria-atomic="true" 
        className="sr-only"
        id="search-announcements"
      >
        {/* Annunci dinamici per screen reader */}
      </div>
    </div>
  );
}
