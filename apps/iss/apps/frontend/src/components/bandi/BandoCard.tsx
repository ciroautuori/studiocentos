import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Bando } from '@/types/api';
import { 
  Calendar, 
  Euro, 
  ExternalLink, 
  Building2,
  Tag,
  Clock,
  AlertTriangle,
  BookmarkPlus,
  Bookmark
} from 'lucide-react';
import { cn } from '@/utils/cn';

interface BandoCardProps {
  bando: Bando;
  onSave?: (bando: Bando) => void;
  onSelect?: (bando: Bando) => void;
  onDetails?: (bando: Bando) => void;
  className?: string;
  compact?: boolean;
  isSelected?: boolean;
  isSaved?: boolean;
  viewMode?: 'grid' | 'list';
}

export const BandoCard: React.FC<BandoCardProps> = ({ 
  bando, 
  onDetails,
  onSave,
  onSelect,
  className,
  compact = false,
  isSelected = false,
  isSaved = false,
  viewMode = 'grid'
}) => {
  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat('it-IT', {
      day: '2-digit',
      month: '2-digit',  
      year: 'numeric'
    }).format(new Date(dateString));
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('it-IT', {
      style: 'currency',
      currency: 'EUR',
      notation: amount > 100000 ? 'compact' : 'standard',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getStatusBadge = () => {
    if (bando.scaduto) {
      return (
        <Badge variant="secondary" className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          Scaduto
        </Badge>
      );
    }
    
    if (bando.giorni_rimanenti !== undefined && bando.giorni_rimanenti <= 7) {
      return (
        <Badge variant="warning" className="flex items-center gap-1">
          <AlertTriangle className="h-3 w-3" />
          In scadenza ({bando.giorni_rimanenti} giorni)
        </Badge>
      );
    }
    
    return (
      <Badge variant="success" className="flex items-center gap-1">
        <Calendar className="h-3 w-3" />
        Attivo
      </Badge>
    );
  };

  const getFonteLabel = (fonte: string) => {
    const fonteMap: Record<string, string> = {
      'comune_salerno': 'Comune di Salerno',
      'regione_campania': 'Regione Campania',
      'csv_salerno': 'CSV Salerno',
      'fondazione_comunita': 'Fondazione di Comunità',
      'altro': 'Altri Enti'
    };
    return fonteMap[fonte] || fonte.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const handleSave = (e: React.MouseEvent) => {
    e.stopPropagation();
    onSave?.(bando);
  };

  const handleSelect = () => {
    onSelect?.(bando);
  };

  const handleDetails = () => {
    onDetails?.(bando);
  };

  const handleExternalLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(bando.link, '_blank', 'noopener,noreferrer');
  };

  // List view per layout orizzontale
  if (viewMode === 'list') {
    return (
      <div
        className={cn(
          'flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md hover:border-iss-bordeaux-200',
          bando.scaduto && 'opacity-75',
          bando.giorni_rimanenti !== undefined && bando.giorni_rimanenti <= 7 && 'ring-1 ring-orange-200',
          isSelected && 'ring-2 ring-iss-bordeaux-600 bg-iss-bordeaux-50',
          className
        )}
        onClick={handleDetails}
      >
        {/* Selezione */}
        {onSelect && (
          <div className="flex-shrink-0">
            <Checkbox
              checked={isSelected}
              onCheckedChange={handleSelect}
              aria-label={`Seleziona bando ${bando.title}`}
            />
          </div>
        )}

        {/* Contenuto principale */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold line-clamp-1 mb-2">
                {bando.title}
              </h3>
              
              <div className="flex items-center gap-3 mb-2">
                {getStatusBadge()}
                <Badge variant="outline" className="flex items-center gap-1">
                  <Tag className="h-3 w-3" />
                  {getFonteLabel(bando.fonte)}
                </Badge>
              </div>

              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Building2 className="h-4 w-4 flex-shrink-0" />
                <span>{bando.ente}</span>
              </div>
            </div>

            {/* Info laterali */}
            <div className="flex items-center gap-6 text-sm">
              {bando.importo_max && (
                <div className="text-center">
                  <div className="flex items-center gap-1 text-green-600 font-medium">
                    <Euro className="h-4 w-4" />
                    <span>{formatCurrency(bando.importo_max)}</span>
                  </div>
                  <div className="text-xs text-gray-500">Importo max</div>
                </div>
              )}
              
              {bando.scadenza && (
                <div className="text-center">
                  <div className={cn(
                    "flex items-center gap-1",
                    bando.scaduto ? "text-gray-500" : 
                    (bando.giorni_rimanenti !== undefined && bando.giorni_rimanenti <= 7) ? "text-orange-600" : "text-gray-600"
                  )}>
                    <Calendar className="h-4 w-4" />
                    <time dateTime={bando.scadenza}>
                      {formatDate(bando.scadenza)}
                    </time>
                  </div>
                  <div className="text-xs text-gray-500">Scadenza</div>
                </div>
              )}
            </div>

            {/* Azioni */}
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleSave}
                className="p-2"
                aria-label={isSaved ? `Rimuovi dai salvati il bando ${bando.title}` : `Salva il bando ${bando.title}`}
              >
                {isSaved ? (
                  <Bookmark className="h-4 w-4 text-iss-gold-600" />
                ) : (
                  <BookmarkPlus className="h-4 w-4" />
                )}
              </Button>

              <Button
                variant="outline"
                size="sm"
                onClick={handleExternalLink}
                className="flex items-center gap-1"
                aria-label={`Vai al sito del bando ${bando.title} (si apre in una nuova finestra)`}
              >
                <ExternalLink className="h-3 w-3" />
                Vai al bando
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Grid view (default)
  return (
    <Card
      className={cn(
        'cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-iss-bordeaux-200',
        bando.scaduto && 'opacity-75',
        bando.giorni_rimanenti !== undefined && bando.giorni_rimanenti <= 7 && 'ring-1 ring-orange-200',
        isSelected && 'ring-2 ring-iss-bordeaux-600 bg-iss-bordeaux-50',
        className
      )}
      onClick={handleDetails}
      role="article"
      aria-labelledby={`bando-title-${bando.id}`}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleDetails();
        }
      }}
    >
      <CardHeader className={cn('pb-3', compact && 'pb-2')}>
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            {onSelect && (
              <div className="flex items-center gap-2 mb-2">
                <Checkbox
                  checked={isSelected}
                  onCheckedChange={handleSelect}
                  aria-label={`Seleziona bando ${bando.title}`}
                />
              </div>
            )}
            
            <CardTitle 
              id={`bando-title-${bando.id}`}
              className="text-base font-semibold line-clamp-2 mb-2"
            >
              {bando.title}
            </CardTitle>
            
            <div className="flex items-center gap-2 mb-2 flex-wrap">
              {getStatusBadge()}
              <Badge variant="outline" className="flex items-center gap-1">
                <Tag className="h-3 w-3" />
                {getFonteLabel(bando.fonte)}
              </Badge>
            </div>
          </div>
          
          <div className="flex items-start gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleSave}
              className="p-1"
              aria-label={isSaved ? `Rimuovi dai salvati il bando ${bando.title}` : `Salva il bando ${bando.title}`}
            >
              {isSaved ? (
                <Bookmark className="h-4 w-4 text-iss-gold-600" />
              ) : (
                <BookmarkPlus className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        <div className="space-y-3">
          {/* Ente erogatore */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Building2 className="h-4 w-4 flex-shrink-0" />
            <span className="truncate">{bando.ente}</span>
          </div>

          {/* Descrizione */}
          {!compact && bando.descrizione && (
            <p className="text-sm text-muted-foreground line-clamp-3">
              {bando.descrizione}
            </p>
          )}

          {/* Info importanti */}
          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-4 text-sm">
              {bando.importo_max && (
                <div className="flex items-center gap-1 text-green-600 font-medium">
                  <Euro className="h-4 w-4" />
                  <span>{formatCurrency(bando.importo_max)}</span>
                </div>
              )}
              
              {bando.scadenza && (
                <div className={cn(
                  "flex items-center gap-1",
                  bando.scaduto ? "text-gray-500" : 
                  (bando.giorni_rimanenti !== undefined && bando.giorni_rimanenti <= 7) ? "text-orange-600" : "text-gray-600"
                )}>
                  <Calendar className="h-4 w-4" />
                  <time dateTime={bando.scadenza}>
                    {formatDate(bando.scadenza)}
                  </time>
                </div>
              )}
              
              {bando.giorni_rimanenti !== undefined && !bando.scaduto && (
                <div className="text-xs text-gray-500">
                  {bando.giorni_rimanenti} giorni rimanenti
                </div>
              )}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleExternalLink}
              className="flex items-center gap-1"
              aria-label={`Vai al sito del bando ${bando.title} (si apre in una nuova finestra)`}
            >
              <ExternalLink className="h-3 w-3" />
              Vai al bando
            </Button>
          </div>

          {/* Keywords */}
          {bando.keywords && bando.keywords.length > 0 && (
            <div className="flex flex-wrap gap-1 pt-2">
              {bando.keywords.slice(0, 3).map((keyword) => (
                <Badge 
                  key={keyword} 
                  variant="outline" 
                  className="text-xs px-2 py-1"
                >
                  {keyword}
                </Badge>
              ))}
              {bando.keywords.length > 3 && (
                <Badge variant="outline" className="text-xs px-2 py-1">
                  +{bando.keywords.length - 3} altri
                </Badge>
              )}
            </div>
          )}

          {/* Match keyword evidenziato */}
          {bando.keyword_match && (
            <div className="pt-2">
              <Badge variant="default" className="bg-iss-gold-500 text-white text-xs">
                Match: {bando.keyword_match}
              </Badge>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
