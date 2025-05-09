'use client';

import { useEffect, useState } from 'react';
import AppLayout from '@/app/components/AppLayout';
import { fetchAllTransactions, approveTransaction } from '@/lib/api/transaction';
import { AdminTransactionLog } from '@/lib/api/types';

export default function Transactions() {
  const [transactions, setTransactions] = useState<AdminTransactionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [error, setError] = useState<string | null>(null);
  const [selectedTransactions, setSelectedTransactions] = useState<number[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [transactionsPerPage, setTransactionsPerPage] = useState(5);
  const [sortConfig, setSortConfig] = useState<{ key: keyof AdminTransactionLog; direction: 'ascending' | 'descending' } | null>(null);

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const data = await fetchAllTransactions();
        setTransactions(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch transactions:', err);
        setError('Failed to load transactions.');
      } finally {
        setLoading(false);
      }
    };

    loadTransactions();
  }, []);

  // Calculate tokens on hold
  const tokensOnHold = transactions
    .filter(tx => tx.transaction_status === 'onhold')
    .reduce((sum, tx) => sum + tx.tokens_redeemed, 0);

  // Handle transaction selection
  const handleSelectTransaction = (transactionId: number) => {
    setSelectedTransactions(prev =>
      prev.includes(transactionId)
        ? prev.filter(id => id !== transactionId)
        : [...prev, transactionId]
    );
  };

  // Handle select all on current page
  const handleSelectAll = () => {
    const pageTransactionIds = currentTransactions.map(tx => Number(tx.transaction_id));
    if (selectedTransactions.length === pageTransactionIds.length) {
      setSelectedTransactions([]);
    } else {
      setSelectedTransactions(pageTransactionIds);
    }
  };

  // Handle approval
  const handleApprove = async () => {
    if (selectedTransactions.length === 0) return;
    
    try {
      await approveTransaction(selectedTransactions);
      // Refresh transactions after approval
      const data = await fetchAllTransactions();
      setTransactions(data);
      setSelectedTransactions([]);
    } catch (err) {
      console.error('Failed to approve transactions:', err);
      setError('Failed to approve transactions.');
    }
  };

  // Sorting
  const requestSort = (key: keyof AdminTransactionLog) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedTransactions = [...transactions];
  if (sortConfig !== null) {
    sortedTransactions.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });
  }

  // Filtering
  const filteredTransactions = sortedTransactions.filter(tx => {
    const matchesSearch = 
      tx.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tx.user_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      tx.transaction_id.toString().includes(searchTerm);
    
    const matchesStatus = 
      statusFilter === 'all' || 
      tx.transaction_status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  // Pagination
  const indexOfLastTransaction = currentPage * transactionsPerPage;
  const indexOfFirstTransaction = indexOfLastTransaction - transactionsPerPage;
  const currentTransactions = filteredTransactions.slice(indexOfFirstTransaction, indexOfLastTransaction);
  const totalPages = Math.ceil(filteredTransactions.length / transactionsPerPage);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-2xl font-semibold text-gray-800">Transactions Management</h1>
              {tokensOnHold > 0 && (
                <p className="text-sm text-gray-600 mt-1">
                  Total tokens on hold: <span className="font-medium">{tokensOnHold.toLocaleString()}</span>
                </p>
              )}
            </div>
            <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
              {selectedTransactions.length > 0 && (
                <button
                  onClick={handleApprove}
                  className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Approve Selected ({selectedTransactions.length})
                </button>
              )}
              <select
                className="px-3 py-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value);
                  setCurrentPage(1);
                }}
              >
                <option value="all">All Statuses</option>
                <option value="onhold">On Hold</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="success">Success</option>
                <option value="failed">Failed</option>
              </select>
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
                value={transactionsPerPage}
                onChange={(e) => {
                  setTransactionsPerPage(Number(e.target.value));
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
              <p>Loading...</p>
            ) : error ? (
              <p className="text-red-500">{error}</p>
            ) : transactions.length === 0 ? (
              <p className="text-gray-500">No transaction data available.</p>
            ) : (
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                User
                            </th>
                            <th
                            scope="col"
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                            onClick={() => requestSort('tokens_redeemed')}
                            >
                            <div className="flex items-center">
                            Tokens Redeemed
                            {sortConfig?.key === 'tokens_redeemed' && (
                                <span className="ml-1">
                                {sortConfig.direction === 'ascending' ? '↑' : '↓'}
                                </span>
                            )}
                            </div>
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Transaction ID
                        </th>
                        <th
                            scope="col"
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                            onClick={() => requestSort('transaction_date')}
                        >
                            <div className="flex items-center">
                            Date
                            {sortConfig?.key === 'transaction_date' && (
                                <span className="ml-1">
                                {sortConfig.direction === 'ascending' ? '↑' : '↓'}
                                </span>
                            )}
                            </div>
                        </th>
                        <th
                            scope="col"
                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                            onClick={() => requestSort('transaction_status')}
                        >
                            <div className="flex items-center">
                            Status
                            {sortConfig?.key === 'transaction_status' && (
                                <span className="ml-1">
                                {sortConfig.direction === 'ascending' ? '↑' : '↓'}
                                </span>
                            )}
                            </div>
                        </th>
                        <th scope="col" className="relative px-6 py-3">
                            <input
                            type="checkbox"
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                            checked={selectedTransactions.length === currentTransactions.length && currentTransactions.length > 0}
                            onChange={handleSelectAll}
                            />
                        </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {currentTransactions.map((tx) => (
                        <tr key={tx.transaction_id} className={selectedTransactions.includes(Number(tx.transaction_id)) ? 'bg-gray-50' : ''}>
                            
                            <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <img
                                src={`https://ui-avatars.com/api/?name=${encodeURIComponent(tx.user_name)}&background=6366f1&color=fff`}
                                className="h-10 w-10 rounded-full"
                                alt={tx.user_name}
                              />
                              <div className="ml-4">
                                <div className="text-sm font-medium text-gray-900">{tx.user_name}</div>
                                <div className="text-sm text-gray-500">{tx.user_email}</div>
                              </div>
                            </div>
                          </td>

                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {tx.tokens_redeemed.toLocaleString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tx.transaction_id}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(tx.transaction_date).toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit',
                                timeZone: 'America/New_York' 
                            })}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                tx.transaction_status === 'success' || tx.transaction_status === 'approved'
                                ? 'bg-green-100 text-green-800'
                                : tx.transaction_status === 'pending' || tx.transaction_status === 'onhold'
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-red-100 text-red-800'
                            }`}>
                                {tx.transaction_status.charAt(0).toUpperCase() + tx.transaction_status.slice(1)}
                            </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                            <input
                                type="checkbox"
                                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                checked={selectedTransactions.includes(Number(tx.transaction_id))}
                                onChange={() => handleSelectTransaction(Number(tx.transaction_id))}
                                disabled={tx.transaction_status !== 'onhold'}
                            />
                            </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
                {totalPages > 1 && (
                  <div className="px-6 py-4 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center text-sm text-gray-700 gap-2">
                    <div>
                      Showing <span className="font-medium">{indexOfFirstTransaction + 1}</span> to{" "}
                      <span className="font-medium">{Math.min(indexOfLastTransaction, filteredTransactions.length)}</span> of{" "}
                      <span className="font-medium">{filteredTransactions.length}</span> transactions
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
              </div>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}