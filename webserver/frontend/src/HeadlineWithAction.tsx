import styled from 'styled-components';
import Headline from './Headline';

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

export default function HeadlineWithAction({
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
