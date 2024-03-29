import { useEffect } from 'react';
import {
  CgChevronDoubleDown,
  CgChevronDoubleUp,
  CgTrophy,
} from 'react-icons/cg';
import styled from 'styled-components';
import useSWR from 'swr';
import {
  TransitionGroup,
  CSSTransition,
} from 'react-transition-group';

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

const StyledList = styled(List)`
  margin-left: 60px;
  padding-right: 15px;
`;

const AnimatedWrapper = styled.li`
  overflow: hidden;
  margin-bottom: 10px;

  &.enter,  &&.exit-active {
    height: 0px;
    opacity: 0;
    margin-bottom: 0;
  }

  &.exit, &&.enter-active {
    height: 38px;
    opacity: 1;
    margin-bottom: 10px;
  }

  &.enter-active, &.exit-active {
    transition: all .3s ease;
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
    <ListEntry
      onClick={onClick}
      $selected={selected}
    >
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
  const { data: gameData } = useSWR<Game[]>('/api/games', undefined, {
    refreshInterval: 5000,
  });

  useEffect(() => {
    // select first entry when data was loaded initially
    if (gameData && gameData.length > 0) {
      onItemSelect(gameData[0].id);
    }
  }, [gameData == null])

  if (!gameData) {
    return null;
  }

  return (
    <TransitionGroup component={StyledList} appear={false}>
      {gameData.map((item) => (
        <CSSTransition key={item.id} timeout={1000}>
          <AnimatedWrapper>
            <Entry
              item={item}
              onClick={() => onItemSelect(item.id)}
              selected={selectedId === item.id}
            />
          </AnimatedWrapper>
        </CSSTransition>
      ))}
    </TransitionGroup>
  );
}
