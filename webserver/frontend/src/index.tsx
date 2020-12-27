import ReactDOM from 'react-dom';

import demoGame from '../demo.json';

import App from './App';
import { GameReplay } from './api-types';

ReactDOM.render(
  <App replay={demoGame as GameReplay} />,
  document.getElementById('app')
);
