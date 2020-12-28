import { useCallback, useEffect, useRef, useState } from 'react';

import styled, { css } from 'styled-components';

import ActionAnimation from './ActionAnimation';
import Map from './Map';
import { GameReplay } from './api-types';
import { GlobalStyle } from './styles';

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

const sliderThumbCss = css`
appearance: none;
    border-radius: 0;
    margin: 0;
    height: 15px;
    width: 5px;
    border: 0;
    background: var(--white);
`;

const Range = styled.input.attrs({ "type": 'range'})`
  width: 400px;
  appearance: none;
  height: 15px;
  margin: 20px;
  background: var(--secondary);

  &::-moz-range-thumb {
    ${sliderThumbCss};
  }

  &::-webkit-slider-thumb {
    ${sliderThumbCss};
  }
`;

export default function App({ replay }: { replay: GameReplay }) {
  const [currentFrameIdx, setCurrentFrameIdx] = useState(0);
  const [play, setPlay] = useState(true);
  const currentFrameIdxRef = useRef(currentFrameIdx);

  const frame = replay[currentFrameIdx];

  const unfinishedActions = useRef<number[]>([]);

  const frameAnimatonsFinished = useCallback((frameIdx: number) => {
    if (frameIdx === currentFrameIdxRef.current) {
      console.log('Animations finished!', frameIdx);

      if (play) {
        if (currentFrameIdx === replay[0].game_state.max_ticks) {
          setPlay(false);
        } else {
          console.log("Going to next frame");
          setCurrentFrameIdx(frameIdx + 1);
          currentFrameIdxRef.current = frameIdx + 1;
        }
      }
    }
  }, [currentFrameIdx, play]);

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

      <button type="button" onClick={() => {
        setPlay(!play);
        const newIdx = currentFrameIdx + 1;
        setCurrentFrameIdx(newIdx);
        currentFrameIdxRef.current = newIdx;
      }}>
        {play ? 'Pause' : 'Play'}
      </button>

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
      <DebugInfo value={JSON.stringify(frame, null, 2)} />
      <GlobalStyle />
    </Wrapper>
  );
}
