'use client';
import { useEffect, useState } from 'react';
import AppLayout from '../components/AppLayout';
import { getWallet, updateWallet } from '@/lib/api/wallet';
import { getPoints, redeemPointsApi } from '@/lib/api/points'; // Import the API function to fetch points
import { toast } from 'react-toastify';

export default function Wallet() {
  const [walletAddress, setWalletAddress] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [totalPoints, setTotalPoints] = useState<number | null>(null); // State to store total points
  const [redeemPoints, setRedeemPoints] = useState<number>(0); // State to store points to redeem

  const fetchWallet = async () => {
    try {
      const data = await getWallet();
      if (!data || !data.wallet_address) {
        toast.info('No wallet address found. Please add one.');
        setWalletAddress('');
      } else {
        setWalletAddress(data.wallet_address);
      }
    } catch (err) {
      console.error('Failed to fetch wallet', err);
      toast.error('Error fetching wallet information.');
    } finally {
      setLoading(false);
    }
  };

  const fetchPoints = async () => {
    try {
      const data = await getPoints(); // Fetch points from the backend
      if (data && data.available_for_redemtion) {
        setTotalPoints(Number(data.available_for_redemtion)); // Convert BigInteger to number and set the total points
      } else {
        setTotalPoints(0); // Default to 0 if no data is returned
      }
    } catch (err) {
      console.error('Failed to fetch points', err);
      toast.error('Error fetching points information.');
    }
  };

  useEffect(() => {
    fetchWallet();
    fetchPoints(); // Fetch points when the component loads
  }, []);

  const handleRedeemPointsChange = (value: string) => {
    const points = Number(value);
    if (points <= (totalPoints || 0)) {
      setRedeemPoints(points);
    } else {
      toast.error('Points to redeem cannot exceed total points.');
    }
  };

  const handleRedeemPoints = async () => {
    try {
      await redeemPointsApi(redeemPoints); // Call the redeemPoints function with the points to redeem
      toast.success('Points redeemed successfully!');
      // setRedeemPoints(0); // Reset the redeem points input
      fetchPoints(); // Refresh the total points after redemption
    } catch (err) {
      console.error('Failed to redeem points', err);
      toast.error('Error redeeming points.');
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Wallet Management</h1>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Your Wallet Address</h2>
          {loading ? (
            <p>Loading...</p>
          ) : isEditing ? (
            <div className="space-y-4">
              <input
                type="text"
                value={walletAddress}
                onChange={(e) => setWalletAddress(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
                placeholder="Enter your Polygon wallet address"
              />
              <div className="flex space-x-3">
                <button
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  onClick={async () => {
                    try {
                      await updateWallet(walletAddress);
                      setIsEditing(false);
                    } catch (err) {
                      console.error('Failed to update wallet', err);
                    }
                  }}
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
                >
                  Save Changes
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Polygon (ERC-20) Address</p>
                <p className="mt-1 text-sm font-medium text-gray-900 break-all">{walletAddress}</p>
              </div>
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600"
              >
                {walletAddress ? 'Edit' : 'Add Wallet'}
              </button>
            </div>
          )}
        </div>

        {/* Token Redemption Block */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-4">Token Redemption</h2>
          <p className="text-sm text-gray-500 mb-4">Convert your points to ZVIO tokens</p>

          <div className="space-y-4">
            {/* Display Total Points */}
            <div>
              <p className="text-sm font-medium text-gray-700">Total Points: {totalPoints || 0}</p>
            </div>

            {/* Input for Points to Redeem */}
            <div>
              <label htmlFor="points" className="block text-sm font-medium text-gray-700">
                Points to Redeem
              </label>
              <input
                type="number"
                id="points"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter points amount"
                value={redeemPoints}
                onChange={(e) => handleRedeemPointsChange(e.target.value)}
              />
            </div>

            {/* Estimated Tokens */}
            <div className="bg-gray-50 p-4 rounded-md">
              <div className="flex justify-between">
                <span className="text-sm font-medium text-gray-500">Exchange Rate</span>
                <span className="text-sm font-medium text-gray-900">1 points = 1 ZVIO</span>
              </div>
              <div className="mt-2 flex justify-between">
                <span className="text-sm font-medium text-gray-500">Estimated Tokens</span>
                <span className="text-sm font-medium text-gray-900">{redeemPoints || 0} ZVIO</span>
              </div>
            </div>

            <button
              disabled={!walletAddress || redeemPoints <= 0}
              title={!walletAddress ? 'Add wallet to proceed' : ''}
              onClick={handleRedeemPoints} // Use the new function here
              className={`w-full px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
                ${walletAddress && redeemPoints > 0 ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400 cursor-not-allowed'} 
                focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            >
              Redeem Tokens
            </button>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
