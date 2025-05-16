// components/Header.tsx
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import UserDropdown from './UserDropdown';
import { getAllNodes, getuserNodes } from '@/lib/api/nodes';
import { NodesResponse, userNodes } from '@/lib/api';

export default function Header() {
  const { user } = useAuth();
  const [nodes, setNodes] = useState<NodesResponse[]>([]);
  const [userNodesData, setUserNodesData] = useState<userNodes | null>(null); // Renamed to avoid conflict
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch both data in parallel
        const [allNodes, userNodes] = await Promise.all([
          getAllNodes(),
          user?.id ? getuserNodes(Number(user.id)) : Promise.resolve(null)
        ]);
        
        setNodes(allNodes);
        setUserNodesData(userNodes);
      } catch (err) {
        setError('Failed to fetch data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (user?.role === 'admin' || user?.role === 'user') {
      fetchData();
    }
  }, [user?.role, user?.id]); // Added user.id dependency

  const activeNodes = nodes.find(node => node.status === 'active');

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        {/* Logo Section */}
        <div className="flex items-center justify-center py-4">
          <img 
            src="/logo.jpeg" 
            alt="Zaivio Logo" 
            className="h-12 w-auto"
          />
        </div>

        <div className="flex items-center space-x-6">
          {/* Admin/User Stats */}
          {(user?.role === 'admin' || user?.role === 'user') && (
            <div className="flex items-center space-x-4 bg-gray-50 rounded-lg px-4 py-2">
              {loading ? (
                <div className="flex space-x-4">
                  <div className="h-8 w-20 bg-gray-200 rounded animate-pulse"></div>
                  <div className="h-8 w-20 bg-gray-200 rounded animate-pulse"></div>
                </div>
              ) : error ? (
                <span className="text-red-500 text-sm">{error}</span>
              ) : (
                <>
                  {/* Your Nodes - Will show if userNodesData exists */}
                  {userNodesData && (
                    <>
                      <div className="text-center">
                        <p className="text-xs text-gray-500">Your Nodes</p>
                        <p className="text-lg font-semibold text-blue-600">
                          {userNodesData.nodes_assigned ?? 0}
                        </p>
                      </div>
                      <div className="h-8 border-r border-gray-200"></div>
                    </>
                  )}

                  {/* Active Nodes - Will show if activeNodes exists */}
                  {activeNodes && (
                    <>
                      <div className="text-center">
                        <p className="text-xs text-gray-500">Active Nodes</p>
                        <p className="text-lg font-semibold text-indigo-600">
                          {activeNodes.total_nodes ?? 0}
                        </p>
                      </div>
                      <div className="h-8 border-r border-gray-200"></div>
                    </>
                  )}

                  {/* Daily Reward - Will show if activeNodes exists */}
                  {activeNodes && (
                    <div className="text-center">
                      <p className="text-xs text-gray-500">Daily Reward</p>
                      <p className="text-lg font-semibold text-green-600">
                        {activeNodes.daily_reward && activeNodes.total_nodes
                          ? (activeNodes.daily_reward / activeNodes.total_nodes).toFixed(2)
                          : '0.00'}
                      </p>
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          <button className="p-2 rounded-full text-gray-500 hover:text-gray-700 hover:bg-gray-100">
            <BellIcon />
          </button>
          <UserDropdown />
        </div>
      </div>
    </header>
  );
}

// BellIcon remains the same

function BellIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
  );
}