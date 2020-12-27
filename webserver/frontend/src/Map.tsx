import React from 'react';
import styled from 'styled-components';

import Entity from './Entity';
import Floor from './Floor';
import { GameState } from './api-types';

const MapWrapper = styled.div`
  position: relative;
  border: 2px solid var(--white);
  margin: 20px;
`;

export default function Map({
  gameState,
  children,
}: {
  gameState: GameState;
  children: React.ReactNode;
}) {
  return (
    <MapWrapper>
      <Floor width={gameState.map_w} height={gameState.map_h} />
      {gameState.entities.map((entity, i) => (
        <Entity key={i} {...entity} />
      ))}
      {children}
    </MapWrapper>
  );
}
