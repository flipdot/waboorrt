import styled from 'styled-components';

import { Entity } from './api-types';
import { fieldSize } from './constants';
import robot from './robot.png';

const EntityBody = styled.div<Entity>`
  position: absolute;
  top: ${(props) => props.y * fieldSize}px;
  left: ${(props) => props.x * fieldSize}px;
  height: ${fieldSize}px;
  width: ${fieldSize}px;
  background: url(${robot});
  background-size: contain;
  transition: top 0.4s, left 0.4s;
`;

const Health = styled.div`
  color: var(--white);
  font-size: 0.7rem;
  bottom: 100%;
  position: absolute;
  left: 50%;
  margin-left: -25px;
  margin-bottom: 2px;
  width: 50px;
  text-align: center;
`;

export default function Entity(props: Entity) {
  return (
    <>
      <EntityBody {...props}>
        <Health>{props.health}</Health>
      </EntityBody>
    </>
  );
}
