import styled, { css } from 'styled-components';

const Input = styled.input<{ $fullWidth?: boolean }>`
  display: block;
  height: 40px;
  padding: 0.5rem 1rem;
  font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
    'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  font-size: 1.125rem;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  background-color: #29255b;
  background-clip: padding-box;
  border: 1px solid #ae30ff;
  border-radius: 0;
  box-shadow: inset 0px 0px 15px rgba(32, 29, 71, 0.5);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;

  ${(props) =>
    props.$fullWidth &&
    css`
      width: 100%;
    `}

  ::placeholder {
    color: var(--white);
    opacity: 0.4;
  }
`;

export default Input;
