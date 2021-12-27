import React, { useState } from 'react';
import styled from 'styled-components';
import useSWR from 'swr';

import InstructionPage from './InstructionPage';
import List from './List';
import Player from './Player';
import { GameReplay } from './api-types';
import { GlobalStyle } from './styles';

const Logo = styled.img`
  height: 40px;
  filter: drop-shadow(0 0 5px rgba(255,255,255,0.5));
`;

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
  height: 40px;
  color: #fff;
  border: 0;
  background-color: var(--primary);
  box-shadow: inset 0px 0px 15px rgba(32, 29, 71, 0.5);
  cursor: pointer;
  font-size: 1.125rem;

  &:hover {
    filter: brightness(120%);
  }
`;

const Input = styled.input`
  display: block;
  height: 40px;
  padding: 0 1rem;
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
  const { data: templateData = [] } = useSWR('/api/templates');

  return (
    <NavbarWrapper>
      <NavbarInner>
        <Logo alt="waboorrt" src={require("./logo.svg")}/>
        <HorizontalFormGroup method="GET" action="/api/auth/auth-redirect">
          {/* <Input as="select" placeholder="Template" name="template" required>
            {templateData.map((item: string) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))} */}
          {/* </Input>
          <Input placeholder="SSH Pub Key" type="text" name="pubkey" required /> */}
          <LoginButton>Join the game!</LoginButton>
        </HorizontalFormGroup>
      </NavbarInner>
    </NavbarWrapper>
  );
}

export default function App() {
  const [selectedReplay, setSelectedReplay] = useState<string | null>(null);
  const { data } = useSWR<GameReplay>(
    selectedReplay && `/api/games/${selectedReplay}`
  );

  const searchParams = new URLSearchParams(window.location.search);
  const loggedInUser = searchParams.get('login_success');
  if (loggedInUser) {
    return (
      <>
        <InstructionPage username={loggedInUser} />
        <GlobalStyle />
      </>
    );
  }

  return (
    <>
      <Navbar />
      <Columns>
        <Player replay={data} />
        <List
          onItemSelect={(id) => setSelectedReplay(id)}
          selectedId={selectedReplay}
        />
      </Columns>
      <GlobalStyle />
    </>
  );
}
