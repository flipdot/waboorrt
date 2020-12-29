import styled from 'styled-components';

import { Entity } from '../api-types';
import { fieldSize } from '../constants';

import robot from './robot.png';

const EntityBody = styled.div<Entity>`
  position: absolute;
  top: ${(props) => props.y * fieldSize}px;
  left: ${(props) => props.x * fieldSize}px;
  height: ${fieldSize}px;
  width: ${fieldSize}px;
  background: url(${robot});
  background-size: contain;
  transition: top 0.5s, left 0.5s;
`;

const Annotation = styled.div`
  color: var(--white);
  font-size: 0.7rem;
  position: absolute;
  left: 50%;
  margin-left: -50px;
  width: 100px;
  text-align: center;
`;

const Health = styled(Annotation)`
  bottom: 100%;
  margin-bottom: 2px;
`;

const Name = styled(Annotation)`
  top: 100%;
  margin-top: 2px;
  opacity: 0.5;
`;

export default function Entity(props: Entity) {
  return (
    <>
      <EntityBody {...props}>
        <Health>{props.health}</Health>
        <Name>{props.name}</Name>
      </EntityBody>
    </>
  );
}
