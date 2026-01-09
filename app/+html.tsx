import { ScrollViewStyleReset } from 'expo-router/html';
import { type PropsWithChildren } from 'react';

// This file is web-only and used to configure the root HTML for every
// web page during static rendering.
// The contents of this function only run in Node.js environments and
// do not have access to the DOM or browser APIs.
export default function Root({ children }: PropsWithChildren) {
  return (
    <html lang="ru">
      <head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        
        {/* Mobile Optimization Meta Tags */}
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, shrink-to-fit=no, viewport-fit=cover" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="theme-color" content="#2d6caa" />
        
        {/* PWA Meta Tags */}
        <meta name="application-name" content="Клиренс креатинина" />
        <meta name="apple-mobile-web-app-title" content="Медкальк" />

        {/* 
          Disable body scrolling on web. This makes ScrollView components work closer to how they do on native. 
          However, body scrolling is often nice to have for mobile web. If you want to enable it, remove this line.
        */}
        <ScrollViewStyleReset />

        {/* Add any additional <head> elements that you want globally available on web... */}
        <title>Клиренс креатинина - Расчет по формуле Cockcroft-Gault</title>
        <meta name="description" content="Калькулятор клиренса креатинина для оценки функции почек и коррекции доз лекарственных препаратов по формуле Cockcroft-Gault." />
      </head>
      <body>{children}</body>
    </html>
  );
}
