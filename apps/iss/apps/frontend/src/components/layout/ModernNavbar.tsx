import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Menu, 
  X, 
  Search, 
  User, 
  LogOut, 
  ChevronDown,
  Target,
  BookOpen,
  Calendar,
  Heart,
  Settings,
  Bell,
  Home,
  Rocket,
  Newspaper,
  Handshake
} from 'lucide-react';

interface ModernNavbarProps {
  className?: string;
}

interface NavigationItem {
  name: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
  badge?: string;
  description?: string;
  isNew?: boolean;
}

export const ModernNavbar: React.FC<ModernNavbarProps> = ({ className = '' }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  
  // Mock user state - sostituire con context reale
  const [user, setUser] = useState<any>(null);
  const isAuthenticated = !!user;

  // Scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Check for existing auth
  useEffect(() => {
    const token = localStorage.getItem('iss_token');
    const userData = localStorage.getItem('iss_user');
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
  }, []);

  const navigation: NavigationItem[] = [
    { 
      name: 'Home', 
      href: '/', 
      icon: Home,
      description: 'Torna alla homepage'
    },
    { 
      name: 'Bandi', 
      href: '/bandi', 
      icon: Target,
      badge: 'Hub APS',
      description: 'Cerca bandi di finanziamento'
    },
    { 
      name: 'Corsi', 
      href: '/corsi', 
      icon: BookOpen,
      badge: 'Gratuiti',
      description: 'Formazione digitale inclusiva',
      isNew: true
    },
    { 
      name: 'Eventi', 
      href: '/eventi', 
      icon: Calendar,
      badge: 'ISS',
      description: 'Workshop e hackathon sociali',
      isNew: true
    },
    { 
      name: 'Progetti', 
      href: '/progetti', 
      icon: Rocket,
      badge: 'Attivi',
      description: 'Portfolio progetti ISS',
      isNew: true
    },
    { 
      name: 'Volontariato', 
      href: '/volontariato', 
      icon: Heart,
      badge: 'Matching',
      description: 'Opportunità volontariato digitale',
      isNew: true
    },
    { 
      name: 'News', 
      href: '/news', 
      icon: Newspaper,
      badge: 'Blog',
      description: 'Notizie e aggiornamenti ISS',
      isNew: true
    },
    { 
      name: 'Partners', 
      href: '/partners', 
      icon: Handshake,
      badge: 'Rete',
      description: 'Collaborazioni e testimonials',
      isNew: true
    },
    { 
      name: 'Dashboard', 
      href: '/dashboard', 
      icon: Settings,
      badge: 'Area Riservata',
      description: 'Pannello di controllo personale'
    }
  ];

  const handleNavigation = (href: string) => {
    window.location.href = href;
    setIsMenuOpen(false);
    setActiveDropdown(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('iss_token');
    localStorage.removeItem('iss_user');
    setUser(null);
    window.location.href = '/';
  };

  const getUserInitials = (user: any) => {
    if (!user) return 'U';
    return `${user.nome?.[0] || ''}${user.cognome?.[0] || ''}`.toUpperCase();
  };

  const getUserRole = (role: string) => {
    const roleMap: Record<string, string> = {
      'admin': 'Amministratore',
      'aps_responsabile': 'Responsabile APS',
      'aps_operatore': 'Operatore APS',
      'cittadino': 'Cittadino',
      'volontario': 'Volontario'
    };
    return roleMap[role] || role;
  };

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled 
          ? 'bg-white/98 backdrop-blur-xl shadow-2xl border-b border-iss-bordeaux-100/50' 
          : 'bg-white/85 backdrop-blur-lg shadow-lg'
      } ${className}`}
      style={{
        backgroundImage: isScrolled 
          ? 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.98) 100%)'
          : 'linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(248,250,252,0.90) 100%)'
      }}
    >
      <div className="container mx-auto px-4">
        <div className="flex h-16 lg:h-18 items-center justify-between">
          {/* Logo ISS Ufficiale - Desktop Ottimizzato */}
          <div 
            className="flex items-center space-x-3 lg:space-x-4 cursor-pointer group"
            onClick={() => handleNavigation('/')}
          >
            {/* Logo Container - Dimensioni Desktop Ottimizzate */}
            <div className="h-10 w-10 sm:h-12 sm:w-12 lg:h-14 lg:w-14 relative overflow-hidden flex-shrink-0">
              {/* Glow Effect Background - Ridotto su Desktop */}
              <div className="absolute inset-0 bg-gradient-to-br from-iss-bordeaux-500/15 to-iss-gold-500/15 lg:from-iss-bordeaux-500/10 lg:to-iss-gold-500/10 rounded-full blur-md group-hover:blur-lg transition-all duration-500 scale-105 group-hover:scale-115" />
              
              {/* Logo Container - Stile Desktop Raffinato */}
              <div className="relative h-full w-full bg-white/95 backdrop-blur-sm rounded-full p-0.5 lg:p-1 shadow-md group-hover:shadow-lg transition-all duration-300 border border-white/60 group-hover:border-iss-gold-300/40">
                <img 
                  src="/iss-logo.svg" 
                  alt="ISS - Innovazione Sociale Salernitana" 
                  className="w-full h-full object-contain drop-shadow-sm group-hover:drop-shadow transition-all duration-300 group-hover:scale-102"
                />
              </div>
              
              {/* Pulse Ring - Più Sottile su Desktop */}
              <div className="absolute inset-0 rounded-full border border-iss-gold-400/20 lg:border-iss-gold-400/15 group-hover:border-iss-gold-500/30 transition-colors duration-300" />
            </div>
            
            {/* Brand Text - Desktop Compatto e Professionale */}
            <div className="hidden sm:block min-w-0">
              <div className="text-base lg:text-lg xl:text-xl font-bold bg-gradient-to-r from-iss-bordeaux-900 via-iss-bordeaux-700 to-iss-gold-600 bg-clip-text text-transparent group-hover:from-iss-gold-600 group-hover:to-iss-bordeaux-900 transition-all duration-500 leading-tight">
                Innovazione Sociale Salernitana
              </div>
              <div className="text-xs lg:text-xs xl:text-sm text-gray-600 font-medium group-hover:text-iss-bordeaux-700 transition-colors duration-300 leading-tight mt-0.5 max-w-xs lg:max-w-sm xl:max-w-md truncate">
                Hub Bandi APS • Formazione Digitale • 500+ APS
              </div>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navigation.slice(0, 5).map((item) => (
              <div key={item.name} className="relative group">
                <button
                  onClick={() => handleNavigation(item.href)}
                  className="relative flex items-center gap-1 px-3 py-2 rounded-lg text-xs font-semibold text-gray-700 hover:text-iss-bordeaux-900 transition-all duration-300 group overflow-hidden"
                  onMouseEnter={() => setActiveDropdown(item.name)}
                  onMouseLeave={() => setActiveDropdown(null)}
                >
                  {/* Hover Background Effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-iss-bordeaux-50 to-iss-gold-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl" />
                  <div className="absolute inset-0 bg-white/50 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl" />
                  
                  {/* Content */}
                  <div className="relative z-10 flex items-center gap-2">
                    {item.icon && <item.icon className="w-4 h-4" />}
                    <span className="truncate">{item.name}</span>
                    {item.badge && (
                      <Badge 
                        className={`text-xs ${
                          item.isNew 
                            ? 'bg-green-100 text-green-800 border-green-200' 
                            : 'bg-iss-gold-100 text-iss-gold-800 border-iss-gold-200'
                        }`}
                      >
                        {item.badge}
                      </Badge>
                    )}
                    {item.isNew && (
                      <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    )}
                  </div>
                </button>
                
                {/* Tooltip */}
                {activeDropdown === item.name && item.description && (
                  <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg whitespace-nowrap z-50">
                    {item.description}
                    <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45" />
                  </div>
                )}
              </div>
            ))}
            
            {/* Menu "Altro" per pagine extra */}
            {navigation.length > 5 && (
              <div className="relative group">
                <button
                  onClick={() => setActiveDropdown(activeDropdown === 'more' ? null : 'more')}
                  className="relative flex items-center gap-1 px-3 py-2 rounded-lg text-xs font-semibold text-gray-700 hover:text-iss-bordeaux-900 transition-all duration-300 group overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-iss-bordeaux-50 to-iss-gold-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl" />
                  <div className="absolute inset-0 bg-white/50 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl" />
                  
                  <div className="relative z-10 flex items-center gap-1">
                    <span>Altro</span>
                    <ChevronDown className="w-3 h-3" />
                  </div>
                </button>
                
                {/* Dropdown per pagine extra */}
                {activeDropdown === 'more' && (
                  <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-200 py-2 z-50">
                    {navigation.slice(5).map((item) => (
                      <button
                        key={item.name}
                        onClick={() => handleNavigation(item.href)}
                        className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        {item.icon && <item.icon className="w-4 h-4 mr-3" />}
                        <span>{item.name}</span>
                        {item.isNew && (
                          <Badge className="ml-auto bg-green-100 text-green-800 text-xs">
                            NEW
                          </Badge>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-2">
            {/* Search Button */}
            <Button 
              variant="ghost" 
              size="icon" 
              className="hidden md:inline-flex hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900"
            >
              <Search className="h-4 w-4" />
              <span className="sr-only">Cerca</span>
            </Button>

            {/* Notifications (if authenticated) */}
            {isAuthenticated && (
              <Button 
                variant="ghost" 
                size="icon" 
                className="relative hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900"
              >
                <Bell className="h-4 w-4" />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">3</span>
                </div>
                <span className="sr-only">Notifiche</span>
              </Button>
            )}

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="relative group">
                <button
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-iss-bordeaux-50 transition-colors"
                  onClick={() => setActiveDropdown(activeDropdown === 'user' ? null : 'user')}
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-iss-bordeaux-600 to-iss-gold-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                    {getUserInitials(user)}
                  </div>
                  <div className="hidden sm:block text-left">
                    <div className="text-sm font-medium text-gray-900">
                      {user?.nome} {user?.cognome}
                    </div>
                    <div className="text-xs text-gray-600">
                      {getUserRole(user?.role)}
                    </div>
                  </div>
                  <ChevronDown className="w-4 h-4 text-gray-500" />
                </button>

                {/* User Dropdown */}
                {activeDropdown === 'user' && (
                  <div className="absolute right-0 top-full mt-2 w-64 bg-white rounded-xl shadow-xl border border-gray-200 py-2 z-50">
                    <div className="px-4 py-3 border-b border-gray-100">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-iss-bordeaux-600 to-iss-gold-500 rounded-full flex items-center justify-center text-white font-semibold">
                          {getUserInitials(user)}
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">
                            {user?.nome} {user?.cognome}
                          </div>
                          <div className="text-sm text-gray-600">
                            {user?.email}
                          </div>
                          <div className="text-xs text-iss-bordeaux-600 font-medium">
                            {getUserRole(user?.role)}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="py-2">
                      <button
                        onClick={() => handleNavigation('/dashboard')}
                        className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      >
                        <User className="w-4 h-4 mr-3" />
                        Dashboard
                      </button>
                      <button
                        onClick={() => handleNavigation('/settings')}
                        className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      >
                        <Settings className="w-4 h-4 mr-3" />
                        Impostazioni
                      </button>
                    </div>
                    
                    <div className="border-t border-gray-100 py-2">
                      <button
                        onClick={handleLogout}
                        className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                      >
                        <LogOut className="w-4 h-4 mr-3" />
                        Logout
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="hidden sm:flex items-center space-x-2">
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => handleNavigation('/auth/login')}
                  className="hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900"
                >
                  Accedi
                </Button>
                <Button 
                  size="sm"
                  onClick={() => handleNavigation('/auth/register')}
                  className="bg-iss-bordeaux-900 hover:bg-iss-bordeaux-800 text-white"
                >
                  Registrati
                </Button>
              </div>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              <span className="sr-only">Toggle menu</span>
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div 
          className={`lg:hidden transition-all duration-300 ease-in-out ${
            isMenuOpen 
              ? 'max-h-screen opacity-100 pb-6' 
              : 'max-h-0 opacity-0 overflow-hidden'
          }`}
        >
          <div className="border-t border-gray-200 pt-4">
            <div className="space-y-1">
              {navigation.map((item) => (
                <button
                  key={item.name}
                  onClick={() => handleNavigation(item.href)}
                  className="flex items-center justify-between w-full px-4 py-3 rounded-lg text-base font-medium text-gray-700 hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    {item.icon && <item.icon className="w-5 h-5" />}
                    <span>{item.name}</span>
                    {item.isNew && (
                      <div className="w-2 h-2 bg-green-500 rounded-full" />
                    )}
                  </div>
                  {item.badge && (
                    <Badge 
                      className={`text-xs ${
                        item.isNew 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-iss-gold-100 text-iss-gold-800'
                      }`}
                    >
                      {item.badge}
                    </Badge>
                  )}
                </button>
              ))}
            </div>

            {/* Mobile Auth Section */}
            {!isAuthenticated ? (
              <div className="mt-6 pt-6 border-t border-gray-200 space-y-3">
                <Button
                  onClick={() => handleNavigation('/auth/login')}
                  variant="outline"
                  className="w-full justify-center border-iss-bordeaux-200 text-iss-bordeaux-900 hover:bg-iss-bordeaux-50"
                >
                  Accedi
                </Button>
                <Button
                  onClick={() => handleNavigation('/auth/register')}
                  className="w-full justify-center bg-iss-bordeaux-900 hover:bg-iss-bordeaux-800 text-white"
                >
                  Registrati Gratuitamente
                </Button>
              </div>
            ) : (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="flex items-center space-x-3 px-4 py-3 bg-iss-bordeaux-50 rounded-lg mb-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-iss-bordeaux-600 to-iss-gold-500 rounded-full flex items-center justify-center text-white font-semibold">
                    {getUserInitials(user)}
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">
                      {user?.nome} {user?.cognome}
                    </div>
                    <div className="text-sm text-gray-600">
                      {getUserRole(user?.role)}
                    </div>
                  </div>
                </div>
                
                <div className="space-y-1">
                  <button
                    onClick={() => handleNavigation('/dashboard')}
                    className="flex items-center w-full px-4 py-3 text-base font-medium text-gray-700 hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900 rounded-lg transition-colors"
                  >
                    <User className="w-5 h-5 mr-3" />
                    Dashboard
                  </button>
                  <button
                    onClick={() => handleNavigation('/settings')}
                    className="flex items-center w-full px-4 py-3 text-base font-medium text-gray-700 hover:bg-iss-bordeaux-50 hover:text-iss-bordeaux-900 rounded-lg transition-colors"
                  >
                    <Settings className="w-5 h-5 mr-3" />
                    Impostazioni
                  </button>
                  <button
                    onClick={handleLogout}
                    className="flex items-center w-full px-4 py-3 text-base font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <LogOut className="w-5 h-5 mr-3" />
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Overlay for mobile menu */}
      {isMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/20 backdrop-blur-sm lg:hidden z-40"
          onClick={() => setIsMenuOpen(false)}
        />
      )}
    </header>
  );
};
