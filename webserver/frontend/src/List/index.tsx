import {
  CgChevronDoubleDown,
  CgChevronDoubleUp,
  CgTrophy,
} from 'react-icons/cg';
import styled, { css } from 'styled-components';
import useSWR from 'swr';

import { Game } from '../api-types';

const EntryWrapper = styled.li<{ $selected: boolean }>`
  border: 2px solid var(--plattform);
  background: linear-gradient(270deg, #100e23 0%, var(--plattform) 100%);
  padding: 0.5rem;
  color: #ffffffbb;
  cursor: pointer;
  display: flex;
  justify-content: space-around;

  &:not(:last-child) {
    margin-bottom: 10px;
  }

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
    <EntryWrapper onClick={onClick} $selected={selected}>
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
