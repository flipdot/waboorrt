import { CgTrophy } from 'react-icons/cg';
import styled from 'styled-components';
import useSWR from 'swr';

import { Game } from '../api-types';

const EntryWrapper = styled.li`
  border: 2px solid var(--plattform);
  background: linear-gradient(270deg, #100e23 0%, var(--plattform) 100%);
  padding: 0.5rem;
  color: var(--white);
  cursor: pointer;

  &:not(:last-child) {
    margin-bottom: 10px;
  }
`;

function Entry({ item, onClick }: { item: Game; onClick: () => void }) {
  return (
    <EntryWrapper onClick={onClick}>
      {Object.entries(item.scores).map(([name, score], i) => (
        <span key={i}>
          {i !== 0 && ' vs '}
          <span style={score > 0 ? { fontWeight: 'bold'}: {}}>{name}</span>
          {score > 0 && <><CgTrophy style={{ verticalAlign: 'middle' }} /></>}
          {' '}
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
}: {
  onItemSelect: (id: string) => void;
}) {
  const { data: gameData } = useSWR<Game[]>('/api/games');

  return (
    <ListWrapper>
      {(gameData || []).map((item) => (
        <Entry
          key={item.id}
          item={item}
          onClick={() => onItemSelect(item.id)}
        />
      ))}
    </ListWrapper>
  );
}
