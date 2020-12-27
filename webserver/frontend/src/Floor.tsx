import React from 'react';
import styled from 'styled-components';

import { fieldSize } from './constants';

const FloorTile = styled.div`
  width: ${fieldSize}px;
  height: ${fieldSize}px;
  border: 1px solid;
`;

const FloorRow = styled.div`
  display: flex;
`;

function Floor({ width, height }: { width: number; height: number }) {
  return (
    <div>
      {new Array(height).fill(0).map((_, y) => (
        <FloorRow key={y}>
          {new Array(width).fill(0).map((_, x) => (
            <FloorTile key={x} />
          ))}
        </FloorRow>
      ))}
    </div>
  );
}

export default React.memo(Floor);
