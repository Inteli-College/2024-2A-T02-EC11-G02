import React from "react";
import { Routes, Route } from "react-router-dom";

import InitialPage from "../pages/initial";
import AppPage from "../pages/app";


const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<InitialPage />} />
      <Route path="/app" element={<AppPage />} />
    </Routes>
  );
};

export default AppRoutes;
