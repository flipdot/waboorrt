import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { GlobalStyle } from './styles';
import Navbar from './Navbar';
import HomePage from './pages/HomePage';
import OAuthRedirectPage from './pages/OAuthRedirectPage';
import BotsPage from './pages/BotsPage';
import NewBotPage from './pages/CreateBotPage';

export default function App() {
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
