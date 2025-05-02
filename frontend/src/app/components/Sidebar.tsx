'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  DashboardIcon, 
  RewardsIcon, 
  WalletIcon, 
  TransactionIcon, 
  AdminIcon,
  UsersIcon,
  NodesIcon, 
  ContactIcon
} from './icons';
import { useState } from 'react';
import clsx from 'clsx';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
  const pathname = usePathname();
  const [adminMenuOpen, setAdminMenuOpen] = useState(pathname.startsWith('/admin'));
  const { user } = useAuth();

  const isAdmin = user?.role === 'admin' 
  
  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: DashboardIcon },
    { name: 'Rewards', href: '/rewards', icon: RewardsIcon },
    { name: 'Wallet', href: '/wallet', icon: WalletIcon },
    { name: 'Transactions', href: '/transactions', icon: TransactionIcon },
    ...(isAdmin ? [{
      name: 'Admin', 
      href: '/admin/users', 
      icon: AdminIcon,
      subItems: [
        { name: 'Users', href: '/admin/users', icon: UsersIcon },
        { name: 'Nodes', href: '/admin/nodes', icon: NodesIcon }
      ]
    }] : []),
    { name: 'Contact', href: 'http://Zaivio.com', icon: ContactIcon, external: true }, // New link
  ];
  
  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64 border-r border-gray-200 bg-white">
        {/* Logo Section */}
        <div className="flex items-center justify-center py-4">
          <img 
            src="/logo.jpeg" 
            alt="Zaivio Logo" 
            className="h-12 w-auto"
          />
        </div>
        <div className="h-0 flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <nav className="flex-1 px-2 space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href || 
                (item.subItems && item.subItems.some(subItem => pathname === subItem.href));
              
              if (item.external) {
                return (
                  <a
                    key={item.name}
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={clsx(
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md',
                      'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    )}
                  >
                    {item.icon && (
                      <item.icon 
                        className={clsx(
                          'mr-3 flex-shrink-0 h-6 w-6',
                          'text-gray-400 group-hover:text-gray-500'
                        )}
                      />
                    )}
                    {item.name}
                  </a>
                );
              }

              if (item.subItems) {
                return (
                  <div key={item.name}>
                    <button
                      onClick={() => setAdminMenuOpen(!adminMenuOpen)}
                      className={clsx(
                        'group w-full flex items-center px-2 py-2 text-sm font-medium rounded-md',
                        isActive ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      )}
                    >
                      <div className="flex items-center">
                        {item.icon && (
                          <item.icon 
                            active={isActive} 
                            className={clsx(
                              'mr-3 flex-shrink-0 h-6 w-6',
                              isActive ? 'text-indigo-500' : 'text-gray-400 group-hover:text-gray-500'
                            )}
                          />
                        )}
                        {item.name}
                      </div>
                      <svg
                        className={clsx(
                          'ml-1 h-5 w-5 transform transition-transform',
                          adminMenuOpen ? 'rotate-90' : 'rotate-0'
                        )}
                        viewBox="0 0 20 20"
                        aria-hidden="true"
                      >
                        <path d="M6 6L14 10L6 14V6Z" fill="currentColor" />
                      </svg>
                    </button>

                    {adminMenuOpen && (
                      <div className="ml-8 mt-1 space-y-1">
                        {item.subItems.map((subItem) => (
                          <Link
                            key={subItem.name}
                            href={subItem.href}
                            className={clsx(
                              'group flex items-center px-2 py-2 text-sm font-medium rounded-md',
                              pathname === subItem.href
                                ? 'bg-indigo-50 text-indigo-700'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                            )}
                          >
                            {subItem.icon && (
                              <subItem.icon 
                                active={pathname === subItem.href} 
                                className={clsx(
                                  'mr-3 flex-shrink-0 h-5 w-5',
                                  pathname === subItem.href
                                    ? 'text-indigo-500'
                                    : 'text-gray-400 group-hover:text-gray-500'
                                )}
                              />
                            )}
                            {subItem.name}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              } else {
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={clsx(
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md',
                      isActive ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    )}
                  >
                    {item.icon && (
                      <item.icon 
                        active={isActive} 
                        className={clsx(
                          'mr-3 flex-shrink-0 h-6 w-6',
                          isActive ? 'text-indigo-500' : 'text-gray-400 group-hover:text-gray-500'
                        )}
                      />
                    )}
                    {item.name}
                  </Link>
                );
              }
            })}
          </nav>
        </div>
      </div>
    </div>
  );
}