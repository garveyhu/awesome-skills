module.exports = {
  '*.{js,jsx,ts,tsx}': ['eslint --fix', 'prettier --write'],
  '*.{css,scss,less,html}': ['stylelint --fix --allow-empty-input', 'prettier --write'],
  '*.vue': ['eslint --fix', 'prettier --write', 'stylelint --fix'],
  '*.md': ['prettier --write'],
  'package.json': ['prettier --write'],
  '**/*': ['ls-lint'],
};
