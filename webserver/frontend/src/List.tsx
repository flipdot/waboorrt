import styled, { css } from 'styled-components';

export const ListEntry = styled.li<{ $selected?: boolean }>`
  border: 2px solid var(--plattform);
  background: linear-gradient(270deg, #100e23 0%, var(--plattform) 100%);
  padding: 0.5rem;
  color: #ffffffbb;
  align-items: center;

  display: flex;
  justify-content: space-around;

  &:not(:last-child) {
    margin-bottom: 10px;
  }

  ${(props) =>
    props.onClick &&
    css`
      cursor: pointer;
    `}

  ${(props) =>
    props.$selected &&
    css`
      border-color: #02fae0;
      background: linear-gradient(270deg, #100e23 0%, #018577 100%);
    `}

  > div {
    flex: 1 1 0%;

    text-align: center;
  }
`;

export const List = styled.ul`
  list-style: none;
  flex: 1 1 0%;
  margin: 0;
  overflow: auto;
  background: var(--dark);
`;
