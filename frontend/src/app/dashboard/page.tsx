"use client";

import { useEffect, useState } from 'react';
import DashboardCard, { PointsIcon, TokenIcon, WalletIcon } from '../components/DashboardCard';
import RecentActivity from '../components/RecentActivity';
import { useRouter } from 'next/navigation';
import { useAuth } from '../context/AuthContext';
import AppLayout from '../components/AppLayout';
import { getPoints } from '@/lib/api/points';
import { PointsResponse } from '@/lib/api/types';
import { toast } from 'react-toastify';

export default function Dashboard() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  const [pointsData, setPointsData] = useState<PointsResponse | null>(null);
  const [pointsError, setPointsError] = useState<string | null>(null);

  const handleRedeemPoints = async () => {
    try {
      if (!loading && isAuthenticated) {
        router.push('/wallet');
      }
    } catch (error) {
      console.error('Error redeeming points:', error);
      toast.error('Failed to redeem points.');
    }
  };
  

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [loading, isAuthenticated, router]);

  useEffect(() => {
    const fetchPoints = async () => {
      try {
        if (isAuthenticated) {
          const data = await getPoints();
          console.log("points data:", data);
          if (!data || Object.keys(data).length === 0) {
            setPointsData(null);
          }
          else {
          setPointsData(data);
          setPointsError(null); // clear any old error
        }
      }
      } catch (err) {
        console.error('Error fetching points:', err);
        // setPointsError('Failed to load points. Please try again later.');
      }
    };

    if (!loading && isAuthenticated) {
      fetchPoints();
    }
  }, [loading, isAuthenticated]);

  
  // if (loading) return <div>Loading...</div>;

  if (!isAuthenticated) return null;

  if (pointsError) {
    return (
      <AppLayout>
        <div className="text-center text-red-600 mt-10">
          <p className="text-lg font-semibold">{pointsError}</p>
        </div>
      </AppLayout>
    );
  }

  // if (!pointsData) return <div>Loading points...</div>;

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <button className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          onClick={handleRedeemPoints}
          >
            Redeem Points
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <DashboardCard 
            title="Total Points" 
            value={pointsData?.total_points.toLocaleString() || "No data"} 
            icon={<PointsIcon />}
            trend="up"
            trendValue="5% from yesterday"
          />
          <DashboardCard 
            title="Available for Redemption" 
            value={pointsData?.available_for_redemtion?.toLocaleString() || "No data"} 
            icon={<WalletIcon />}
          />
          <DashboardCard 
            title="ZVIO Tokens Redeemed" 
            value={pointsData?.zavio_token_rewarded?.toLocaleString() || "No data"} 
            icon={<TokenIcon />}
          />
        </div>

        {/* Optional: future charts */}
        {/* <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Points Accumulation</h2>
          <PointsChart />
        </div> */}

        <RecentActivity />
      </div>
    </AppLayout>
  );
}
