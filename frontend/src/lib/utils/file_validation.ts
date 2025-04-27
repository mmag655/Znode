// /src/lib/utils/file_validation.ts
// import { console } from 'inspector';
import * as XLSX from 'xlsx';
import { BulkUserImport, ImportResult, ValidationError } from '../api/types';
import { bulkCreate } from '../api';

/**
 * Parses uploaded Excel/CSV file into JSON data
 */
export const parseUploadedFile = async (file: File): Promise<any[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        if (!data) {
          throw new Error('No file data found');
        }

        const workbook = XLSX.read(data, { type: 'binary' });
        if (workbook.SheetNames.length === 0) {
          throw new Error('No sheets found in the file');
        }

        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);
        resolve(jsonData);
      } catch (err) {
        reject(new Error(`File parsing failed: ${err instanceof Error ? err.message : String(err)}`));
      }
    };

    reader.onerror = () => reject(new Error('File reading failed'));
    reader.readAsBinaryString(file);
  });
};


// Validates user import data with strict typing

export const validateUserData = (data: any[]): {
    validData: BulkUserImport[];
    errors: ValidationError[];
  } => {
    const validData: BulkUserImport[] = [];
    const errors: ValidationError[] = [];
  
    data.forEach((row, index) => {
      const rowErrors: ValidationError[] = [];
  
      // Normalize column names (handle various possible names)
      const normalizedRow = {
        email: row['user email'] || row.email || row['User Email'] || null,
        username: row['user name'] || row.username || row['User Name'] || null,
        nodes: row.nodes || row.Nodes || row['Node Count'] || null
      };
  
      // Validate username (required)
      if (!normalizedRow.username || typeof normalizedRow.username !== 'string') {
        rowErrors.push({
          row: index + 1,
          field: 'username',
          message: 'Username is required'
        });
      }
  
      // Validate nodes (required, must be number)
      if (normalizedRow.nodes === undefined || normalizedRow.nodes === null) {
        rowErrors.push({
          row: index + 1,
          field: 'nodes',
          message: 'Nodes assignment is required'
        });
      } else if (isNaN(Number(normalizedRow.nodes))) {
        rowErrors.push({
          row: index + 1,
          field: 'nodes',
          message: 'Nodes must be a number'
        });
      }
  
      // Validate email format if provided
      if (normalizedRow.email && typeof normalizedRow.email === 'string') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(normalizedRow.email)) {
          rowErrors.push({
            row: index + 1,
            field: 'email',
            message: 'Invalid email format'
          });
        }
      }
  
      if (rowErrors.length === 0) {
        validData.push({
          username: String(normalizedRow.username),
          email: normalizedRow.email ? String(normalizedRow.email) : null,
          assigned_nodes: Number(normalizedRow.nodes),
          import_status: 'pending',
          status: 'active'
        });
      } else {
        errors.push(...rowErrors);
      }
    });
  
    return { validData, errors };
  };
/**
 * Sends validated data to bulk create endpoint
 */
export const bulkCreateUsers = async (usersData: BulkUserImport[]): Promise<ImportResult> => {
  try {
    const response = await bulkCreate(usersData);

    if (!response || !response.data) {
      throw new Error('No data returned from the server');
    }

    return response.data as ImportResult;
  } catch (error) {
    console.error('Bulk create failed:', error);
    throw new Error(
      `Failed to create users: ${error instanceof Error ? error.message : 'Unknown error'}`
    );
  }
};

/**
 * Complete file processing pipeline
 */
export const processUserImportFile = async (file: File): Promise<{
  result?: ImportResult;
  validationErrors?: ValidationError[];
  fileError?: string;
}> => {
  try {
    // Step 1: Parse file
    const rawData = await parseUploadedFile(file);

    // Step 2: Validate data
    const { validData, errors: validationErrors } = validateUserData(rawData);

    if (validationErrors.length > 0) {
      return { validationErrors };
    }

    // Step 3: Send to API
    const result = await bulkCreateUsers(validData);
    return { result };

  } catch (error) {
    return {
      fileError: error instanceof Error ? error.message : 'Unknown file processing error'
    };
  }
};