import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/SideBar';
import ChatApp from './components/ChatApp';
import ChatHistory from './components/ChatHistory';


const App = () => {
  const [activeModel, setActiveModel] = useState(null); // Track the active model

  return (
    <Router>
      <div className="flex">
        <Sidebar activeModel={activeModel} setActiveModel={setActiveModel} />

        <div className="w-full">
          <Routes>
            <Route path="/" element={<ChatApp model={activeModel} />} />
            <Route path="/history" element={<ChatHistory />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
