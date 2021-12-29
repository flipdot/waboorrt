import { useState } from 'react';
import styled from 'styled-components';
import useSWR from 'swr';

import Player from '../Player';
import { GameReplay } from '../api-types';
import MatchList from '../MatchList';

const Columns = styled.div`
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  padding-top: 100px;
  height: 100vh;
`;

export default function HomePage() {
  const [selectedReplay, setSelectedReplay] = useState<string | null>(null);
  const { data } = useSWR<GameReplay>(
    selectedReplay && `/api/games/${selectedReplay}`
  );

  return (
    <>
      <Columns>
        <Player replay={data} />
        <MatchList
          onItemSelect={(id) => setSelectedReplay(id)}
          selectedId={selectedReplay}
        />
      </Columns>
    </>
  );
}
