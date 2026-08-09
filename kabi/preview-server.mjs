import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), 'www');
const port = Number(process.env.PORT || 8124);

function getContentType(filePath) {
  switch (path.extname(filePath).toLowerCase()) {
    case '.html': return 'text/html; charset=utf-8';
    case '.css': return 'text/css; charset=utf-8';
    case '.js': return 'text/javascript; charset=utf-8';
    case '.json': return 'application/json; charset=utf-8';
    case '.svg': return 'image/svg+xml';
    case '.mp4': return 'video/mp4';
    case '.jpg':
    case '.jpeg': return 'image/jpeg';
    case '.png': return 'image/png';
    case '.webp': return 'image/webp';
    case '.ico': return 'image/x-icon';
    case '.xml': return 'application/xml; charset=utf-8';
    case '.txt': return 'text/plain; charset=utf-8';
    default: return 'application/octet-stream';
  }
}

createServer(async (req, res) => {
  try {
    const url = new URL(req.url ?? '/', 'http://localhost');
    let reqPath = decodeURIComponent(url.pathname.replace(/^\/+/, ''));
    if (!reqPath) reqPath = 'index.html';

    let full = path.join(root, reqPath);
    let fileStat = null;

    try {
      fileStat = await stat(full);
    } catch {
      fileStat = null;
    }

    if (fileStat?.isDirectory()) {
      full = path.join(full, 'index.html');
    }

    let statusCode = 200;
    try {
      await stat(full);
    } catch {
      full = path.join(root, '404.html');
      statusCode = 404;
    }

    const bytes = await readFile(full);
    res.statusCode = statusCode;
    res.setHeader('Content-Type', getContentType(full));
    res.setHeader('Cache-Control', 'no-store, max-age=0');
    res.end(bytes);
  } catch {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end('Internal Server Error');
  }
}).listen(port, () => {
  console.log(`Kabi-Chemie preview running at http://localhost:${port}/`);
});
