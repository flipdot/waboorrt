import styled from "styled-components";

const Button = styled.button`
  padding: 8px 15px;
  color: #fff;
  border: 0;
  background-color: var(--primary);
  box-shadow: inset 0px 0px 15px rgba(32, 29, 71, 0.5);
  cursor: pointer;
  font-size: 1rem;

  &:hover {
    filter: brightness(120%);
  }
`;

export default Button;
