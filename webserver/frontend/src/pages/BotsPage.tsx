import React, { FormEvent } from 'react';
import { useNavigate } from 'react-router';
import styled from 'styled-components';
import useSWR from 'swr';
import { authenticatedFetch, authenticatedSWRFetcher } from '../backend';
import Button from '../Button';
import { FormWrapper, Label } from '../Form';
import Headline from '../Headline';
import Input from '../Input';

import { List, ListEntry } from '../List';
import PageWrapper from '../PageWrapper';

const GitCmd = styled.code`
  background: rgba(0, 0, 0, 0.4);
  padding: 5px 10px;
`;

const RepoEntry = styled(ListEntry)`
  flex-direction: column;
  align-items: start;
`;

const RepoName = styled.div`
  font-weight: bold;
  margin-bottom: 10px;
  margin-top: 5px;
  margin-left: 5px;
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

const PublicKeyInput = styled(Input)`
  resize: none;
  height: 100px;
`;

function onSubmit(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);

  const body = {
    ssh_public_key: formData.get('pubkey'),
  };

  authenticatedFetch('/api/account/', {
    method: 'PUT',
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
    },
  }).then(() => {
    // TODO: nice feedback
    window.location.reload();
  });
}

export default function BotsPage() {
  const { data: reposData } = useSWR<Repo[]>(
    '/api/repositories/',
    authenticatedSWRFetcher
  );
  const { data: accountData } = useSWR(
    '/api/account/',
    authenticatedSWRFetcher
  );

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
            <RepoEntry>
              <RepoName>{repo.name}</RepoName>
              <GitCmd>
                git clone ssh://git@{window.location.hostname}:2222/{repo.name}
                .git
              </GitCmd>
            </RepoEntry>
          ))}
        </List>
      )}
      {reposData && reposData.length == 0 && <p>No Bots.</p>}

      <Headline>Account Settings</Headline>
      <form onSubmit={onSubmit}>
        <FormWrapper>
          <Label>SSH Public Key</Label>
          <PublicKeyInput
            value={accountData?.ssh_public_key}
            as="textarea"
            placeholder="Begins with 'ssh-rsa' or 'ssh-ed25519'"
            name="pubkey"
            required
            $fullWidth
            style={{}}
          />
        </FormWrapper>
        <Button>Update Settings</Button>
      </form>
    </PageWrapper>
  );
}
