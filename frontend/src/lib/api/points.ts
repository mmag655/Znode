// /src/lib/api/points.ts
import apiClient from './client';
import { PointsResponse, RedemeResponse } from './types';


export const getPoints = async (): Promise<PointsResponse> => {
    const response = await apiClient.get('/points/get');    
    return response.data.data;
};

export async function redeemPoints(): Promise<RedemeResponse> {

    const response = await apiClient.get('/points/redeeme');    
    return response.data.data;

}