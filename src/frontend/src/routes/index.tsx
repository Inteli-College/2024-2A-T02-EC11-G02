import React from "react";
import { Routes, Route } from "react-router-dom";

import InitialPage from "../pages/initial";
import HistoryPage from "../pages/app/history";
import UploadPage from "../pages/app/upload";
import ReportsPage from "../pages/app/reports";
import NavbarComponent from "../components/Navbar";

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<InitialPage />} />

      <Route element={<NavbarComponent />}>
        <Route path="/app/history" element={<HistoryPage />} />
        <Route path="/app/upload" element={<UploadPage />} />
        <Route path="/app/reports" element={<ReportsPage />} />
      </Route>
    
    </Routes>
  );
};

export default AppRoutes;
