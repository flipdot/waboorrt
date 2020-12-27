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
  transition: top .4s, left .4s;
`;

export default function Entity(props: Entity) {
  return (
    <>
      <EntityBody {...props}>{props.health}</EntityBody>
    </>
  );
}
