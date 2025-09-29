// Removed unused Link import
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { 
  Heart,
  Target, 
  Users, 
  Shield, 
  Accessibility, 
  Globe,
  TrendingUp,
  Award
} from 'lucide-react';

interface ModernHeroSectionProps {
  stats?: {
    aps_servite: string;
    bandi_monitorati: string;
    cittadini_formati: string;
    finanziamenti_facilitati: string;
  };
}

export function ModernHeroSection({ stats }: ModernHeroSectionProps) {
  const defaultStats = {
    aps_servite: '500+',
    bandi_monitorati: '100+',
    cittadini_formati: '2000+',
    finanziamenti_facilitati: '€2M+'
  };

  const heroStats = stats || defaultStats;

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-iss-bordeaux-900 via-iss-bordeaux-800 to-iss-bordeaux-700">
      {/* Background Pattern */}
      <div 
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}
      />
      
      {/* Floating Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-iss-gold-400/10 rounded-full blur-xl animate-pulse" />
      <div className="absolute top-40 right-20 w-32 h-32 bg-iss-gold-400/5 rounded-full blur-2xl animate-pulse delay-1000" />
      <div className="absolute bottom-20 left-1/4 w-16 h-16 bg-white/5 rounded-full blur-xl animate-pulse delay-2000" />
      
      <div className="relative container mx-auto px-4 py-20 lg:py-32">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Hero Content */}
          <div className="text-white space-y-8">
            <div className="space-y-6">
              {/* Badge */}
              <Badge className="bg-iss-gold-500 text-iss-bordeaux-900 hover:bg-iss-gold-400 font-semibold px-4 py-2 text-sm">
                <Heart className="w-4 h-4 mr-2" />
                100% Gratuito e Accessibile
              </Badge>
              
              {/* Main Headline */}
              <h1 className="text-4xl lg:text-6xl font-bold leading-tight">
                Democratizziamo l'accesso ai
                <span className="text-iss-gold-400 block mt-2">
                  finanziamenti
                </span>
                <span className="text-white block">
                  per il terzo settore
                </span>
              </h1>
              
              {/* Subtitle */}
              <p className="text-xl lg:text-2xl text-iss-bordeaux-100 leading-relaxed max-w-2xl">
                La piattaforma ISS connette <strong className="text-iss-gold-300">500+ APS campane</strong> con opportunità di finanziamento, 
                formazione digitale gratuita e progetti di innovazione sociale.
              </p>
              
              {/* Value Proposition */}
              <div className="flex flex-wrap gap-4 text-iss-bordeaux-200">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-iss-gold-400" />
                  <span className="text-sm font-medium">Performance Enterprise</span>
                </div>
                <div className="flex items-center gap-2">
                  <Award className="w-5 h-5 text-iss-gold-400" />
                  <span className="text-sm font-medium">Zero Barriere</span>
                </div>
              </div>
            </div>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                size="lg" 
                className="bg-iss-gold-500 hover:bg-iss-gold-400 text-iss-bordeaux-900 font-semibold px-8 py-4 text-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                onClick={() => window.location.href = '/bandi'}
              >
                <Target className="w-5 h-5 mr-2" />
                Esplora Bandi
              </Button>
              
              <Button 
                variant="outline" 
                size="lg"
                className="border-2 border-white text-white hover:bg-white hover:text-iss-bordeaux-900 px-8 py-4 text-lg font-semibold transition-all duration-300 hover:scale-105"
                onClick={() => window.location.href = '/auth/register'}
              >
                <Users className="w-5 h-5 mr-2" />
                Registra la tua APS
              </Button>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap items-center gap-6 pt-8 border-t border-iss-bordeaux-600">
              <div className="flex items-center gap-2 text-iss-bordeaux-200">
                <Shield className="w-5 h-5 text-iss-gold-400" />
                <span className="text-sm font-medium">Sicuro e Certificato</span>
              </div>
              <div className="flex items-center gap-2 text-iss-bordeaux-200">
                <Accessibility className="w-5 h-5 text-iss-gold-400" />
                <span className="text-sm font-medium">WCAG 2.1 AA</span>
              </div>
              <div className="flex items-center gap-2 text-iss-bordeaux-200">
                <Globe className="w-5 h-5 text-iss-gold-400" />
                <span className="text-sm font-medium">Open Source</span>
              </div>
            </div>
          </div>
          
          {/* Hero Stats Grid */}
          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/15 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center">
                <div className="text-3xl lg:text-4xl font-bold text-iss-gold-400 mb-2">
                  {heroStats.aps_servite}
                </div>
                <div className="text-sm text-iss-bordeaux-100 font-medium">
                  APS Campane Servite
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/15 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center">
                <div className="text-3xl lg:text-4xl font-bold text-iss-gold-400 mb-2">
                  {heroStats.bandi_monitorati}
                </div>
                <div className="text-sm text-iss-bordeaux-100 font-medium">
                  Bandi Monitorati 24/7
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/15 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center">
                <div className="text-3xl lg:text-4xl font-bold text-iss-gold-400 mb-2">
                  {heroStats.cittadini_formati}
                </div>
                <div className="text-sm text-iss-bordeaux-100 font-medium">
                  Cittadini Formati GRATIS
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/15 transition-all duration-300 hover:scale-105">
              <CardContent className="p-6 text-center">
                <div className="text-3xl lg:text-4xl font-bold text-iss-gold-400 mb-2">
                  {heroStats.finanziamenti_facilitati}
                </div>
                <div className="text-sm text-iss-bordeaux-100 font-medium">
                  Finanziamenti Facilitati
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      
      {/* Wave Separator */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" className="w-full h-12 fill-white">
          <path d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1392,42.7L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z" />
        </svg>
      </div>
    </section>
  );
}
