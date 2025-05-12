"use client";

import { useState, useEffect } from 'react';
import AppLayout from '@/app/components/AppLayout';
import { 
  getAllNodes,
  updateNodes,
} from '@/lib/api/nodes';
import { NodesResponse } from '@/lib/api/types';
import { toast } from 'react-toastify';

export default function AdminNodes() {
  const [nodes, setNodes] = useState<NodesResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newNodeCount, setNewNodeCount] = useState<number | ''>('');
  const [newNodeReward, setNewNodeReward] = useState<number | ''>('');
  const [newNodeStatus, setNewNodeStatus] = useState<'active' | 'inactive' | 'reserved'>('inactive');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValues, setEditValues] = useState<Omit<NodesResponse, 'node_id'>>({ 
    total_nodes: 0,
    daily_reward: 0,
    status: 'inactive',
    date_updated: ''
  });

  useEffect(() => {
    const fetchNodes = async () => {
      try {
        setLoading(true);
        const data = await getAllNodes();
        setNodes(data);
      } catch (err) {
        setError('Failed to fetch nodes');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchNodes();
  }, []);

  const handleAddNode = async () => {
    if (!newNodeCount || newNodeCount <= 0) return;
    
    try {
      setLoading(true);
      // const newNodeData = {
      //   total_nodes: Number(newNodeCount),
      //   daily_reward: Number(newNodeReward) || 0,
      //   status: newNodeStatus,
      //   date_updated: new Date().toISOString()
      // };

      // const response = await createNodes(newNodeData);

      toast.info("Nodes category already added can you modify")
      // setNodes([...nodes, response]);
      // setNewNodeCount('');
      // setNewNodeReward('');
    } catch (err) {
      setError('Failed to create node');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const changeStatus = async (nodeId: number, newStatus: 'active' | 'inactive' | 'reserved') => {
    try {
      setLoading(true);
      const nodeToUpdate = nodes.find(node => node.node_id === nodeId);
      if (!nodeToUpdate) return;

      const updatedNode = await updateNodes(nodeId, {
        ...nodeToUpdate,
        status: newStatus,
        date_updated: new Date().toISOString()
      });

      setNodes(nodes.map(node => 
        node.node_id === nodeId ? updatedNode : node
      ));
    } catch (err) {
      setError('Failed to update node status');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const startEditing = (node: NodesResponse) => {
    setEditingId(node.node_id);
    setEditValues({
      total_nodes: node.total_nodes,
      daily_reward: node.daily_reward || 0,
      status: node.status,
      date_updated: node.date_updated
    });
  };

  const saveEditing = async (nodeId: number) => {
    try {
      setLoading(true);
      const updatedNode = await updateNodes(nodeId, {
        ...editValues,
        date_updated: new Date().toISOString()
      });

      setNodes(nodes.map(node => 
        node.node_id === nodeId ? updatedNode : node
      ));
      setEditingId(null);
    } catch (err) {
      setError('Failed to update node');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const cancelEditing = () => {
    setEditingId(null);
  };

  const totalNodesCount = nodes.reduce((sum, node) => sum + node.total_nodes, 0);
  const totalActive = nodes.filter(node => node.status === 'active').length;
  const totalReserved = nodes.filter(node => node.status === 'reserved').length;
  const totalRewards = nodes.reduce(
    (sum, node) => sum + (node.status === 'active' ? (node.daily_reward || 0) : 0), 
    0
  );

  if (loading && nodes.length === 0) {
    return (
      <AppLayout>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-center items-center h-64">
            <p>Loading nodes...</p>
          </div>
        </div>
      </AppLayout>
    );
  }

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
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h1 className="text-2xl font-semibold text-gray-900">Nodes Management</h1>
            <div className="flex flex-wrap gap-2 text-sm">
              <div className="bg-gray-50 px-3 py-2 rounded">
                <span className="font-medium">Total Nodes: </span>
                <span className="font-mono">{totalNodesCount.toLocaleString()}</span>
              </div>
              <div className="bg-green-50 px-3 py-2 rounded">
                <span className="font-medium">Active: </span>
                <span className="font-mono">{totalActive}</span>
              </div>
              <div className="bg-yellow-50 px-3 py-2 rounded">
                <span className="font-medium">Reserved: </span>
                <span className="font-mono">{totalReserved}</span>
              </div>
              <div className="bg-blue-50 px-3 py-2 rounded">
                <span className="font-medium">Total Rewards: </span>
                <span className="font-mono">{totalRewards}</span>
              </div>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <h2 className="text-lg font-medium mb-3 text-gray-800">Add New Node</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nodes Count</label>
                <input
                  type="number"
                  min="1"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={newNodeCount}
                  onChange={(e) => setNewNodeCount(e.target.value ? Number(e.target.value) : '')}
                  placeholder="10000"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Daily Reward</label>
                <input
                  type="number"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={newNodeReward}
                  onChange={(e) => setNewNodeReward(e.target.value ? Number(e.target.value) : '')}
                  placeholder="50"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={newNodeStatus}
                  onChange={(e) => setNewNodeStatus(e.target.value as 'active' | 'inactive' | 'reserved')}
                >
                  <option value="inactive">Inactive</option>
                  <option value="active">Active</option>
                  <option value="reserved">Reserved</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={handleAddNode}
                  disabled={!newNodeCount || loading}
                  className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {loading ? 'Adding...' : 'Add Node'}
                </button>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nodes</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Daily Reward</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Updated</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {nodes.map((node) => (
                  <tr key={node.node_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {node.node_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {editingId === node.node_id ? (
                        <input
                          type="number"
                          min="1"
                          className="w-full px-2 py-1 border border-gray-300 rounded-md"
                          value={editValues.total_nodes}
                          onChange={(e) => setEditValues({
                            ...editValues,
                            total_nodes: Number(e.target.value)
                          })}
                        />
                      ) : (
                        node.total_nodes.toLocaleString()
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {editingId === node.node_id ? (
                        <input
                          type="number"
                          min="0"
                          className="w-full px-2 py-1 border border-gray-300 rounded-md"
                          value={editValues.daily_reward || 0}
                          onChange={(e) => setEditValues({
                            ...editValues,
                            daily_reward: Number(e.target.value)
                          })}
                        />
                      ) : (
                        node.daily_reward || 0
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {editingId === node.node_id ? (
                        <select
                          className="w-full px-2 py-1 border border-gray-300 rounded-md"
                          value={editValues.status}
                          onChange={(e) => setEditValues({
                            ...editValues,
                            status: e.target.value as 'active' | 'inactive' | 'reserved'
                          })}
                        >
                          <option value="inactive">Inactive</option>
                          <option value="active">Active</option>
                          <option value="reserved">Reserved</option>
                        </select>
                      ) : (
                        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          node.status === 'active' 
                            ? 'bg-green-100 text-green-800' 
                            : node.status === 'reserved'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {node.status.charAt(0).toUpperCase() + node.status.slice(1)}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {node.date_updated ? new Date(node.date_updated).toLocaleString('en-US', { timeZone: 'America/New_York' }) : 'Never'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      {editingId === node.node_id ? (
                        <>
                          <button 
                            onClick={() => saveEditing(node.node_id)}
                            className="text-indigo-600 hover:text-indigo-900"
                            disabled={loading}
                          >
                            {loading ? 'Saving...' : 'Save'}
                          </button>
                          <button 
                            onClick={cancelEditing}
                            className="text-gray-600 hover:text-gray-900"
                            disabled={loading}
                          >
                            Cancel
                          </button>
                        </>
                      ) : (
                        <>
                          <button 
                            onClick={() => startEditing(node)}
                            className="text-indigo-600 hover:text-indigo-900"
                            disabled={loading}
                          >
                            Edit
                          </button>
                          {node.status !== 'active' && (
                            <button
                              onClick={() => changeStatus(node.node_id, 'active')}
                              className="text-green-600 hover:text-green-900"
                              disabled={loading}
                            >
                              Activate
                            </button>
                          )}
                          {node.status !== 'reserved' && (
                            <button
                              onClick={() => changeStatus(node.node_id, 'reserved')}
                              className="text-yellow-600 hover:text-yellow-900"
                              disabled={loading}
                            >
                              Reserve
                            </button>
                          )}
                          {node.status !== 'inactive' && (
                            <button
                              onClick={() => changeStatus(node.node_id, 'inactive')}
                              className="text-gray-600 hover:text-gray-900"
                              disabled={loading}
                            >
                              Deactivate
                            </button>
                          )}
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}