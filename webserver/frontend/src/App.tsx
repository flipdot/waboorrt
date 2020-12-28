import { useState } from 'react';
import styled from 'styled-components';

import demoGame from '../demo.json';

import List from './List';
import Player from './Player';
import { GameReplay } from './api-types';

const Columns = styled.div`
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 0;
  padding-top: 100px;
  height: 100vh;
`;

const NavbarWrapper = styled.nav`
  height: 60px;
  position: fixed;
  background: var(--plattform-dark);
  width: 100%;
`;

const NavbarInner = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
`;

const HorizontalFormGroup = styled.form`
  display: flex;
  margin-left: auto;

  > input,
  > button {
    margin-left: 10px;
  }
`;

const LoginButton = styled.button`
  padding: 5px 20px;
  color: #fff;
  border: 0;
  background-color: var(--primary);;
  box-shadow: inset 0px 0px 15px rgba(32,29,71,.5);
  cursor: pointer;
  font-size: 1.125rem;
`;

const Input = styled.input`
  display: block;
  height: 40px;
  padding: 1rem 1rem;
  font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
    'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  font-size: 1.125rem;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  background-color: #29255b;
  background-clip: padding-box;
  border: 1px solid #ae30ff;
  border-radius: 0;
  box-shadow: inset 0px 0px 15px rgba(32, 29, 71, 0.5);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;

  ::placeholder {
    color: var(--white);
    opacity: 0.4;
  }
`;

function Navbar() {
  return (
    <NavbarWrapper>
      <NavbarInner>
        <HorizontalFormGroup method="GET" action="/auth-redirect">
          <Input placeholder="Template" type="text" name="template" />
          <Input placeholder="SSH Pub Key" type="text" name="pubkey" />
          <LoginButton>Login</LoginButton>
        </HorizontalFormGroup>
      </NavbarInner>
    </NavbarWrapper>
  );
}

export default function App() {
  const [selectedReplay, setSelectedReplay] = useState(null);

  return (
    <>
      <Navbar />
      <Columns>
        <Player replay={demoGame as GameReplay} />
        <List />
      </Columns>
    </>
  );
}
