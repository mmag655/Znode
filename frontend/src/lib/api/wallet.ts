// /src/lib/api/points.ts
import apiClient from './client';
import { WalletResponse } from './types';


export const getWallet = async (): Promise<WalletResponse> => {
    const response = await apiClient.get('/wallet/get_wallet');    
    return response.data.data;
};

export const createWallet = async (): Promise<WalletResponse> => {
    const response = await apiClient.post('/wallet/create_wallet');    
    return response.data.data;
};

export async function updateWallet(wallet_address: string): Promise<WalletResponse> {
    const response = await apiClient.put('/wallet/update_wallet', null, {
        params: { wallet_address }
    });
    return response.data.data;
}