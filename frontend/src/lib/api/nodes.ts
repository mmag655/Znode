// /src/lib/api/nodes.ts
import apiClient from './client';
import { NodesResponse } from './types';

export const getAllNodes = async (): Promise<NodesResponse[]> => {
  const response = await apiClient.get('/admin/nodes/all');
  return response.data.data;
};

export const updateNodes = async (node_id: number, nodeData: Omit<NodesResponse, 'node_id'>): Promise<NodesResponse> => {
  const response = await apiClient.patch(`/admin/nodes/update/${node_id}`, nodeData);
  return response.data.data;
};

export const createNodes = async (nodeData: Omit<NodesResponse, 'node_id'>): Promise<NodesResponse> => {
  const response = await apiClient.post('/admin/nodes/create', nodeData);
  return response.data.data;
};
