import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { GlobalStyle } from './styles';
import Navbar from './Navbar';
import HomePage from './pages/HomePage';
import OAuthRedirectPage from './pages/OAuthRedirectPage';
import BotsPage from './pages/BotsPage';
import NewBotPage from './pages/CreateBotPage';
import { useEffect } from 'react';
import { authenticatedFetch, clearSession, isLoggedIn } from './backend';

function enforeceValidSession() {
  if (isLoggedIn()) {
    authenticatedFetch('/api/account/').then((res) => {
      if (res.status === 401 || res.status === 403) {
        // session is invalid -> clear and reload
        clearSession();
        window.location.assign('/');
      }
    });
  }
}

export default function App() {
  useEffect(() => {
    enforeceValidSession();
  }, []);

  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/bots" element={<BotsPage />} />
          <Route path="/bots/new" element={<NewBotPage />} />
          <Route path="/oauth/:provider" element={<OAuthRedirectPage />} />
        </Routes>
        <GlobalStyle />
      </BrowserRouter>
    </>
  );
}
