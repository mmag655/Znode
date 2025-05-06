export interface User {
    id: string;
    email: string;
    name: string;
    is_first_time_login: boolean;
    import_status: 'pending' | 'completed' | string;
    role: 'admin' | 'user' | string;
  }
  
  export interface ApiError {
    message: string;
    error_code?: number;
    details?: string;
  }

  export interface PointsResponse {
    total_points: BigInteger;
    available_for_redemtion: BigInteger;
    zavio_token_rewarded: BigInteger;
  };

  export interface Activity {
    id: number;
    type: 'reward' | 'redemption' | 'bonus';
    points: number;
    description: string;
    activity_timestamp: string;
    isCredit: boolean;
  }

  // /src/lib/api/types.ts

export interface RedemeResponse {
  total_redeemed_points: number;
  remaining_points: number;
  transaction_id?: string;
  timestamp?: string;
}

export interface WalletResponse {
  wallet_address: string;
  wallet_type: string;
}

export interface Transaction {
  transaction_id: string
  tokens_redeemed: number
  transaction_status: 'success' | 'pending' | 'failed';
  transaction_date: string;
}

// /src/lib/types.ts
export interface NodesResponse {
  node_id: number;
  status: 'active' | 'reserved' | 'inactive';
  total_nodes: number;
  daily_reward: number;
  date_updated: string;
}

export interface BulkUserImport {
  username: string;
  email?: string | null;
  assigned_nodes: number;
  import_status?: 'pending' | 'completed' | string;
  status?: 'active' | 'inactive' | string;
}

export interface ValidationError {
  row: number;
  field: string;
  message: string;
}

export interface ImportResult {
  success: BulkUserImport[];
  failed: {
    data: BulkUserImport;
    error: string;
  }[];
}

export interface usersPoints {
  user_id: number;
  user_name: string;
  user_email: string;
  point_id: number;
  total_points: number;
}



  