// File: app/admin/points/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppLayout from "@/app/components/AppLayout";
import { getAllPoints, updateUserPoints } from "@/lib/api/points";
import { useAuth } from "@/app/context/AuthContext";
import { toast } from "react-toastify";
import { usersPoints } from "@/lib/api";

export default function AdminPoints() {
  const [pointsData, setPointsData] = useState<usersPoints[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [editedPoints, setEditedPoints] = useState<number>(0);

  const [searchTerm, setSearchTerm] = useState("");
  const [sortField, setSortField] = useState<keyof usersPoints>("user_name");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [usersPerPage, setUsersPerPage] = useState<number>(5);

  const router = useRouter();
  const isAdmin = useAuth().user?.role === "admin";

  useEffect(() => {
    if (!isAdmin) {
      router.push("/");
      return;
    }

    const fetchPoints = async () => {
      try {
        const pointsList = await getAllPoints();
        console.log("Fetched points data:", pointsList);
        setPointsData(pointsList);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch users:", err);
        setError("Failed to load user data.");
      } finally {
        setLoading(false);
      }
    };

    fetchPoints();
  }, [isAdmin, router]);

  const filteredUsers = pointsData.filter((user) =>
    user.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.user_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.total_points.toString().includes(searchTerm)
  );

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (a[sortField] < b[sortField]) return sortOrder === "asc" ? -1 : 1;
    if (a[sortField] > b[sortField]) return sortOrder === "asc" ? 1 : -1;
    return 0;
  });

  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = sortedUsers.slice(indexOfFirstUser, indexOfLastUser);
  const totalPages = Math.ceil(sortedUsers.length / usersPerPage);

  const paginate = (pageNumber: number) => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  };

  const handleSort = (field: keyof usersPoints) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
    setCurrentPage(1);
  };

  const handleEditClick = (points: usersPoints) => {
    setEditingUserId(points.user_id);
    setEditedPoints(points.total_points);
  };

  const handleSaveClick = async (points: usersPoints) => {
    try {
      await updateUserPoints(points.user_id, editedPoints);
      toast.success("Points updated successfully");
      const refreshed = await getAllPoints();
      setPointsData(refreshed);
      setEditingUserId(null);
    } catch (err) {
      console.error("Failed to update points:", err);
      toast.error("Failed to update points");
    }
  };

  if (error) {
    return (
      <AppLayout>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h1 className="text-2xl font-semibold text-gray-800">Points Management</h1>

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
                <option value="5">5 per page</option>
                <option value="10">10 per page</option>
                <option value="15">15 per page</option>
                <option value="20">20 per page</option>
              </select>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            {loading ? (
              <div className="p-8 text-center text-gray-500">Loading users...</div>
            ) : (
              <>
                <div className="overflow-x-auto bg-white shadow rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort("user_name")}>
                          <div className="flex items-center">
                            User
                            {sortField === "user_name" && <span className="ml-1">{sortOrder === "asc" ? "↑" : "↓"}</span>}
                          </div>
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort("total_points")}>
                          <div className="flex items-center">
                            Points
                            {sortField === "total_points" && <span className="ml-1">{sortOrder === "asc" ? "↑" : "↓"}</span>}
                          </div>
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" onClick={() => handleSort("last_updated")}>
                          <div className="flex items-center">
                            Last Updated
                            {sortField === "last_updated" && <span className="ml-1">{sortOrder === "asc" ? "↑" : "↓"}</span>}
                          </div>
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {currentUsers.map((points) => (
                        <tr key={points.user_id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <img
                                src={`https://ui-avatars.com/api/?name=${encodeURIComponent(points.user_name)}&background=6366f1&color=fff`}
                                className="h-10 w-10 rounded-full"
                                alt={points.user_name}
                              />
                              <div className="ml-4">
                                <div className="text-sm font-medium text-gray-900">{points.user_name}</div>
                                <div className="text-sm text-gray-500">{points.user_email}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {editingUserId === points.user_id ? (
                              <input
                                type="number"
                                className="border rounded px-2 py-1 w-24"
                                value={editedPoints}
                                onChange={(e) => setEditedPoints(Number(e.target.value))}
                              />
                            ) : (
                              <span>{points.total_points}</span>
                            )}
                          </td>                         
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {points.last_updated ? new Date(points.last_updated).toLocaleString() : 'Never'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            {editingUserId === points.user_id ? (
                              <>
                                <button className="text-green-600 hover:text-green-900 mr-2" onClick={() => handleSaveClick(points)}>
                                  Save
                                </button>
                                <button className="text-gray-600 hover:text-gray-900" onClick={() => setEditingUserId(null)}>
                                  Cancel
                                </button>
                              </>
                            ) : (
                              <button className="text-indigo-600 hover:text-indigo-900" onClick={() => handleEditClick(points)}>
                                Edit
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {totalPages > 1 && (
                  <div className="px-6 py-4 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center text-sm text-gray-700 gap-2">
                    <div>
                      Showing <span className="font-medium">{indexOfFirstUser + 1}</span> to{" "}
                      <span className="font-medium">{Math.min(indexOfLastUser, sortedUsers.length)}</span> of{" "}
                      <span className="font-medium">{sortedUsers.length}</span> users
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => paginate(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="px-3 py-1 border rounded-md text-sm bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
                      >
                        Previous
                      </button>
                      <button
                        onClick={() => paginate(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        className="px-3 py-1 border rounded-md text-sm bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
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
