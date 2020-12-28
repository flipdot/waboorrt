import styled, { css } from 'styled-components';

const sliderThumbCss = css`
  appearance: none;
  border-radius: 0;
  margin: 0;
  height: 15px;
  width: 5px;
  border: 0;
  background: var(--white);
`;

const Range = styled.input.attrs({ type: 'range' })`
  flex: 1 1 0%;
  appearance: none;
  height: 15px;
  margin: 0 20px;
  background: var(--secondary);

  &::-moz-range-thumb {
    ${sliderThumbCss};
  }

  &::-webkit-slider-thumb {
    ${sliderThumbCss};
  }
`;

export default Range;
