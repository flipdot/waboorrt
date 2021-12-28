import React, { useEffect, useState } from 'react';
import useSWR from 'swr';

import { Game, GameReplay } from '../api-types';

import Player from './index';

export default function LatestGamePlayer() {
  const { data: gameData, mutate } = useSWR<Game[]>('/api/games');
  const [selectedReplay, setSelectedReplay] = useState<string | null>(null);
  const { data } = useSWR<GameReplay>(
    selectedReplay && `/api/games/${selectedReplay}`
  );

  useEffect(() => {
    if (gameData && gameData.length > 0) {
      // Todo check if the first is the latest
      setSelectedReplay(gameData[0].id);
    }
  }, [gameData]);

  return <Player replay={data} onReplayComplete={mutate} />;
}
