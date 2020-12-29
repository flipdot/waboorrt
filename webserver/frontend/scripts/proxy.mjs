import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

app.use(
  '/api',
  createProxyMiddleware({
    target: 'https://waboorrt.flipdot.org',
    changeOrigin: true,
  })
);

app.use(
  '/',
  createProxyMiddleware({
    target: 'http://localhost:1234',
    changeOrigin: true,
  })
);
app.listen(3000);
