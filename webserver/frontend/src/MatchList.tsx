import {
  CgChevronDoubleDown,
  CgChevronDoubleUp,
  CgTrophy,
} from 'react-icons/cg';
import styled from 'styled-components';
import useSWR from 'swr';

import { List, ListEntry } from './List';
import { Game } from './api-types';

const Trophy = styled(CgTrophy)`
  vertical-align: middle;
  color: var(--plattform);
  background: #fff;
  border-radius: 50%;
`;

const Name = styled.span`
  font-weight: bold;
  color: var(--white);
`;

const Elo = styled.span`
  font-size: 0.7em;
  opacity: 0.6;
  font-weight: normal;
`;

const Divider = styled.div`
  opacity: 0.5;

  && {
    flex: 0 0 20px;
  }
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
    <ListEntry onClick={onClick} $selected={selected}>
      {scoreEntries.map(([label, score], i) => (
        <>
          {i !== 0 && <Divider>/</Divider>}
          <div key={i}>
            <Name>{label}</Name>{' '}
            {score > 0 && (
              <>
                <Trophy />{' '}
              </>
            )}
            <Elo>
              {score > 0 ? <CgChevronDoubleUp /> : <CgChevronDoubleDown />}
              {item.elo_rank[label]}
            </Elo>
          </div>
        </>
      ))}
    </ListEntry>
  );
}

export default function MatchList({
  onItemSelect,
  selectedId,
}: {
  onItemSelect: (id: string) => void;
  selectedId: string | null;
}) {
  const { data: gameData } = useSWR<Game[]>('/api/games');

  return (
    <List>
      {(gameData || []).map((item) => (
        <Entry
          key={item.id}
          item={item}
          onClick={() => onItemSelect(item.id)}
          selected={selectedId === item.id}
        />
      ))}
    </List>
  );
}
