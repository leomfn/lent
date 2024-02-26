'use strict'

const path = require('path');
const autoprefixer = require('autoprefixer')
const miniCssExtractPlugin = require('mini-css-extract-plugin')


module.exports = {
  entry: './assets/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new miniCssExtractPlugin()
  ],
  module: {
    rules: [
      // {
      //   mimetype: 'image/svg+xml',
      //   scheme: 'data',
      //   type: 'asset/resource',
      //   generator: {
      //     filename: 'icons/[hash].svg'
      //   }
      // },
      {
        test: /\.scss$/i,
        use: [
          {
            // Adds CSS to the DOM by injecting a `<style>` tag
            loader: 'style-loader'
          },
          {
            // Extracts CSS for each JS file that includes CSS
            loader: miniCssExtractPlugin.loader
          },

          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: 'css-loader'
          },
          {
            // Loader for webpack to process CSS with PostCSS
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  autoprefixer
                ]
              }
            }
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: 'sass-loader'
          }
        ],
      },
    ],
  },
};
