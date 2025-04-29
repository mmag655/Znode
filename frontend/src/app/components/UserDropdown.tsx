'use client';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function UserDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth(); // Get user and logout

  if (!user) return null; // Hide dropdown if user is not logged in

  // Extract user details
  const email = user?.email;

  // Generate initials from name or email
  const getInitials = () => {
    if (user.name) {
      const nameParts = user.name.split(' ');
      return nameParts.map(n => n[0].toUpperCase()).slice(0, 2).join('');
    } else if (email) {
      return email.slice(0, 2).toUpperCase();
    }
    return 'U';
  };

  const handleLogout = async () => {
    await logout();
    setIsOpen(false);
  };

  return (
    <div className="relative ml-3">
      <div>
        <button
          type="button"
          className="flex items-center justify-center h-8 w-8 rounded-full bg-indigo-600 text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          onClick={() => setIsOpen(!isOpen)}
        >
          <span className="sr-only">Open user menu</span>
          {getInitials()}
        </button>
      </div>

      {isOpen && (
        <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
          <div className="px-4 py-2 border-b border-gray-100">
            <p className="text-sm font-medium text-gray-900 truncate">{email}</p>
          </div>
          {/* <Link
            href="/profile"
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Your Profile
          </Link> */}
          {/* <Link
            href="/settings"
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Settings
          </Link> */}
          <button
            onClick={handleLogout}
            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}
