import { cn } from "@/utils/cn"
import { Button } from "@/components/ui/button"
// import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { 
  LayoutDashboard,
  Users,
  FileText,
  Calendar,
  Heart,
  Building,
  Settings,
  BarChart3,
  Shield,
  Database,
  Mail,
  Bell,
  LogOut,
  ChevronLeft,
  ChevronRight
} from "lucide-react"
import { Link, useLocation } from "@tanstack/react-router"
import { useState } from "react"

interface SidebarProps {
  userRole: 'admin' | 'user' | 'partner' | 'moderator'
  className?: string
}

export function DashboardSidebar({ userRole, className }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  const adminMenuItems = [
    {
      title: "Dashboard",
      icon: LayoutDashboard,
      href: "/dashboard/admin",
      badge: null
    },
    {
      title: "Gestione Utenti",
      icon: Users,
      href: "/dashboard/admin/users",
      badge: "5"
    },
    {
      title: "Gestione Bandi",
      icon: FileText,
      href: "/dashboard/admin/bandi",
      badge: "3"
    },
    {
      title: "Eventi & Corsi",
      icon: Calendar,
      href: "/dashboard/admin/events",
      badge: null
    },
    {
      title: "Volontariato",
      icon: Heart,
      href: "/dashboard/admin/volunteer",
      badge: "12"
    },
    {
      title: "Partner",
      icon: Building,
      href: "/dashboard/admin/partners",
      badge: null
    },
    {
      title: "Analytics",
      icon: BarChart3,
      href: "/dashboard/admin/analytics",
      badge: null
    },
    {
      title: "Sistema",
      icon: Database,
      href: "/dashboard/admin/system",
      badge: null
    },
    {
      title: "Sicurezza",
      icon: Shield,
      href: "/dashboard/admin/security",
      badge: "2"
    },
    {
      title: "Notifiche",
      icon: Bell,
      href: "/dashboard/admin/notifications",
      badge: "8"
    },
    {
      title: "Impostazioni",
      icon: Settings,
      href: "/dashboard/admin/settings",
      badge: null
    }
  ]

  const userMenuItems = [
    {
      title: "Dashboard",
      icon: LayoutDashboard,
      href: "/dashboard/user",
      badge: null
    },
    {
      title: "I Miei Corsi",
      icon: FileText,
      href: "/dashboard/user/courses",
      badge: "3"
    },
    {
      title: "Eventi",
      icon: Calendar,
      href: "/dashboard/user/events",
      badge: "2"
    },
    {
      title: "Volontariato",
      icon: Heart,
      href: "/dashboard/user/volunteer",
      badge: "1"
    },
    {
      title: "Messaggi",
      icon: Mail,
      href: "/dashboard/user/messages",
      badge: "4"
    },
    {
      title: "Profilo",
      icon: Users,
      href: "/dashboard/user/profile",
      badge: null
    },
    {
      title: "Impostazioni",
      icon: Settings,
      href: "/dashboard/user/settings",
      badge: null
    }
  ]

  const partnerMenuItems = [
    {
      title: "Dashboard",
      icon: LayoutDashboard,
      href: "/dashboard/partner",
      badge: null
    },
    {
      title: "I Miei Progetti",
      icon: FileText,
      href: "/dashboard/partner/projects",
      badge: "7"
    },
    {
      title: "Team",
      icon: Users,
      href: "/dashboard/partner/team",
      badge: "25"
    },
    {
      title: "Collaborazioni",
      icon: Building,
      href: "/dashboard/partner/collaborations",
      badge: "4"
    },
    {
      title: "Analytics",
      icon: BarChart3,
      href: "/dashboard/partner/analytics",
      badge: null
    },
    {
      title: "Documenti",
      icon: FileText,
      href: "/dashboard/partner/documents",
      badge: null
    },
    {
      title: "Messaggi",
      icon: Mail,
      href: "/dashboard/partner/messages",
      badge: "2"
    },
    {
      title: "Impostazioni",
      icon: Settings,
      href: "/dashboard/partner/settings",
      badge: null
    }
  ]

  const getMenuItems = () => {
    switch (userRole) {
      case 'admin':
        return adminMenuItems
      case 'user':
        return userMenuItems
      case 'partner':
        return partnerMenuItems
      default:
        return userMenuItems
    }
  }

  const getRoleColor = () => {
    switch (userRole) {
      case 'admin':
        return 'text-red-600 bg-red-50'
      case 'user':
        return 'text-green-600 bg-green-50'
      case 'partner':
        return 'text-purple-600 bg-purple-50'
      default:
        return 'text-blue-600 bg-blue-50'
    }
  }

  const menuItems = getMenuItems()

  return (
    <div className={cn(
      "flex flex-col border-r bg-background",
      collapsed ? "w-16" : "w-64",
      "transition-all duration-300",
      className
    )}>
      {/* Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center", getRoleColor())}>
              {userRole === 'admin' && <Shield className="h-4 w-4" />}
              {userRole === 'user' && <Users className="h-4 w-4" />}
              {userRole === 'partner' && <Building className="h-4 w-4" />}
            </div>
            <div>
              <p className="text-sm font-medium capitalize">{userRole}</p>
              <p className="text-xs text-muted-foreground">Dashboard</p>
            </div>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setCollapsed(!collapsed)}
          className="h-8 w-8 p-0"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <div className="flex-1 px-3 py-4 overflow-y-auto">
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.href}
                to={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                  "hover:bg-accent hover:text-accent-foreground",
                  isActive && "bg-accent text-accent-foreground font-medium",
                  collapsed && "justify-center px-2"
                )}
              >
                <item.icon className="h-4 w-4 flex-shrink-0" />
                {!collapsed && (
                  <>
                    <span className="flex-1">{item.title}</span>
                    {item.badge && (
                      <Badge variant="secondary" className="h-5 text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </>
                )}
              </Link>
            )
          })}
        </nav>
      </div>

      {/* Footer */}
      <div className="border-t p-3">
        <Button
          variant="ghost"
          className={cn(
            "w-full justify-start gap-3 text-sm",
            collapsed && "justify-center px-2"
          )}
        >
          <LogOut className="h-4 w-4" />
          {!collapsed && "Logout"}
        </Button>
      </div>
    </div>
  )
}
