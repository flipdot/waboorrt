import styled from 'styled-components';

const EntryWrapper = styled.li`
  border: 2px solid var(--plattform);
  background: linear-gradient(270deg, #100E23 0%, var(--plattform) 100%);
  padding: .5rem;
  color: var(--white);

  &:not(:last-child) {
    margin-bottom: 10px;
  }
`;

function Entry() {
  return <EntryWrapper>Test</EntryWrapper>;
}

const ListWrapper = styled.ul`
  list-style: none;
  flex: 1 1 0%;
  margin-left: 60px;
  overflow: auto;
  background: var(--dark);
  padding-right: 15px;
`;

export default function List() {
  return (
    <ListWrapper>
      {new Array(100).fill(0).map((_) => (
        <Entry />
      ))}
    </ListWrapper>
  );
}
