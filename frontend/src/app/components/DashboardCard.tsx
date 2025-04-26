// components/DashboardCard.tsx
import { ReactNode } from 'react';

interface DashboardCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  trend?: 'up' | 'down';
  trendValue?: string;
}

export default function DashboardCard({ 
  title, 
  value, 
  icon, 
  trend, 
  trendValue 
}: DashboardCardProps) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
              {icon}
            </div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd>
                <div className="text-lg font-medium text-gray-900">{value}</div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      {trend && trendValue && (
        <div className={`px-5 py-3 ${trend === 'up' ? 'bg-green-50' : 'bg-red-50'} rounded-b-lg`}>
          <div className="text-sm">
            <span className={`font-medium ${trend === 'up' ? 'text-green-700' : 'text-red-700'} flex items-center`}>
              {trend === 'up' ? (
                <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12 7a1 1 0 01-1-1V5.414l-4.293 4.293a1 1 0 01-1.414-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L13 5.414V6a1 1 0 01-1 1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12 13a1 1 0 100-2H5.414l4.293-4.293a1 1 0 00-1.414-1.414l-6 6a1 1 0 000 1.414l6 6a1 1 0 001.414-1.414L5.414 13H12z" clipRule="evenodd" />
                </svg>
              )}
              {trendValue}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

// Example icon component that could be used with DashboardCard
export function PointsIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  );
}

export function WalletIcon() {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
      </svg>
    );
  }
  
  export function TokenIcon() {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    );
  }