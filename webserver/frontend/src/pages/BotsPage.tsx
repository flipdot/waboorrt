import React from 'react';
import { useNavigate } from 'react-router';
import styled from 'styled-components';
import useSWR from 'swr';
import { authenticatedSWRFetcher } from '../backend';
import Button from '../Button';
import Headline from '../Headline';

import { List, ListEntry } from '../List';
import PageWrapper from '../PageWrapper';

const Code = styled.code`
  background: rgba(0, 0, 0, 0.4);
  padding: 5px 10px;
`;

const Wrapper = styled.div`
  display: flex;
  margin-top: 30px;
  align-items: center;
  margin-bottom: 15px;
`;

const Left = styled(Headline)`
  margin-top: 0;
  margin-bottom: 0;
  flex: 1 1 auto;
`;

const Right = styled.div`
  flex: 0 0 auto;
`;

function HeadlineWithAction({
  children,
  action,
}: {
  children: React.ReactNode;
  action: React.ReactNode;
}) {
  return (
    <Wrapper>
      <Left>{children}</Left>
      <Right>{action}</Right>
    </Wrapper>
  );
}

type Repo = {
  id: string;
  name: string;
};

export default function BotsPage() {
  const { data: reposData } = useSWR<Repo[]>('/api/repositories/', authenticatedSWRFetcher);

  const navigate = useNavigate();

  return (
    <PageWrapper>
      <HeadlineWithAction
        action={
          <Button onClick={() => navigate('/bots/new')}>Create Bot</Button>
        }
      >
        My Bots
      </HeadlineWithAction>
      {reposData && (
        <List style={{ marginBottom: '20px' }}>
          {reposData.map((repo) => (
            <ListEntry>
              {repo.name}
              <Code>
                git clone ssh://git@{window.location.hostname}:2222/{repo.name}
              </Code>
            </ListEntry>
          ))}
        </List>
      )}
      {reposData && reposData.length == 0 && <p>No Bots.</p>}
    </PageWrapper>
  );
}
