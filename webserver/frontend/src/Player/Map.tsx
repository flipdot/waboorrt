import React from 'react';
import styled from 'styled-components';

import { GameState } from '../api-types';

import Entity from './Entity';
import Floor from './Floor';

const MapContainer = styled.div`
  overflow: hidden;
  padding: 20px;
  margin: -20px;
`;

const MapWrapper = styled.div`
  position: relative;
  border: 2px solid var(--white);
  flex: 0 0 auto;
`;

export default function Map({
  gameState,
  children,
}: {
  gameState: GameState;
  children: React.ReactNode;
}) {
  return (
    <MapContainer>
      <MapWrapper>
        <Floor width={gameState.map_w} height={gameState.map_h} />
        {gameState.entities.map((entity, i) => (
          <Entity key={i} {...entity} />
        ))}
        {children}
      </MapWrapper>
    </MapContainer>
  );
}
