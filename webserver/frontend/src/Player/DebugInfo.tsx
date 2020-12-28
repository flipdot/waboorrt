import styled from 'styled-components';

const DebugInfo = styled.textarea.attrs({ readOnly: true })`
  padding: 20px;
  border: 0;
  resize: none;
  width: 100%;
  min-height: 120px;
  flex: 1 1 0%;
  font-family: monospace;

  background: var(--dark);
  color: var(--tertiary);
  border: 2px solid var(--tertiary);
`;

export default DebugInfo;
