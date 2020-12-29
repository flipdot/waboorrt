import { CgTrophy } from 'react-icons/cg';
import styled, { css } from 'styled-components';
import useSWR from 'swr';

import { Game } from '../api-types';

const EntryWrapper = styled.li<{ $selected: boolean }>`
  border: 2px solid var(--plattform);
  background: linear-gradient(270deg, #100e23 0%, var(--plattform) 100%);
  padding: 0.5rem;
  color: var(--white);
  cursor: pointer;

  &:not(:last-child) {
    margin-bottom: 10px;
  }

  ${(props) =>
    props.$selected &&
    css`
      border-color: #02fae0;
      background: linear-gradient(270deg, #100e23 0%, #018577 100%);
    `}
`;

function Entry({
  item,
  onClick,
  selected,
}: {
  item: Game;
  onClick: () => void;
  selected: boolean;
}) {
  const scoreEntries = Object.entries(item.scores);

  return (
    <EntryWrapper onClick={onClick} $selected={selected}>
      {scoreEntries.map(([name, score], i) => (
        <span key={i}>
          {i !== 0 && ' vs '}
          <span style={score > 0 ? { fontWeight: 'bold' } : {}}>{name}</span>
          {score > 0 && (
            <>
              <CgTrophy style={{ verticalAlign: 'middle' }} />
            </>
          )}{' '}
        </span>
      ))}
    </EntryWrapper>
  );
}

const ListWrapper = styled.ul`
  list-style: none;
  flex: 1 1 0%;
  margin-left: 60px;
  overflow: auto;
  background: var(--dark);
  padding-right: 15px;
`;

export default function List({
  onItemSelect,
  selectedId,
}: {
  onItemSelect: (id: string) => void;
  selectedId: string | null;
}) {
  const { data: gameData } = useSWR<Game[]>('/api/games');

  return (
    <ListWrapper>
      {(gameData || []).map((item) => (
        <Entry
          key={item.id}
          item={item}
          onClick={() => onItemSelect(item.id)}
          selected={selectedId === item.id}
        />
      ))}
    </ListWrapper>
  );
}
