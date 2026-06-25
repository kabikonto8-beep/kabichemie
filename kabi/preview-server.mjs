import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(fileURLToPath(new URL(".", import.meta.url)), "www");
const port = 8124;

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
};

function resolvePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0]);
  const clean = normalize(decoded).replace(/^(\.\.[/\\])+/, "");
  let target = join(root, clean);

  if (existsSync(target) && statSync(target).isDirectory()) {
    target = join(target, "index.html");
  }

  if (!existsSync(target)) {
    target = join(root, "404.html");
  }

  return target;
}

createServer((req, res) => {
  const file = resolvePath(req.url || "/");
  const ext = extname(file).toLowerCase();

  res.writeHead(file.endsWith("404.html") ? 404 : 200, {
    "Content-Type": types[ext] || "application/octet-stream",
    "Cache-Control": "no-store, max-age=0",
  });

  createReadStream(file).pipe(res);
}).listen(port, () => {
  console.log(`Preview running at http://localhost:${port}/`);
});
