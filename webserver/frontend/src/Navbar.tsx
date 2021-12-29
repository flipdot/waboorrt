import { useNavigate } from 'react-router';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

import { isLoggedIn } from './backend';
import Button from './Button';

const Logo = styled.img`
  height: 40px;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
`;

const NavbarWrapper = styled.nav`
  height: 60px;
  position: fixed;
  background: #211132;
  width: 100%;
  border-bottom: 1px solid #3d1f5c;
`;

const NavbarInner = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
`;

const HorizontalFormGroup = styled.div`
  display: flex;
  margin-left: auto;

  > input,
  > button {
    margin-left: 10px;
  }
`;

export default function Navbar() {
  const navigate = useNavigate();

  return (
    <NavbarWrapper>
      <NavbarInner>
        <Link to="/">
          <Logo alt="waboorrt" src={require('./logo.svg')} />
        </Link>
        <HorizontalFormGroup>
          {isLoggedIn() ? (
            <Button onClick={() => navigate('bots')}>Manage Bots</Button>
          ) : (
            <form method="GET" action="/api/auth/auth-redirect">
              <Button>Create a Bot!</Button>
            </form>
          )}
        </HorizontalFormGroup>
      </NavbarInner>
    </NavbarWrapper>
  );
}
