"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AppLayout from '@/app/components/AppLayout';
import { getAllUsers, suspendUser, updateUserProfile } from '@/lib/api';
import { bulkCreateUsers, parseUploadedFile, validateUserData } from '@/lib/utils/file_validation';
import { toast } from 'react-toastify';

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
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [editedEmail, setEditedEmail] = useState('');
  const [editedNodes, setEditedNodes] = useState(0);
  const [isAddUserModalOpen, setIsAddUserModalOpen] = useState(false);
  const [newUserName, setNewUserName] = useState('');
  const [newUserNodes, setNewUserNodes] = useState(0);
  const [newUserEmail, setNewUserEmail] = useState('');

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

  const handleEditClick = (user: User) => {
    setEditingUserId(user.user_id);
    setEditedEmail(user.email);
    setEditedNodes(user.assigned_nodes);
  };

  const handleSaveClick = async (userId: number) => {
    try {
      await updateUserProfile({
        user_id: userId,
        email: editedEmail,
        nodes: editedNodes
      });
      
      // Update local state
      setUsersData(usersData.map(user => 
        user.user_id === userId 
          ? { ...user, email: editedEmail, assigned_nodes: editedNodes } 
          : user
      ));
      
      setEditingUserId(null);
    } catch (error) {
      console.error('Failed to update user:', error);
      setError('Failed to update user.');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
  
    try {
      setLoading(true);
      setError(null);
      
      // 1. Parse the uploaded file
      const rawData = await parseUploadedFile(file);
      
      // 2. Validate the data structure
      const { validData, errors: validationErrors } = validateUserData(rawData);
      
      if (validationErrors.length > 0) {
        // Format validation errors for better display
        const formattedErrors = validationErrors.map(err => 
          `Row ${err.row}: ${err.field} error - ${err.message}`
        );
        setError(`Validation issues found:\n${formattedErrors.join('\n')}`);
        return;
      }
      
      // 3. Send valid data to API
      const result = await bulkCreateUsers(validData);
      
      // 4. Handle results
      if (result.failed.length > 0) {
        const failedDetails = result.failed.map(f => 
          `${f.data.username || 'Unknown user'}: ${f.error}`
        ).join('\n');
        
        alert(`${result.failed.length} imports failed:\n${failedDetails}`);
      }
      
      // 5. Refresh data on any success
      if (result.success.length > 0) {
        const usersList = await getAllUsers();
        setUsersData(usersList);
        
        // Show toast instead of alert for better UX
        toast.success(`Successfully imported ${result.success.length} users`, {
          position: "top-right",
          autoClose: 5000,
        });
      }
      
    } catch (err) {
      console.error('Import error:', err);
      setError(
        err instanceof Error ? err.message : 'An unexpected error occurred during import'
      );
      
      // Show error toast
      toast.error('Failed to complete import', {
        position: "top-right",
        autoClose: 5000,
      });
    } finally {
      setLoading(false);
      if (e.target) e.target.value = ''; // Reset input
    }
  };

  const handleAddUser = async () => {
    if (!newUserName || newUserNodes <= 0) {
      toast.error('Username and nodes are required.', {
        position: "top-right",
        autoClose: 5000,
      });
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const newUser = {
        username: newUserName,
        email: newUserEmail || undefined,
        assigned_nodes: newUserNodes,
        status: 'active',
      };

      const result = await bulkCreateUsers([newUser]);

      if (result.success.length > 0) {
        const usersList = await getAllUsers();
        setUsersData(usersList);
        toast.success('User added successfully!', {
          position: "top-right",
          autoClose: 5000,
        });
      }

      if (result.failed.length > 0) {
        toast.error(`Failed to add user: ${result.failed[0].error}`, {
          position: "top-right",
          autoClose: 5000,
        });
      }

      setIsAddUserModalOpen(false);
      setNewUserName('');
      setNewUserNodes(0);
      setNewUserEmail('');
    } catch (err) {
      console.error('Failed to add user:', err);
      setError('Failed to add user.');
    } finally {
      setLoading(false);
    }
  };

  // In your component
const handleSuspendUser = async (userId: number, currentStatus: 'active' | 'inactive') => {
  try {
    const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
    
    // Call the API to suspend/activate user
    await suspendUser(userId);
    
    // Update local state
    setUsersData(usersData.map(user => 
      user.user_id === userId 
        ? { ...user, status: newStatus } 
        : user
    ));
  } catch (error) {
    console.error('Failed to update user status:', error);
    setError('Failed to update user status.');
  }
};


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
              {/* Add this file input (hidden) */}
              <input
                type="file"
                id="bulk-import"
                accept=".csv,.xlsx,.xls"
                className="hidden"
                onChange={handleFileUpload}
              />
              
              {/* Add this button */}
              <button
                onClick={() => document.getElementById('bulk-import')?.click()}
                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Bulk Import
              </button>
              <button
                onClick={() => setIsAddUserModalOpen(true)}
                className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                Add User
              </button>
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

          {/* Add User Modal */}
          {isAddUserModalOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
              <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
                <h2 className="text-lg font-semibold text-gray-800 mb-4">Add New User</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Username</label>
                    <input
                      type="text"
                      className="mt-1 px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 w-full"
                      value={newUserName}
                      onChange={(e) => setNewUserName(e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Nodes</label>
                    <input
                      type="number"
                      className="mt-1 px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 w-full"
                      value={newUserNodes}
                      onChange={(e) => setNewUserNodes(Number(e.target.value))}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                      type="email"
                      className="mt-1 px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 w-full"
                      value={newUserEmail}
                      onChange={(e) => setNewUserEmail(e.target.value)}
                    />
                  </div>
                </div>
                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    onClick={() => setIsAddUserModalOpen(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleAddUser}
                    className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    Add User
                  </button>
                </div>
              </div>
            </div>
          )}

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
                                  {editingUserId === user.user_id ? (
                                    <input
                                      type="email"
                                      className="text-sm border border-gray-300 rounded px-2 py-1"
                                      value={editedEmail}
                                      onChange={(e) => setEditedEmail(e.target.value)}
                                    />
                                  ) : (
                                    <div className="text-sm text-gray-500">{user.email}</div>
                                  )}
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-900">
                              {editingUserId === user.user_id ? (
                                <input
                                  type="number"
                                  className="border border-gray-300 rounded px-2 py-1 w-16"
                                  value={editedNodes}
                                  onChange={(e) => setEditedNodes(Number(e.target.value))}
                                />
                              ) : (
                                user.assigned_nodes
                              )}
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
                              {editingUserId === user.user_id ? (
                                <>
                                  <button 
                                    className="text-green-600 hover:text-green-900"
                                    onClick={() => handleSaveClick(user.user_id)}
                                  >
                                    Save
                                  </button>
                                  <button 
                                    className="text-gray-600 hover:text-gray-900"
                                    onClick={() => setEditingUserId(null)}
                                  >
                                    Cancel
                                  </button>
                                </>
                              ) : (
                                <button 
                                  className="text-indigo-600 hover:text-indigo-900"
                                  onClick={() => handleEditClick(user)}
                                >
                                  Edit
                                </button>
                              )}
                                <button 
                              className={user.status === 'active' ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'}
                              onClick={() => handleSuspendUser(user.user_id, user.status)}
                            >
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