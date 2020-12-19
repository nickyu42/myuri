const path = require('path');
const BundleTracker = require('webpack4-bundle-tracker');

const outputDir = path.join('..', 'app', 'assets', 'dist');

module.exports = {
  mode: "production",
  entry: {
    index: path.resolve(__dirname, './src/index.ts')
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: '[name].js',
    publicPath: '/static/',  // necessary for webpack loader
    path: path.resolve(__dirname, outputDir),
  },
  plugins: [
    new BundleTracker({filename: path.join(outputDir, 'webpack-stats.json')})
  ]
};