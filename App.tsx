
import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Chatbot from './components/Chatbot';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import LoginPage from './pages/LoginPage';
import DiscoverSchemes from './pages/DiscoverSchemes';
import MyApplications from './pages/MyApplications';
import ApprovedBenefits from './pages/ApprovedBenefits';
import MyDocuments from './pages/MyDocuments';
import SchemeDetails from './pages/SchemeDetails';
import VoiceAssistant from './pages/VoiceAssistant';
import LanguageSettings from './pages/LanguageSettings';
import HelpCenter from './pages/HelpCenter';
import ProfilePage from './pages/ProfilePage';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => setIsAuthenticated(true);
  const handleLogout = () => setIsAuthenticated(false);

  return (
    <LanguageProvider>
      <ThemeProvider>
        <Router>
          <Routes>
            <Route path="/" element={!isAuthenticated ? <LandingPage /> : <Navigate to="/dashboard" />} />
            <Route path="/login" element={!isAuthenticated ? <LoginPage onLogin={handleLogin} /> : <Navigate to="/dashboard" />} />
            <Route path="/register" element={<LoginPage onLogin={handleLogin} />} />
            
            {/* Authenticated Routes */}
            <Route
              path="/dashboard"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <Dashboard />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/discover"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <DiscoverSchemes />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/applications"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <MyApplications />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/approved"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <ApprovedBenefits />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/documents"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <MyDocuments />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/scheme/:id"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <SchemeDetails />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/voice"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <VoiceAssistant />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
             <Route
              path="/language"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <LanguageSettings />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/help"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <HelpCenter />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/profile"
              element={
                isAuthenticated ? (
                  <Layout onLogout={handleLogout}>
                    <ProfilePage />
                    <Chatbot />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
          </Routes>
        </Router>
      </ThemeProvider>
    </LanguageProvider>
  );
};

export default App;
