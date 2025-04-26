import React, { useEffect, useState } from 'react';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/outline';
import { Activity } from '@/lib/api/types';
import { fetchActivities } from '@/lib/api/activity';

export default function RecentActivity() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getActivities = async () => {
      try {
        const activitiesData = await fetchActivities();
        setActivities(activitiesData);
      } catch (error) {
        console.error('Error fetching activities:', error);
        setError('Failed to load activities.');
      } finally {
        setLoading(false);
      }
    };
    getActivities();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-lg font-medium mb-4">Recent Activity</h2>
      <div className="flow-root">
        <ul className="-mb-8">
          {activities.map((activity, activityIdx) => (
            <li key={activityIdx}>
              <div className="relative pb-8">
                {activityIdx !== activities.length - 1 && (
                  <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                )}
                <div className="relative flex space-x-3">
                  <div>
                    <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${
                      activity.isCredit ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {activity.isCredit ? (
                        <ArrowUpIcon className="h-5 w-5" aria-hidden="true" />
                      ) : (
                        <ArrowDownIcon className="h-5 w-5" aria-hidden="true" />
                      )}
                    </span>
                  </div>
                  <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                    <div>
                      <p className="text-sm text-gray-800">
                        {activity.description}{' '}
                        <span className={`font-medium ${
                          activity.isCredit ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {activity.isCredit ? '+' : '-'}{activity.points} points
                        </span>
                      </p>
                    </div>
                    <div className="text-right text-sm whitespace-nowrap text-gray-500">
                    <time dateTime={activity.activity_timestamp}>
                      {new Date(activity.activity_timestamp).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true
                      })}
                    </time>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
