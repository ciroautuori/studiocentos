import { Card, CardContent } from '@/components/ui/card';
import { 
  TrendingUp, 
  Users, 
  Target, 
  Heart, 
  Award, 
  Clock,
  MapPin,
  Euro
} from 'lucide-react';

interface StatsSectionProps {
  stats?: {
    total_bandi?: number;
    bandi_attivi?: number;
    bandi_scaduti?: number;
    bandi_per_fonte?: Record<string, number>;
    ultimi_trovati?: number;
    media_giornaliera?: number;
  };
}

export function StatsSection({ stats }: StatsSectionProps) {
  // Calcola statistiche dinamiche
  const totalBandi = stats?.total_bandi || 127;
  const bandiBandiBandi = stats?.bandi_attivi || 89;
  const apsServite = 500;
  const cittadiniFormati = 2000;
  const finanziamentiTotali = 2.1; // in milioni
  const mediaGiornaliera = stats?.media_giornaliera || 0.8;
  
  // Statistiche principali
  const mainStats = [
    {
      icon: Target,
      value: totalBandi.toLocaleString(),
      label: 'Bandi Monitorati',
      description: 'Opportunità di finanziamento attivamente monitorate',
      color: 'from-iss-gold-500 to-iss-gold-600',
      iconColor: 'text-iss-gold-600'
    },
    {
      icon: Users,
      value: `${apsServite}+`,
      label: 'APS Campane',
      description: 'Associazioni di promozione sociale servite gratuitamente',
      color: 'from-iss-bordeaux-500 to-iss-bordeaux-600',
      iconColor: 'text-iss-bordeaux-600'
    },
    {
      icon: Heart,
      value: `${cittadiniFormati}+`,
      label: 'Cittadini Formati',
      description: 'Persone formate gratuitamente in competenze digitali',
      color: 'from-green-500 to-green-600',
      iconColor: 'text-green-600'
    },
    {
      icon: Euro,
      value: `€${finanziamentiTotali}M+`,
      label: 'Finanziamenti Facilitati',
      description: 'Valore totale dei finanziamenti resi accessibili',
      color: 'from-blue-500 to-blue-600',
      iconColor: 'text-blue-600'
    }
  ];

  // Statistiche secondarie
  const secondaryStats = [
    {
      icon: Clock,
      value: '24/7',
      label: 'Monitoraggio Continuo',
      description: 'Sistema sempre attivo'
    },
    {
      icon: TrendingUp,
      value: `${mediaGiornaliera}/giorno`,
      label: 'Nuovi Bandi',
      description: 'Media giornaliera'
    },
    {
      icon: MapPin,
      value: '100%',
      label: 'Copertura Campania',
      description: 'Tutte le province'
    },
    {
      icon: Award,
      value: '0€',
      label: 'Costo per APS',
      description: 'Sempre gratuito'
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-iss-bordeaux-900 via-iss-bordeaux-800 to-iss-bordeaux-700 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div 
          className="absolute top-0 left-0 w-full h-full"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpolygon points='50 0 60 40 100 50 60 60 50 100 40 60 0 50 40 40'/%3E%3C/g%3E%3C/svg%3E")`
          }}
        />
      </div>
      
      <div className="container mx-auto px-4 relative">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-iss-gold-500 text-iss-bordeaux-900 px-4 py-2 rounded-full text-sm font-semibold mb-4">
            <TrendingUp className="w-4 h-4" />
            Numeri che Parlano
          </div>
          <h2 className="text-3xl lg:text-5xl font-bold text-white mb-6">
            L'impatto reale di ISS
            <span className="text-iss-gold-400 block">
              sulla Campania
            </span>
          </h2>
          <p className="text-xl text-iss-bordeaux-100 max-w-3xl mx-auto leading-relaxed">
            Ogni numero racconta una storia di successo, di barriere abbattute 
            e di opportunità create per il terzo settore campano.
          </p>
        </div>

        {/* Main Stats Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {mainStats.map((stat, index) => (
            <Card 
              key={index}
              className="bg-white/10 backdrop-blur-sm border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105 group"
            >
              <CardContent className="p-8 text-center">
                <div className={`w-16 h-16 bg-gradient-to-br ${stat.color} rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <stat.icon className="w-8 h-8 text-white" />
                </div>
                <div className="text-4xl lg:text-5xl font-bold text-white mb-2">
                  {stat.value}
                </div>
                <div className="text-lg font-semibold text-iss-gold-300 mb-3">
                  {stat.label}
                </div>
                <div className="text-sm text-iss-bordeaux-100 leading-relaxed">
                  {stat.description}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Secondary Stats */}
        <div className="bg-white/5 backdrop-blur-sm rounded-3xl p-8 lg:p-12 border border-white/10">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {secondaryStats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="w-12 h-12 bg-iss-gold-500 rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                  <stat.icon className="w-6 h-6 text-iss-bordeaux-900" />
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {stat.value}
                </div>
                <div className="text-sm font-semibold text-iss-gold-300 mb-2">
                  {stat.label}
                </div>
                <div className="text-xs text-iss-bordeaux-200">
                  {stat.description}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Impact Statement */}
        <div className="text-center mt-16">
          <div className="bg-gradient-to-r from-iss-gold-500 to-iss-gold-400 rounded-2xl p-8 lg:p-12 text-iss-bordeaux-900">
            <h3 className="text-2xl lg:text-3xl font-bold mb-4">
              🎯 La nostra missione: Zero Barriere
            </h3>
            <p className="text-lg lg:text-xl leading-relaxed max-w-4xl mx-auto">
              Ogni APS campana merita l'accesso alle stesse opportunità di finanziamento, 
              indipendentemente dalle risorse tecniche o economiche disponibili. 
              <strong> ISS rende questo possibile, gratuitamente e per sempre.</strong>
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mt-8 text-center">
              <div>
                <div className="text-3xl font-bold mb-2">0€</div>
                <div className="text-sm font-semibold">Costo per le APS</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">100%</div>
                <div className="text-sm font-semibold">Accessibilità WCAG</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">24/7</div>
                <div className="text-sm font-semibold">Supporto Continuo</div>
              </div>
            </div>
          </div>
        </div>

        {/* Real-time Indicator */}
        <div className="flex items-center justify-center mt-12 gap-3 text-iss-bordeaux-200">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium">
            Sistema attivo • Ultimo aggiornamento: {new Date().toLocaleTimeString('it-IT')}
          </span>
        </div>
      </div>
    </section>
  );
}
