import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  :root {
    --white: #fff;
    --gray-dark: #343a40;
    --primary: #AE30FF;
    --secondary: #6800E7;
    --success: #AE30FF;
    --info: #29255B;
    --warning: #05B9EC;
    --danger: #FD90A4;
    --light: #FFFFFF;
    --dark: #100E23;
    --tertiary: #05B9EC;
    --assembly: #02FAE0;
    --plattform: #6800E7;
    --plattform-dark: #29255B;
    --assembly-dark: #018577;
  }

  *, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background: var(--dark);
    font-family: sans-serif;
  }

  ::selection {
      color: #fff;
      background: #ae30ff;
  }

  * {
    scrollbar-width: thin;
    scrollbar-color: #6800e7 #29255b;
  }

  *::-webkit-scrollbar {
    width: 0.75rem;
  }

  *::-webkit-scrollbar-track {
    background: #29255b;
  }

  *::-webkit-scrollbar-thumb {
    background-color: #6800e7;
  }
`;
