// src/app/layout.tsx
import './globals.css'
import { ReactNode } from 'react'
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


import { AuthProvider } from './context/AuthContext'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
          <ToastContainer position="top-right" autoClose={3000} />
        </AuthProvider>
      </body>
    </html>
  )
}
