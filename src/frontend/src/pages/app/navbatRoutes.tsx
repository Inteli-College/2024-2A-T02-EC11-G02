import React from "react";
import { Routes, Route } from "react-router-dom";

import HomePage from "./home";
import HistoryPage from "./history";
import UploadPage from "./upload";
import ReportsPage from "./reports";



const NavbarRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/reports" element={<ReportsPage />} />
    </Routes>
  );
};

export default NavbarRoutes;
