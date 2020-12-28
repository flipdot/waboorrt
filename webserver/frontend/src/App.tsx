import { useState } from 'react';

import styled from 'styled-components';

import Map from './Map';
import { ActionResult, Entity, GameReplay, GameState } from './api-types';
import { fieldSize } from './constants';
import { GlobalStyle } from './styles';

type Pos = { x: number; y: number };

const SnowBall = styled.div<{ $pos: Pos }>`
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--white);
  border-radius: 50%;
  margin-left: ${fieldSize / 2 - 5}px;
  margin-top: ${fieldSize / 2 - 5}px;
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

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
`;

const DebugInfo = styled.textarea.attrs({ readOnly: true })`
  padding: 20px;
  margin-top: 40px;
  border: 0;
  resize: none;
  width: 640px;
  height: 240px;

  background: transparent;
  color: var(--tertiary);
  border: 2px solid var(--tertiary);
`;

export default function App({ replay }: { replay: GameReplay }) {
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const frame = replay[currentFrameIdx];

  return (
    <Wrapper>
      <input
        type="range"
        max={replay[0].game_state.max_ticks}
        min={0}
        value={currentFrameIdx}
        onChange={(e) => setCurrentFrameIdx(Number(e.currentTarget.value))}
      />

      <Map gameState={frame.game_state}>
        {frame.actions.map((action, i) => (
          <ActionAnimation
            key={i}
            actionResult={action}
            gameState={frame.game_state}
          />
        ))}
      </Map>
      <DebugInfo value={JSON.stringify(frame, null, 2)} />
      <GlobalStyle />
    </Wrapper>
  );
}
