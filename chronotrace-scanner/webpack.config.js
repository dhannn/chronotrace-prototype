const { readFileSync, read } = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

console.log(path.resolve(__dirname, './certs/ca-cert.pem'));

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],
  devServer: {
    host: '0.0.0.0',//your ip address
    port: 80,
    allowedHosts: ['all'],
    static: {
      directory: path.join(__dirname, 'dist'),
    },
    hot: true,
    // open: true,
    // https://www.youtube.com/watch?v=Q67TZyT5Xjc
    server: {
      type: 'https',
      options: {     
        key: readFileSync(path.resolve(__dirname, './certs/server-key.pem')),
        cert: readFileSync(path.resolve(__dirname, './certs/server-cert.pem')),
        ca: readFileSync(path.resolve(__dirname, './certs/ca-cert.pem'))
      }
    }
  },
};