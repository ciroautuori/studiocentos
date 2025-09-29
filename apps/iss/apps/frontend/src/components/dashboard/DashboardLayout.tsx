import React from 'react';
import { cn } from '@/utils/cn';
import { DashboardSidebar } from './DashboardSidebar';
// import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';

interface DashboardLayoutProps {
  children: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
  userRole: 'admin' | 'user' | 'partner' | 'moderator';
  // breadcrumbs?: Array<{ label: string; href?: string }>;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  title,
  description,
  action,
  className,
  userRole
}) => {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <DashboardSidebar userRole={userRole} />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex h-16 items-center justify-between px-6">
            <div className="flex items-center gap-4">
              <h2 className="text-lg font-semibold">{title}</h2>
            </div>
            {action && (
              <div className="flex items-center gap-2">
                {action}
              </div>
            )}
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto">
          <div className="container mx-auto p-6">
            <div className={cn("space-y-6", className)}>
              {/* Page Header */}
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
                {description && (
                  <p className="text-muted-foreground">{description}</p>
                )}
              </div>

              {/* Page Content */}
              <div className="space-y-6">
                {children}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};
