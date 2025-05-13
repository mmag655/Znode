// /src/lib/api/points.ts
import apiClient from './client';
import { PointsResponse, RedemeResponse, usersPoints } from './types';


export const getPoints = async (): Promise<PointsResponse> => {
    const response = await apiClient.get('/points/get');    
    return response.data.data;
};

export async function redeemPointsApi(pointsToRedeeme: number): Promise<RedemeResponse> {

    const response = await apiClient.post(`/points/redeem/${pointsToRedeeme}`);    
    return response.data.data;

}

export const getAllPoints = async (): Promise<usersPoints[]> => {
    const response = await apiClient.get('/points/admin/get/all');    
    return response.data.data;
};

export const updateUserPoints = async (user_id: number, total_points: number, available_for_redemtion: number): Promise<void> => {
    const points_already_redeemed = total_points - available_for_redemtion
    const response = await apiClient.put(`/points/admin/update/${user_id}`, {
        total_points: total_points,
        available_for_redemtion: available_for_redemtion,
        zavio_token_rewarded: points_already_redeemed

    });
    return response.data.data;
};

