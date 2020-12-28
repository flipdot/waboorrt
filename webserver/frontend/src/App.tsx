import { useState } from 'react';
import styled from 'styled-components';

import demoGame from '../demo.json';

import List from './List';
import Player from './Player';
import { GameReplay } from './api-types';

const Wrapper = styled.div`
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  height: 100vh;
`;

export default function App() {
  const [selectedReplay, setSelectedReplay] = useState(null);

  return (
    <Wrapper>
      <Player replay={demoGame as GameReplay}  />
      <List />
    </Wrapper>
  );
}
