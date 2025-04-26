'use client';

import { useEffect, useState } from 'react';
import AppLayout from "../components/AppLayout";
import { fetchTransactions } from '@/lib/api/transaction';
import { Transaction } from '@/lib/api/types';



export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const data = await fetchTransactions();
        setTransactions(data);
        setError(null);
      } catch (err: any) {
        console.error('Failed to fetch transactions:', err);
        setError('Failed to load transactions.');
      } finally {
        setLoading(false);
      }
    };

    loadTransactions();
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Transactions</h1>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Points Redemption History</h2>

          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : transactions.length === 0 ? (
            <p className="text-gray-500">No transaction data available.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tokens Redeemed</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transaction ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {transactions.map((tx, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(tx.transaction_date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                          second: '2-digit',
                        })}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {tx.tokens_redeemed.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tx.transaction_id}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          tx.transaction_status === 'success'
                            ? 'bg-green-100 text-green-800'
                            : tx.transaction_status === 'pending'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                        }`}>
                          {tx.transaction_status.charAt(0).toUpperCase() + tx.transaction_status.slice(1)}
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
