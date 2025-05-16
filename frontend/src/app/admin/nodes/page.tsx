"use client";

import { useState, useEffect } from 'react';
import AppLayout from '@/app/components/AppLayout';
import { 
  getAllNodes,
  updateNodes,
} from '@/lib/api/nodes';
import { NodesResponse } from '@/lib/api/types';
import { toast } from 'react-toastify';

const MAX_TOTAL_NODES = 20000;

export default function AdminNodes() {
  const [nodes, setNodes] = useState<NodesResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newNodeCount, setNewNodeCount] = useState<number | ''>('');
  const [newNodeStatus, setNewNodeStatus] = useState<'active' | 'inactive' | 'reserved'>('inactive');
  const [dailyReward, setDailyReward] = useState<number>(0);
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
        
        // Set daily reward from active nodes (assuming all active nodes have same reward)
        const activeNode = data.find(node => node.status === 'active');
        if (activeNode) {
          setDailyReward(activeNode.daily_reward || 0);
        }
        
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
      toast.info("Nodes category already added can you modify");
    } catch (err) {
      setError('Failed to create node');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const startEditing = (node: NodesResponse) => {
    // Only allow editing if node is reserved
    if (node.status === 'reserved') {
      setEditingId(node.node_id);
      setEditValues({
        total_nodes: node.total_nodes,
        daily_reward: node.daily_reward || 0,
        status: node.status,
        date_updated: node.date_updated
      });
    }
  };

  const handleReservedNodesChange = (newValue: number) => {
    const reservedNode = nodes.find(node => node.status === 'reserved');
    const inactiveNode = nodes.find(node => node.status === 'inactive');
    
    if (!reservedNode || !inactiveNode) return;

    // Calculate the difference from current reserved nodes
    // const difference = newValue - reservedNode.total_nodes;
    
    // Calculate new inactive count
    // const newInactiveCount = inactiveNode.total_nodes - difference;
    
    // Check if total would exceed MAX_TOTAL_NODES
    // const activeNode = nodes.find(node => node.status === 'active');
    // const activeCount = activeNode ? activeNode.total_nodes : 0;
    // const newTotal = activeCount + newValue + inactiveNode.total_nodes;
    
    // if (newTotal > MAX_TOTAL_NODES) {
    //   toast.error(`Total nodes cannot exceed ${MAX_TOTAL_NODES}`);
    //   return;
    // }

    setEditValues(prev => ({
      ...prev,
      total_nodes: newValue
    }));

    // Update the inactive nodes count in the UI (will be saved when user clicks save)
    // setNodes(nodes.map(node => 
    //   node.status === 'inactive' 
    //     ? { ...node, total_nodes: newInactiveCount } 
    //     : node
    // ));
  };

  const saveEditing = async (nodeId: number) => {
    try {
      setLoading(true);
      const nodeToUpdate = nodes.find(node => node.node_id === nodeId);
      if (!nodeToUpdate) return;

      // For reserved nodes, we need to update both reserved and inactive nodes
      if (nodeToUpdate.status === 'reserved') {
        const inactiveNode = nodes.find(node => node.status === 'inactive');
        if (!inactiveNode) return;

        // First update the reserved node
        const updatedReservedNode = await updateNodes(nodeId, {
          ...editValues,
          date_updated: new Date().toISOString()
        });

        // Then update the inactive node
        const difference = editValues.total_nodes - nodeToUpdate.total_nodes;
        const updatedInactiveNode = await updateNodes(inactiveNode.node_id, {
          ...inactiveNode,
          total_nodes: inactiveNode.total_nodes - difference,
          date_updated: new Date().toISOString()
        });

        setNodes(nodes.map(node => {
          if (node.node_id === nodeId) return updatedReservedNode;
          if (node.node_id === inactiveNode.node_id) return updatedInactiveNode;
          return node;
        }));
      } else if (nodeToUpdate.status === 'active') {
        // For active nodes, update the global daily reward
        const updatedNode = await updateNodes(nodeId, {
          ...nodeToUpdate,
          daily_reward: dailyReward,
          date_updated: new Date().toISOString()
        });

        setNodes(nodes.map(node => 
          node.node_id === nodeId ? updatedNode : node
        ));
      }
      
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

  // Sort nodes: active first, then reserved, then inactive
  const sortedNodes = [...nodes].sort((a, b) => {
    const order = { active: 1, reserved: 2, inactive: 3 };
    return order[a.status] - order[b.status];
  });

  const totalNodesCount = nodes.reduce((sum, node) => sum + node.total_nodes, 0);
  const totalActive = nodes.filter(node => node.status === 'active').reduce((sum, node) => sum + node.total_nodes, 0);
  const totalReserved = nodes.filter(node => node.status === 'reserved').reduce((sum, node) => sum + node.total_nodes, 0);
  const totalInactive = nodes.filter(node => node.status === 'inactive').reduce((sum, node) => sum + node.total_nodes, 0);
  const activeNode = nodes.find(node => node.status === 'active');
  const activeReward = activeNode ? activeNode.daily_reward || 0 : 0;
  const totalRewards = activeReward;

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
                <span className="font-mono">{totalActive.toLocaleString()}</span>
              </div>
              <div className="bg-yellow-50 px-3 py-2 rounded">
                <span className="font-medium">Reserved: </span>
                <span className="font-mono">{totalReserved.toLocaleString()}</span>
              </div>
              <div className="bg-blue-50 px-3 py-2 rounded">
                <span className="font-medium">Inactive: </span>
                <span className="font-mono">{totalInactive.toLocaleString()}</span>
              </div>
              <div className="bg-purple-50 px-3 py-2 rounded">
                <span className="font-medium">Total Rewards: </span>
                <span className="font-mono">{totalRewards.toLocaleString()}</span>
              </div>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <h2 className="text-lg font-medium mb-3 text-gray-800">Total Rewards Settings</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Total Reward on All Active Nodes</label>
                <input
                  type="number"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={dailyReward}
                  onChange={(e) => setDailyReward(Number(e.target.value))}
                  placeholder="50"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={() => {
                    const activeNode = nodes.find(node => node.status === 'active');
                    if (activeNode) {
                      saveEditing(activeNode.node_id);
                    }
                  }}
                  disabled={loading}
                  className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {loading ? 'Saving...' : 'Update Reward'}
                </button>
              </div>
            </div>
          </div>

          {/* <div className="bg-white p-4 rounded-lg border border-gray-200">
            <h2 className="text-lg font-medium mb-3 text-gray-800">Add New Node</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
          </div> */}

          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nodes</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Updated</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sortedNodes.map((node) => (
                  <tr key={node.node_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {node.node_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {editingId === node.node_id && node.status === 'reserved' ? (
                        <input
                          type="number"
                          min="1"
                          className="w-full px-2 py-1 border border-gray-300 rounded-md"
                          value={editValues.total_nodes}
                          onChange={(e) => handleReservedNodesChange(Number(e.target.value))}
                        />
                      ) : (
                        node.total_nodes.toLocaleString()
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        node.status === 'active' 
                          ? 'bg-green-100 text-green-800' 
                          : node.status === 'reserved'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {node.status.charAt(0).toUpperCase() + node.status.slice(1)}
                      </span>
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
                        node.status === 'reserved' && (
                          <button 
                            onClick={() => startEditing(node)}
                            className="text-indigo-600 hover:text-indigo-900"
                            disabled={loading}
                          >
                            Edit
                          </button>
                        )
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