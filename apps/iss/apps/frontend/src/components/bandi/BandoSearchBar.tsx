import React, { useState, useEffect } from 'react';
import { Search, Filter, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/utils/cn';
import { bandoService } from '@/services/api';
import type { BandoSource, BandoStatus, BandoSearchParams } from '@/types/api';

interface BandoSearchBarProps {
  onSearch: (params: BandoSearchParams) => void;
  loading?: boolean;
  initialParams?: BandoSearchParams;
  className?: string;
}

const fontiOptions: Array<{ value: BandoSource; label: string }> = [
  { value: 'comune_salerno', label: 'Comune di Salerno' },
  { value: 'regione_campania', label: 'Regione Campania' },
  { value: 'csv_salerno', label: 'CSV Salerno' },
  { value: 'fondazione_comunita', label: 'Fondazione Comunità' },
];

const statusOptions: Array<{ value: BandoStatus; label: string }> = [
  { value: 'attivo', label: 'Attivo' },
  { value: 'scaduto', label: 'Scaduto' },
  { value: 'archiviato', label: 'Archiviato' },
];

const sortOptions = [
  { value: 'created_at', label: 'Più recenti' },
  { value: '-created_at', label: 'Meno recenti' },
  { value: 'scadenza', label: 'Scadenza vicina' },
  { value: '-scadenza', label: 'Scadenza lontana' },
];

export const BandoSearchBar: React.FC<BandoSearchBarProps> = ({
  onSearch,
  loading = false,
  initialParams = {},
  className,
}) => {
  const [query, setQuery] = useState(initialParams.query || '');
  const [fonte, setFonte] = useState<BandoSource | undefined>(initialParams.fonte);
  const [status, setStatus] = useState<BandoStatus | undefined>(initialParams.status);
  const [sort, setSort] = useState(initialParams.sort || 'created_at');
  const [showFilters, setShowFilters] = useState(false);

  // Suggestions from API real keywords
  const [suggestions, setSuggestions] = useState<string[]>([]);

  // Load suggestions from real bando stats
  useEffect(() => {
    const loadSuggestions = async () => {
      try {
        const stats = await bandoService.getStats();
        if (stats.keywords_top) {
          const keywords = stats.keywords_top.map(item => item.keyword);
          setSuggestions(keywords);
        }
      } catch (error) {
        // Fallback keywords se API non disponibile
        setSuggestions([
          'digitale', 'innovazione', 'giovani', 'inclusione', 'formazione',
          'cultura', 'sociale', 'terzo settore', 'volontariato', 'aps'
        ]);
      }
    };

    loadSuggestions();
  }, []);

  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);

  // Filter suggestions based on query
  useEffect(() => {
    if (query.length > 0) {
      const filtered = suggestions.filter((suggestion) =>
        suggestion.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
    } else {
      setShowSuggestions(false);
    }
  }, [query, suggestions]);

  const handleSearch = () => {
    const params: BandoSearchParams = {
      ...(query.trim() && { query: query.trim() }),
      ...(fonte && { fonte }),
      ...(status && { status }),
      sort: sort as any,
      skip: 0, // Reset pagination on new search
      limit: 20,
    };

    onSearch(params);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
      setShowSuggestions(false);
    }
  };

  const clearFilters = () => {
    setQuery('');
    setFonte(undefined);
    setStatus(undefined);
    setSort('created_at');
    onSearch({ skip: 0, limit: 20 });
  };

  const hasActiveFilters = query || fonte || status || sort !== 'created_at';

  return (
    <div className={cn('w-full space-y-4', className)}>
      {/* Main Search Bar */}
      <div className="relative">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Cerca bandi per parole chiave, ente, categoria..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => query.length > 0 && setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              className="pl-10 pr-4"
            />

            {/* Suggestions Dropdown */}
            {showSuggestions && filteredSuggestions.length > 0 && (
              <div className="absolute top-full z-50 mt-1 w-full rounded-md border bg-popover shadow-md">
                {filteredSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    type="button"
                    className="w-full px-3 py-2 text-left text-sm hover:bg-accent hover:text-accent-foreground"
                    onClick={() => {
                      setQuery(suggestion);
                      setShowSuggestions(false);
                    }}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>

          <Button onClick={handleSearch} disabled={loading} variant="iss-primary">
            {loading ? (
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            ) : (
              <Search className="h-4 w-4" />
            )}
            <span className="ml-2 hidden sm:inline">Cerca</span>
          </Button>

          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className={cn(showFilters && 'bg-accent')}
          >
            <Filter className="h-4 w-4" />
            <span className="ml-2 hidden sm:inline">Filtri</span>
          </Button>
        </div>
      </div>

      {/* Advanced Filters */}
      {showFilters && (
        <div className="fade-in rounded-lg border bg-card p-4">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {/* Fonte */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Fonte</label>
              <Select value={fonte || ""} onValueChange={(value) => setFonte(value || undefined as BandoSource)}>
                <SelectTrigger>
                  <SelectValue placeholder="Tutte le fonti" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Tutte le fonti</SelectItem>
                  {fontiOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Status */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Status</label>
              <Select value={status} onValueChange={(value) => setStatus(value as BandoStatus)}>
                <SelectTrigger>
                  <SelectValue placeholder="Tutti gli status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Tutti gli status</SelectItem>
                  {statusOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Sort */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Ordinamento</label>
              <Select value={sort} onValueChange={setSort}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {sortOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Actions */}
            <div className="flex items-end space-x-2">
              <Button onClick={handleSearch} className="flex-1" variant="iss-primary">
                Applica
              </Button>
              {hasActiveFilters && (
                <Button onClick={clearFilters} variant="outline" size="icon">
                  <X className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Active Filters */}
      {hasActiveFilters && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Filtri attivi:</span>
          {query && (
            <Badge variant="info" className="gap-1">
              "{query}"
              <button
                type="button"
                onClick={() => setQuery('')}
                className="ml-1 hover:text-destructive"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
          {fonte && (
            <Badge variant="outline" className="gap-1">
              {fontiOptions.find((f) => f.value === fonte)?.label}
              <button
                type="button"
                onClick={() => setFonte(undefined)}
                className="ml-1 hover:text-destructive"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
          {status && (
            <Badge variant="outline" className="gap-1">
              {statusOptions.find((s) => s.value === status)?.label}
              <button
                type="button"
                onClick={() => setStatus(undefined)}
                className="ml-1 hover:text-destructive"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
        </div>
      )}
    </div>
  );
};
