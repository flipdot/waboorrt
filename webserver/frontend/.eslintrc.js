const noUnusedVarsConfig = {
  // ignore unused variables starting with _
  varsIgnorePattern: '^_',
  // ignore unused arguments starting with _
  argsIgnorePattern: '^_',
};

module.exports = {
  // General settings
  root: true,
  settings: {
    react: {
      version: 'detect', // Tells eslint-plugin-react to automatically detect the version of React to use
    },
  },

  // Use typescript parser
  parser: '@typescript-eslint/parser', // Specifies the ESLint parser
  parserOptions: {
    ecmaFeatures: {
      jsx: true, // Allows for the parsing of JSX
    },
  },
  plugins: ['@typescript-eslint'],

  // Presets
  extends: [
    // React
    'plugin:react/recommended',

    // Typescript
    'plugin:@typescript-eslint/recommended',

    // Imports
    'plugin:import/errors',
    'plugin:import/warnings',

    // Prevent conflicts with prettier
    'prettier',
    'prettier/@typescript-eslint',
  ],

  // Customized rules
  rules: {
    // Allow to mark intentionally unused variables with an underscore prefix.
    'no-unused-vars': ['warn', noUnusedVarsConfig],
    '@typescript-eslint/no-unused-vars': ['warn', noUnusedVarsConfig],

    // Do not require explicit return types
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',

    // Order imports in a nice way.
    'import/order': [
      'warn',
      {
        alphabetize: {
          order: 'asc',
        },
        'newlines-between': 'always-and-inside-groups',
      },
    ],

    // This produced false positives when importing typescript types.
    'import/named': 'off',

    // Enforce usage of arrow callbacks for consistency.
    'prefer-arrow-callback': 'warn',

    // Produces false positives with typescript.
    // Luckily the typescript compiler will report this anyway.
    'import/no-unresolved': 'off',

    // new JSX transforms do not need to import React since version 17.x
    'react/jsx-uses-react': 'off',
    'react/react-in-jsx-scope': 'off',
  },
};
