import { useCallback, useEffect, useRef, useState } from 'react';
import { CgUndo, CgPlayButton, CgPlayPause } from 'react-icons/cg';
import styled from 'styled-components';

import { GameReplay } from '../api-types';

import ActionAnimation from './ActionAnimation';
import DebugInfo from './DebugInfo';
import Map from './Map';
import Range from './Range';

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
`;

const PlayBar = styled.div`
  display: flex;
  align-items: center;
  margin: 20px 0;
  margin-bottom: 40px;
  width: 100%;
`;

const IconButton = styled.button`
  background: transparent;
  color: var(--white);
  font-size: 30px;
  padding: 0;
  margin: 0;
  border: 0;
  line-height: 20px;
  height: 40px;
  width: 40px;
  cursor: pointer;
`;

const LargeIconButton = styled(IconButton)`
  font-size: 38px;
  margin: -4px;
`;

export default function Player({ replay }: { replay?: GameReplay }) {
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const [play, setPlay] = useState(true);
  const currentFrameIdxRef = useRef(currentFrameIdx);

  const unfinishedActions = useRef<number[]>([]);

  const frame: GameReplay[number] = replay ? replay[currentFrameIdx] : {
    actions: [],
    game_state: {
      entities: [],
      map_h: 16,
      map_w: 16,
      tick: 0,
      max_ticks: 100,
    }
  };

  const tickCount = replay?.length || 100;

  useEffect(() => {
    setPlay(true);
    const newIdx = 0;
    setCurrentFrameIdx(newIdx);
    currentFrameIdxRef.current = newIdx;
  }, [replay]);

  const frameAnimatonsFinished = useCallback(
    (frameIdx: number) => {
      if (frameIdx === currentFrameIdxRef.current) {
        console.log('Animations finished!', frameIdx);

        if (play) {
          if (!replay || currentFrameIdx === (tickCount - 1)) {
            setPlay(false);
          } else {
            console.log('Going to next frame');
            setCurrentFrameIdx(frameIdx + 1);
            currentFrameIdxRef.current = frameIdx + 1;
          }
        }
      }
    },
    [currentFrameIdx, play]
  );

  useEffect(() => {
    unfinishedActions.current = new Array(frame?.actions.length || 0)
      .fill(0)
      .map((_, i) => i);

    if (unfinishedActions.current.length === 0) {
      frameAnimatonsFinished(currentFrameIdx);
    }
  }, [frame, frameAnimatonsFinished]);

  return (
    <Wrapper>
      <Map gameState={frame.game_state}>
        {frame.actions.map((action, i) => (
          <ActionAnimation
            key={`${currentFrameIdx}_${i}`}
            actionResult={action}
            gameState={frame.game_state}
            onFinished={() => {
              unfinishedActions.current = unfinishedActions.current.filter(
                (id) => id !== i
              );

              if (unfinishedActions.current.length === 0) {
                frameAnimatonsFinished(currentFrameIdx);
              }
              console.log(unfinishedActions.current);
            }}
          />
        ))}
      </Map>

      <PlayBar>
        <LargeIconButton
          type="button"
          onClick={() => {
            setPlay(!play);
            const newIdx = Math.min(currentFrameIdx + 1, tickCount - 1);
            setCurrentFrameIdx(newIdx);
            currentFrameIdxRef.current = newIdx;
          }}
          title={play ? 'Pause' : 'Play'}
        >
          {play ? <CgPlayPause /> : <CgPlayButton />}
        </LargeIconButton>
        <Range
          max={tickCount - 1}
          min={0}
          value={currentFrameIdx}
          onChange={(e) => {
            setPlay(false);
            const newIdx = Number(e.currentTarget.value);
            setCurrentFrameIdx(newIdx);
            currentFrameIdxRef.current = newIdx;
          }}
        />
        <IconButton
          type="button"
          onClick={() => {
            setPlay(true);
            const newIdx = 0;
            setCurrentFrameIdx(newIdx);
            currentFrameIdxRef.current = newIdx;
          }}
          title="Replay"
        >
          <CgUndo />
        </IconButton>
      </PlayBar>

      <DebugInfo value={JSON.stringify(frame, null, 2)} />
    </Wrapper>
  );
}
