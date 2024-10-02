import React, { useState } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa';
import { Link, useLocation } from 'react-router-dom';

export const Sidebar = ({ activeModel, setActiveModel }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  // Check if the link is active for routing paths
  const isActive = (path) => location.pathname === path;

  // Check if the custom model is active
  const isModelActive = () => activeModel === 'custom';

  // Handle navigation click by resetting the active model
  const handleNavigationClick = () => {
    setActiveModel(null); // Reset the active model when navigating to a different page
  };



  return (
    <div className="relative">
      {/* Toggle Button */}
      <button
        onClick={toggleSidebar}
        className={`p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none z-10 fixed top-4 left-4 transition-transform duration-300 ${
          isOpen ? 'translate-x-64' : ''
        }`}
        aria-label={isOpen ? 'Close Sidebar' : 'Open Sidebar'}
      >
        {isOpen ? <FaTimes /> : <FaBars />}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-screen w-64 bg-gray-900 text-white p-6 transition-transform transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } shadow-lg`}
      >
        <h2 className="text-xl font-semibold mb-4">Menu</h2>
        <ul className="space-y-4">
          <li>
            <Link
              to="/"
              onClick={handleNavigationClick}
              className={`w-full p-2 text-left rounded-md ${
                isActive('/')  && !isModelActive() ? 'bg-blue-600' : 'hover:bg-gray-800'
              }`}
            >
              Current Chat
            </Link>
          </li>
          <li>
            <Link
              to="/"
              onClick={() => setActiveModel('custom')}
              className={`w-full p-2 text-left rounded-md ${
                isModelActive() ? 'bg-blue-600' : 'hover:bg-gray-800'
              }`}
            >
              Custom Model
            </Link>
          </li>
          <li>
            <Link
              to="/history"
              onClick={handleNavigationClick}
              className={`w-full p-2 text-left rounded-md ${
                isActive('/history') && !isModelActive() ? 'bg-blue-600' : 'hover:bg-gray-800'
              }`}
            >
              Chat History
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;