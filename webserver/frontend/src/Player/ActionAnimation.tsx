import { useEffect } from 'react';
import styled from 'styled-components';

import { ActionResult, Entity, GameState } from '../api-types';
import { fieldSize } from '../constants';

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
  opacity: 0;
`;

const Impact = styled.div<{ $pos: Pos; radius: number }>`
  position: absolute;
  width: ${(props) => props.radius * fieldSize * 2}px;
  height: ${(props) => props.radius * fieldSize * 2}px;
  background: #b239ff;
  border-radius: 50%;
  margin-left: ${(props) => fieldSize / 2 - props.radius * fieldSize}px;
  margin-top: ${(props) => fieldSize / 2 - props.radius * fieldSize}px;
  top: ${(props) => props.$pos.y * fieldSize}px;
  left: ${(props) => props.$pos.x * fieldSize}px;
  opacity: 0;
`;

function NoOpAnimation({ delay = 0, onFinished }: { delay?: number, onFinished?: () => void;}) {
  useEffect(() => {
    onFinished && setTimeout(onFinished, delay);
  }, []);
  return null;
}

export default function ActionAnimation({
  actionResult,
  gameState,
  onFinished,
  speed = 1,
}: {
  actionResult: ActionResult;
  gameState: GameState;
  onFinished?: () => void;
  speed?: number;
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
      <>
        <SnowBall
          ref={(ref) => {
            const animation = ref?.animate(
              [
                {
                  top: `${fromPos.y * fieldSize}px`,
                  left: `${fromPos.x * fieldSize}px`,
                  opacity: '1',
                },
                {
                  top: `${toPos.y * fieldSize}px`,
                  left: `${toPos.x * fieldSize}px`,
                  offset: 0.66,
                },
                {
                  top: `${toPos.y * fieldSize}px`,
                  left: `${toPos.x * fieldSize}px`,
                  opacity: '1',
                },
                {
                  opacity: '0',
                },
              ],
              { duration: 1200 / speed }
            );

            if (animation && onFinished) {
              animation.onfinish = onFinished;
            }
          }}
          $pos={toPos}
        />
        <Impact
          ref={(ref) =>
            ref?.animate(
              [
                {
                  transform: 'scale(0.1)',
                  opacity: '0',
                },
                {
                  transform: 'scale(1.0)',
                  opacity: '0.5',
                },
                {
                  transform: 'scale(1.0)',
                  opacity: '0',
                },
              ],
              { duration: 400 / speed, delay: 800 / speed }
            )
          }
          radius={6.5}
          $pos={toPos}
        />
      </>
    );
  }

  let delay = 0;

  switch (action.name) {
    case 'WALK':
      delay = 600;
      break;
  }

  return <NoOpAnimation delay={delay} onFinished={onFinished}/>;
}
