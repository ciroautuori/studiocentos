import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BandoFilters as BandoFiltersType } from '@/types/api';
import { 
  Filter, 
  X, 
  Calendar,
  Euro,
  Building2,
  Tag,
  RotateCcw,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { cn } from '@/utils/cn';

interface BandoFiltersProps {
  filters: BandoFiltersType;
  onFiltersChange: (filters: Partial<BandoFiltersType>) => void;
  onReset: () => void;
}

// Configurazioni per i filtri
const FONTI_OPTIONS = [
  { value: 'all', label: 'Tutte le fonti' },
  { value: 'comune_salerno', label: 'Comune di Salerno' },
  { value: 'regione_campania', label: 'Regione Campania' },
  { value: 'csv_salerno', label: 'CSV Salerno' },
  { value: 'fondazione_comunita', label: 'Fondazione di Comunità' },
  { value: 'ministero_terzo_settore', label: 'Ministero Terzo Settore' },
  { value: 'unione_europea', label: 'Unione Europea' },
] as const;

const CATEGORIE_OPTIONS = [
  { value: 'all', label: 'Tutte le categorie' },
  { value: 'sociale', label: 'Servizi Sociali' },
  { value: 'cultura', label: 'Arte e Cultura' },
  { value: 'ambiente', label: 'Ambiente e Territorio' },
  { value: 'sport', label: 'Sport e Tempo Libero' },
  { value: 'formazione', label: 'Formazione ed Educazione' },
  { value: 'sanita', label: 'Salute e Sanità' },
  { value: 'innovazione', label: 'Innovazione Sociale' },
  { value: 'digitale', label: 'Trasformazione Digitale' },
  { value: 'cooperazione', label: 'Cooperazione Internazionale' },
] as const;

const STATUS_OPTIONS = [
  { value: 'all', label: 'Tutti gli stati' },
  { value: 'attivo', label: 'Attivi' },
  { value: 'scaduto', label: 'Scaduti' },
  { value: 'in_scadenza', label: 'In scadenza (7 giorni)' },
] as const;

const SORT_OPTIONS = [
  { value: 'relevance', label: 'Rilevanza' },
  { value: 'data_scadenza', label: 'Data scadenza' },
  { value: 'data_pubblicazione', label: 'Data pubblicazione' },
  { value: 'importo_max', label: 'Importo massimo' },
  { value: 'priority_score', label: 'Priorità' },
] as const;

const IMPORTO_RANGES = [
  { min: 0, max: 5000, label: 'Fino a €5.000' },
  { min: 5000, max: 15000, label: '€5.000 - €15.000' },
  { min: 15000, max: 50000, label: '€15.000 - €50.000' },
  { min: 50000, max: 100000, label: '€50.000 - €100.000' },
  { min: 100000, max: 1000000, label: 'Oltre €100.000' },
] as const;

export const BandoFilters: React.FC<BandoFiltersProps> = ({
  filters,
  onFiltersChange,
  onReset
}) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['basic']));
  const [activeFiltersCount, setActiveFiltersCount] = useState(0);

  // Calcola filtri attivi (escludendo valori di default)
  const calculateActiveFilters = () => {
    let count = 0;
    if (filters.fonte && filters.fonte !== 'all') count++;
    if (filters.categoria && filters.categoria !== 'all') count++;
    if (filters.status && filters.status !== 'all') count++;
    if (filters.importo_min > 0) count++;
    if (filters.importo_max < 1000000) count++;
    if (filters.data_scadenza_da) count++;
    if (filters.data_scadenza_a) count++;
    if (filters.sort_by !== 'relevance') count++;
    return count;
  };

  const toggleSection = (section: string) => {
    setExpandedSections(prev => {
      const next = new Set(prev);
      if (next.has(section)) {
        next.delete(section);
      } else {
        next.add(section);
      }
      return next;
    });
  };

  const isExpanded = (section: string) => expandedSections.has(section);

  const handleImportoRangeSelect = (min: number, max: number) => {
    onFiltersChange({ 
      importo_min: min, 
      importo_max: max 
    });
  };

  const FilterSection = ({ 
    id, 
    title, 
    icon: Icon, 
    children, 
    defaultExpanded = false 
  }: {
    id: string;
    title: string;
    icon: any;
    children: React.ReactNode;
    defaultExpanded?: boolean;
  }) => (
    <Card>
      <CardHeader 
        className="pb-3 cursor-pointer select-none"
        onClick={() => toggleSection(id)}
      >
        <CardTitle className="flex items-center justify-between text-base">
          <div className="flex items-center gap-2">
            <Icon className="h-4 w-4 text-iss-bordeaux-600" />
            <span>{title}</span>
          </div>
          {isExpanded(id) ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </CardTitle>
      </CardHeader>
      {isExpanded(id) && (
        <CardContent className="pt-0">
          {children}
        </CardContent>
      )}
    </Card>
  );

  return (
    <div className="space-y-4">
      {/* Header filtri */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filtri Avanzati
          </h2>
          {calculateActiveFilters() > 0 && (
            <Badge variant="secondary">
              {calculateActiveFilters()} filtri attivi
            </Badge>
          )}
        </div>
        
        <Button
          variant="outline"
          size="sm"
          onClick={onReset}
          className="flex items-center gap-2"
          aria-label="Ripristina tutti i filtri ai valori predefiniti"
        >
          <RotateCcw className="h-4 w-4" />
          Ripristina
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Filtri di base */}
        <FilterSection id="basic" title="Filtri di Base" icon={Filter} defaultExpanded>
          <div className="space-y-4">
            {/* Fonte */}
            <div>
              <label htmlFor="fonte-select" className="block text-sm font-medium mb-2">
                Fonte del bando
              </label>
              <Select
                id="fonte-select"
                value={filters.fonte}
                onValueChange={(value) => onFiltersChange({ fonte: value })}
                aria-describedby="fonte-help"
              >
                {FONTI_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
              <p id="fonte-help" className="text-xs text-gray-500 mt-1">
                Filtra per ente erogatore del finanziamento
              </p>
            </div>

            {/* Categoria */}
            <div>
              <label htmlFor="categoria-select" className="block text-sm font-medium mb-2">
                Categoria
              </label>
              <Select
                id="categoria-select"
                value={filters.categoria}
                onValueChange={(value) => onFiltersChange({ categoria: value })}
                aria-describedby="categoria-help"
              >
                {CATEGORIE_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
              <p id="categoria-help" className="text-xs text-gray-500 mt-1">
                Seleziona il settore di interesse
              </p>
            </div>

            {/* Status */}
            <div>
              <label htmlFor="status-select" className="block text-sm font-medium mb-2">
                Stato del bando
              </label>
              <Select
                id="status-select"
                value={filters.status}
                onValueChange={(value) => onFiltersChange({ status: value })}
                aria-describedby="status-help"
              >
                {STATUS_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
              <p id="status-help" className="text-xs text-gray-500 mt-1">
                Filtra per stato di attivazione
              </p>
            </div>
          </div>
        </FilterSection>

        {/* Filtri importo */}
        <FilterSection id="importo" title="Fascia di Importo" icon={Euro}>
          <div className="space-y-4">
            {/* Range predefiniti */}
            <div>
              <p className="text-sm font-medium mb-3">Fasce predefinite</p>
              <div className="grid gap-2">
                {IMPORTO_RANGES.map((range) => (
                  <Button
                    key={`${range.min}-${range.max}`}
                    variant="outline"
                    size="sm"
                    onClick={() => handleImportoRangeSelect(range.min, range.max)}
                    className={cn(
                      'justify-start text-left h-auto py-2',
                      filters.importo_min === range.min && 
                      filters.importo_max === range.max && 
                      'border-iss-bordeaux-600 bg-iss-bordeaux-50'
                    )}
                  >
                    {range.label}
                  </Button>
                ))}
              </div>
            </div>

            {/* Range personalizzato */}
            <div>
              <p className="text-sm font-medium mb-3">Importo personalizzato</p>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label htmlFor="importo-min" className="block text-xs text-gray-500 mb-1">
                    Da €
                  </label>
                  <Input
                    id="importo-min"
                    type="number"
                    min="0"
                    value={filters.importo_min || ''}
                    onChange={(e) => onFiltersChange({ 
                      importo_min: parseInt(e.target.value) || 0 
                    })}
                    placeholder="0"
                    className="text-sm"
                  />
                </div>
                <div>
                  <label htmlFor="importo-max" className="block text-xs text-gray-500 mb-1">
                    A €
                  </label>
                  <Input
                    id="importo-max"
                    type="number"
                    min="0"
                    value={filters.importo_max === 1000000 ? '' : filters.importo_max}
                    onChange={(e) => onFiltersChange({ 
                      importo_max: parseInt(e.target.value) || 1000000 
                    })}
                    placeholder="Illimitato"
                    className="text-sm"
                  />
                </div>
              </div>
            </div>
          </div>
        </FilterSection>

        {/* Filtri temporali */}
        <FilterSection id="date" title="Data Scadenza" icon={Calendar}>
          <div className="space-y-4">
            <div>
              <label htmlFor="data-da" className="block text-sm font-medium mb-2">
                Scadenza da
              </label>
              <Input
                id="data-da"
                type="date"
                value={filters.data_scadenza_da}
                onChange={(e) => onFiltersChange({ data_scadenza_da: e.target.value })}
                className="text-sm"
                aria-describedby="data-da-help"
              />
              <p id="data-da-help" className="text-xs text-gray-500 mt-1">
                Data minima di scadenza
              </p>
            </div>

            <div>
              <label htmlFor="data-a" className="block text-sm font-medium mb-2">
                Scadenza a
              </label>
              <Input
                id="data-a"
                type="date"
                value={filters.data_scadenza_a}
                onChange={(e) => onFiltersChange({ data_scadenza_a: e.target.value })}
                className="text-sm"
                aria-describedby="data-a-help"
              />
              <p id="data-a-help" className="text-xs text-gray-500 mt-1">
                Data massima di scadenza
              </p>
            </div>

            {/* Shortcut temporali */}
            <div>
              <p className="text-sm font-medium mb-2">Filtri rapidi</p>
              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const oggi = new Date().toISOString().split('T')[0];
                    const settimana = new Date();
                    settimana.setDate(settimana.getDate() + 7);
                    onFiltersChange({
                      data_scadenza_da: oggi,
                      data_scadenza_a: settimana.toISOString().split('T')[0]
                    });
                  }}
                  className="text-xs"
                >
                  Prossimi 7 giorni
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const oggi = new Date().toISOString().split('T')[0];
                    const mese = new Date();
                    mese.setMonth(mese.getMonth() + 1);
                    onFiltersChange({
                      data_scadenza_da: oggi,
                      data_scadenza_a: mese.toISOString().split('T')[0]
                    });
                  }}
                  className="text-xs"
                >
                  Prossimo mese
                </Button>
              </div>
            </div>
          </div>
        </FilterSection>
      </div>

      {/* Ordinamento */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <label htmlFor="sort-select" className="block text-sm font-medium mb-2">
                Ordina per
              </label>
              <div className="flex gap-2">
                <Select
                  id="sort-select"
                  value={filters.sort_by}
                  onValueChange={(value) => onFiltersChange({ sort_by: value })}
                  className="flex-1"
                >
                  {SORT_OPTIONS.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Select>
                <Select
                  value={filters.sort_order}
                  onValueChange={(value) => onFiltersChange({ sort_order: value })}
                  aria-label="Direzione ordinamento"
                >
                  <option value="desc">Decrescente</option>
                  <option value="asc">Crescente</option>
                </Select>
              </div>
            </div>

            <div>
              <label htmlFor="per-page-select" className="block text-sm font-medium mb-2">
                Risultati per pagina
              </label>
              <Select
                id="per-page-select"
                value={filters.per_page.toString()}
                onValueChange={(value) => onFiltersChange({ per_page: parseInt(value) })}
              >
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Riepilogo filtri attivi */}
      {calculateActiveFilters() > 0 && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-medium text-sm">Filtri attivi</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={onReset}
                className="text-xs"
              >
                Rimuovi tutti
              </Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {filters.fonte !== 'all' && (
                <Badge variant="secondary" className="flex items-center gap-1">
                  <Building2 className="h-3 w-3" />
                  {FONTI_OPTIONS.find(o => o.value === filters.fonte)?.label}
                  <button
                    onClick={() => onFiltersChange({ fonte: 'all' })}
                    className="ml-1 hover:bg-gray-200 rounded"
                    aria-label="Rimuovi filtro fonte"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
              {filters.categoria !== 'all' && (
                <Badge variant="secondary" className="flex items-center gap-1">
                  <Tag className="h-3 w-3" />
                  {CATEGORIE_OPTIONS.find(o => o.value === filters.categoria)?.label}
                  <button
                    onClick={() => onFiltersChange({ categoria: 'all' })}
                    className="ml-1 hover:bg-gray-200 rounded"
                    aria-label="Rimuovi filtro categoria"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              )}
              {/* Altri badge per filtri attivi... */}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
