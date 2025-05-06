// src/app/layout.tsx
'use client';
import './globals.css';
import { ReactNode } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider, AuthInitializer } from './context/AuthContext';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <AuthInitializer>
            {children}
            <ToastContainer position="top-right" autoClose={3000} />
          </AuthInitializer>
        </AuthProvider>
      </body>
    </html>
  );
}