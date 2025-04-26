"use client"
import { useEffect, useState } from 'react';
import AppLayout from "../components/AppLayout";
import { Activity } from "@/lib/api/types";
import { fetchRewards } from '@/lib/api/activity';

interface Reward {
  id: number;
  date: string;
  points: number;
  activity: string;
  status: 'Completed' | 'Pending' | 'Failed';
}

export default function Rewards() {
  const [rewardsData, setRewardsData] = useState<Reward[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadRewards = async () => {
      try {
        const activities: Activity[] = await fetchRewards();

        const formattedRewards = activities.map((item) => ({
          id: item.id,
          date: item.activity_timestamp,
          points: item.points,
          activity: item.description,
          status: 'Completed' as const // If needed, change this based on actual logic
        }));

        setRewardsData(formattedRewards);
        setError(null);
      } catch (err: any) {
        console.error('Failed to fetch rewards:', err);
        setError('Failed to load rewards.');
      } finally {
        setLoading(false);
      }
    };

    loadRewards();
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Rewards</h1>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Daily Points Breakdown</h2>

          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Points Earned</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Activity</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {rewardsData.map((reward, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(reward.date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric'
                        })}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {reward.points.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{reward.activity}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          reward.status === 'Completed' 
                            ? 'bg-green-100 text-green-800' 
                            : reward.status === 'Pending'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                        }`}>
                          {reward.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
