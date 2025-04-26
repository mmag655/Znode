"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AppLayout from '@/app/components/AppLayout';
import { getAllUsers } from '@/lib/api';

interface User {
  user_id: number;
  avatar: string;
  username: string;
  email: string;
  assigned_nodes: number;
  status: 'active' | 'inactive';
}

export default function AdminUsers() {
  const [usersData, setUsersData] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState<string>('username');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [usersPerPage, setUsersPerPage] = useState(5);

  const router = useRouter();
  const isAdmin = true;

  useEffect(() => {
    if (!isAdmin) {
      router.push('/');
      return;
    }

    const fetchUsers = async () => {
      try {
        const usersList = await getAllUsers();
        setUsersData(usersList);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch users:', err);
        setError('Failed to load user data.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [isAdmin, router]);

  const filteredUsers = usersData.filter(user => 
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (a[sortField as keyof User] < b[sortField as keyof User]) return sortOrder === 'asc' ? -1 : 1;
    if (a[sortField as keyof User] > b[sortField as keyof User]) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = sortedUsers.slice(indexOfFirstUser, indexOfLastUser);
  const totalPages = Math.ceil(sortedUsers.length / usersPerPage);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h1 className="text-2xl font-semibold text-gray-800">User Management</h1>
            
            <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
              <input
                type="text"
                className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Search users..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
              />
              <select
                className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                value={usersPerPage}
                onChange={(e) => {
                  setUsersPerPage(Number(e.target.value));
                  setCurrentPage(1);
                }}
              >
                {[5, 10, 15, 20].map(num => (
                  <option key={num} value={num}>{num} per page</option>
                ))}
              </select>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            {loading ? (
              <div className="p-8 text-center text-gray-500">Loading users...</div>
            ) : error ? (
              <div className="p-8 text-center text-red-500">{error}</div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                          onClick={() => {
                            setSortField('username');
                            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
                          }}
                        >
                          <div className="flex items-center">
                            User
                            {sortField === 'username' && (
                              <span className="ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                            )}
                          </div>
                        </th>
                        <th
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                          onClick={() => {
                            setSortField('assigned_nodes');
                            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
                          }}
                        >
                          <div className="flex items-center">
                            Nodes
                            {sortField === 'assigned_nodes' && (
                              <span className="ml-1">{sortOrder === 'asc' ? '↑' : '↓'}</span>
                            )}
                          </div>
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {currentUsers.length > 0 ? (
                        currentUsers.map((user) => (
                          <tr key={user.user_id} className="hover:bg-gray-50">
                            <td className="px-6 py-4">
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-10 w-10">
                                  <img
                                    className="h-10 w-10 rounded-full"
                                    src={user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.username)}&background=6366f1&color=fff`}
                                    alt={user.username}
                                  />
                                </div>
                                <div className="ml-4">
                                  <div className="text-sm font-medium text-gray-900">{user.username}</div>
                                  <div className="text-sm text-gray-500">{user.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-900">
                              {user.assigned_nodes}
                            </td>
                            <td className="px-6 py-4">
                              <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                user.status === 'active'
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-gray-100 text-gray-800'
                              }`}>
                                {user.status.charAt(0).toUpperCase() + user.status.slice(1)}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm font-medium space-x-2">
                              <button className="text-indigo-600 hover:text-indigo-900">
                                Edit
                              </button>
                              <button className="text-red-600 hover:text-red-900">
                                {user.status === 'active' ? 'Suspend' : 'Activate'}
                              </button>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={4} className="px-6 py-4 text-center text-sm text-gray-500">
                            No users found
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>

                {totalPages > 1 && (
                  <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                      Showing <span className="font-medium">{indexOfFirstUser + 1}</span> to{' '}
                      <span className="font-medium">
                        {Math.min(indexOfLastUser, sortedUsers.length)}
                      </span>{' '}
                      of <span className="font-medium">{sortedUsers.length}</span> users
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => paginate(currentPage - 1)}
                        disabled={currentPage === 1}
                        className={`px-3 py-1 rounded-md ${currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                      >
                        Previous
                      </button>
                      <button
                        onClick={() => paginate(currentPage + 1)}
                        disabled={currentPage >= totalPages}
                        className={`px-3 py-1 rounded-md ${currentPage >= totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}