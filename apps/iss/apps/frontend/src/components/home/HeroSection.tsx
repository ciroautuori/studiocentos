import React from 'react';
import { Link } from '@tanstack/react-router';
import { Search, Users, Target, TrendingUp, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/utils/cn';
import { useDashboard } from '@/contexts/DashboardContext';

interface HeroSectionProps {
  className?: string;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ className }) => {
  const { bandoStats, issStats } = useDashboard();

  const quickStats = [
    {
      icon: Target,
      value: bandoStats?.total_bandi || 0,
      label: 'Bandi Disponibili',
      trend: '+12%',
      color: 'text-iss-bordeaux-600',
    },
    {
      icon: Users,
      value: issStats?.studenti_formati || 0,
      label: 'Cittadini Formati',
      trend: '+25%',
      color: 'text-iss-green-600',
    },
    {
      icon: TrendingUp,
      value: issStats?.progetti_attivi || 0,
      label: 'Progetti Attivi',
      trend: '+8%',
      color: 'text-iss-orange-600',
    },
  ];

  return (
    <section className={cn('relative py-12 lg:py-20 overflow-hidden', className)}>
      {/* Background Pattern */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-iss-bordeaux-50/30 via-background to-iss-gold-50/20" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-iss-bordeaux-100 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob" />
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-iss-gold-100 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-1/3 w-96 h-96 bg-iss-bordeaux-200 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000" />
      </div>

      <div className="container mx-auto px-4">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 mb-6">
            <Badge variant="info" className="gap-1">
              <Sparkles className="h-3 w-3" />
              Sistema Rivoluzionario
            </Badge>
            <Badge variant="outline">
              Hub Regionale Campania
            </Badge>
          </div>

          {/* Main Heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
            <span className="text-gradient">
              Innovazione Sociale
            </span>
            <br />
            <span className="text-foreground">
              Salernitana
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed">
            Il <strong>primo sistema automatizzato</strong> per la ricerca di bandi di finanziamento 
            per APS campane + <strong>formazione digitale inclusiva</strong> per cittadini salernitani
          </p>

          {/* Dual CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link to="/bandi">
              <Button
                size="xl"
                variant="gradient"
                className="gap-2 text-lg px-8 py-4 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              >
                <Search className="h-5 w-5" />
                Cerca Bandi per la tua APS
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>

            <Link to="/corsi">
              <Button
                size="xl"
                variant="outline"
                className="gap-2 text-lg px-8 py-4 hover:bg-accent/50 transform hover:scale-105 transition-all duration-300"
              >
                <Users className="h-5 w-5" />
                Scopri i Nostri Corsi
              </Button>
            </Link>
          </div>

          {/* Quick Stats */}
          <div className="grid gap-6 sm:grid-cols-3 max-w-2xl mx-auto mb-12">
            {quickStats.map((stat, index) => (
              <Card key={index} className="iss-card hover:shadow-md transition-shadow">
                <CardContent className="p-4 text-center">
                  <div className={cn('inline-flex p-2 rounded-full mb-2', stat.color.replace('text-', 'bg-') + '/10')}>
                    <stat.icon className={cn('h-5 w-5', stat.color)} />
                  </div>
                  <div className="text-2xl font-bold text-foreground">
                    {stat.value.toLocaleString('it-IT')}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {stat.label}
                  </div>
                  <div className={cn('text-xs font-medium mt-1', stat.color)}>
                    {stat.trend} questo mese
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Value Propositions */}
          <div className="grid gap-8 md:grid-cols-2 max-w-4xl mx-auto text-left">
            {/* Hub Bandi */}
            <Card className="iss-card hover:shadow-lg transition-all duration-300 priority-medium">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-full bg-iss-bordeaux-100 text-iss-bordeaux-600">
                    <Target className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">
                      Hub Bandi per APS Campane
                    </h3>
                    <p className="text-muted-foreground mb-4">
                      Sistema automatizzato che monitora 24/7 fonti ufficiali e trova 
                      bandi pertinenti per la tua organizzazione. Democratizza l'accesso 
                      ai finanziamenti per centinaia di APS.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" className="text-xs">
                        Comune Salerno
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        Regione Campania
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        CSV + Fondazioni
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Attività ISS */}
            <Card className="iss-card hover:shadow-lg transition-all duration-300 priority-medium">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-full bg-iss-green-100 text-iss-green-600">
                    <Users className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">
                      Formazione Digitale Inclusiva
                    </h3>
                    <p className="text-muted-foreground mb-4">
                      Corsi di alfabetizzazione digitale, supporto professionale per persone 
                      con disabilità, hackathon sociali e progetti di innovazione per il territorio.
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline" className="text-xs">
                        Alfabetizzazione
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        Tecnologie Assistive
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        Hackathon Sociali
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Trust Indicators */}
          <div className="mt-12 pt-8 border-t">
            <p className="text-sm text-muted-foreground mb-4">
              Partner e collaborazioni istituzionali
            </p>
            <div className="flex flex-wrap justify-center items-center gap-6 opacity-60">
              <Badge variant="outline" className="px-4 py-2">
                Comune di Salerno
              </Badge>
              <Badge variant="outline" className="px-4 py-2">
                Regione Campania
              </Badge>
              <Badge variant="outline" className="px-4 py-2">
                CSV Salerno
              </Badge>
              <Badge variant="outline" className="px-4 py-2">
                Università di Salerno
              </Badge>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
