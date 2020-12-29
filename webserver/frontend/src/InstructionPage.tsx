import styled from 'styled-components';

const PageWrapper = styled.div`
  max-width: 640px;
  margin: 60px auto;
  color: var(--white);
`;

const Headline = styled.h2`
  margin-bottom: 20px;
`;

const P = styled.p`
  margin-bottom: 1em;
`;

const Pre = styled.pre`
  margin-top: 2em;
  line-height: 1.4;
  border: 2px solid var(--tertiary);
  padding: 20px;
  margin-bottom: 30px;
`;

const Code = styled.code`
  font-size: 1em;
  font-family: monospace;
`;

const LoginButton = styled.a`
  padding: 5px 20px;
  color: #fff;
  border: 0;
  background-color: var(--plattform);
  box-shadow: inset 0px 0px 15px rgba(32, 29, 71, 0.5);
  cursor: pointer;
  font-size: 1.125rem;
  text-decoration: none;
  margin-top: 20px;
`;


export default function InstructionPage({ username }: { username: string }) {
  return (
    <PageWrapper>
      <Headline>Welcome, {username}!</Headline>
      <P>
        Clone your repo. Your bot will join the game after you made your first
        commit!
      </P>

      <Pre>
        <Code>
          git clone ssh://{username}@{window.location.hostname}:2222/git/{username}.git waboorrt-bot
          <br />
          cd waboorrt-bot/ # make your changes
          <br/>
          git commit . -m &quot;Do all the things&quot;
          <br />
          git push
        </Code>
      </Pre>
      <P>
        <LoginButton href="/">Go!</LoginButton>
      </P>
    </PageWrapper>
  );
}
