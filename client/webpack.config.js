const path = require('path');
const BundleTracker = require('webpack4-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

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
      {
        test: /\.css$/,
        exclude: '/node_modules/',
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.css'],
  },
  output: {
    filename: '[name].js',
    publicPath: '/static/dist/',  // necessary for webpack loader
    path: path.resolve(__dirname, outputDir),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/[name]-[hash].css'
    }),
    new BundleTracker({filename: path.join(outputDir, 'webpack-stats.json')}),
  ]
};