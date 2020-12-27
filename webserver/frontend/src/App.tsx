import { useState } from 'react';

import styled from 'styled-components';

import Map from './Map';
import { ActionResult, Entity, GameReplay, GameState } from './api-types';
import { fieldSize } from './constants';
import { GlobalStyle } from './styles';

type Pos = { x: number; y: number };

const SnowBall = styled.div<{ $pos: Pos }>`
  position: absolute;
  width: 12px;
  height: 12px;
  background: green;
  border-radius: 50%;
  margin-left: ${fieldSize /2 - 6}px;
  margin-top: ${fieldSize / 2 - 6}px;
  top: ${(props) => props.$pos.y * fieldSize}px;
  left: ${(props) => props.$pos.x * fieldSize}px;
`;

function ActionAnimation({
  actionResult,
  gameState,
}: {
  actionResult: ActionResult;
  gameState: GameState;
}) {
  const action = actionResult.intended_action;

  if (action.name === 'THROW') {
    const throwingBot: Entity | undefined = gameState.entities.filter(
      (entity) => entity.name === actionResult.bot_name
    )[0];

    if (!throwingBot) {
      console.warn(
        'Failed to animate action. References bot name not found.',
        actionResult
      );
      return null;
    }

    const fromPos = {
      x: throwingBot.x,
      y: throwingBot.y,
    };

    const toPos = {
      x: action.x,
      y: action.y,
    };

    return (
      <SnowBall
        ref={(ref) =>
          ref?.animate(
            [
              {
                top: `${fromPos.y * fieldSize}px`,
                left: `${fromPos.x * fieldSize}px`,
              },
              {
                top: `${toPos.y * fieldSize}px`,
                left: `${toPos.x * fieldSize}px`,
              },
            ],
            { duration: 1000 }
          )
        }
        $pos={toPos}
      />
    );
  }

  return null;
}

export default function App({ replay }: { replay: GameReplay }) {
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const frame = replay[currentFrameIdx];

  return (
    <div>
      <input
        type="range"
        max={replay[0].game_state.max_ticks}
        min={0}
        value={currentFrameIdx}
        onChange={(e) => setCurrentFrameIdx(Number(e.currentTarget.value))}
      />

      {JSON.stringify(frame)}
      <Map gameState={frame.game_state}>
        {frame.actions.map((action, i) => (
          <ActionAnimation
            key={i}
            actionResult={action}
            gameState={frame.game_state}
          />
        ))}
      </Map>
      <GlobalStyle />
    </div>
  );
}
