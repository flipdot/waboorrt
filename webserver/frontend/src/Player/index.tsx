import { useCallback, useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import { CgUndo, CgPlayButton, CgPlayPause } from 'react-icons/cg';

import { GameReplay } from '../api-types';
import { GlobalStyle } from '../styles';

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
  line-height: 30px;
  height: 30px;
  width: 30px;
  cursor: pointer;
`;

export default function Player({ replay }: { replay: GameReplay }) {
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const [play, setPlay] = useState(true);
  const currentFrameIdxRef = useRef(currentFrameIdx);

  const frame = replay[currentFrameIdx];

  const unfinishedActions = useRef<number[]>([]);

  const frameAnimatonsFinished = useCallback(
    (frameIdx: number) => {
      if (frameIdx === currentFrameIdxRef.current) {
        console.log('Animations finished!', frameIdx);

        if (play) {
          if (currentFrameIdx === replay[0].game_state.max_ticks) {
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
    unfinishedActions.current = new Array(frame.actions.length)
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
        <IconButton
          type="button"
          onClick={() => {
            setPlay(!play);
            const newIdx = currentFrameIdx + 1;
            setCurrentFrameIdx(newIdx);
            currentFrameIdxRef.current = newIdx;
          }}
          title={play ? 'Pause' : 'Play'}
        >
          {play ? <CgPlayPause /> : <CgPlayButton />}
        </IconButton>
        <Range
          max={replay[0].game_state.max_ticks}
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
      <GlobalStyle />
    </Wrapper>
  );
}
