$root = Join-Path $PSScriptRoot 'www'
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add('http://localhost:8124/')
$listener.Start()

function Get-ContentType([string]$path) {
  switch ([IO.Path]::GetExtension($path).ToLowerInvariant()) {
    '.html' { 'text/html; charset=utf-8' }
    '.css' { 'text/css; charset=utf-8' }
    '.js' { 'text/javascript; charset=utf-8' }
    '.json' { 'application/json; charset=utf-8' }
    '.svg' { 'image/svg+xml' }
    '.mp4' { 'video/mp4' }
    '.jpg' { 'image/jpeg' }
    '.jpeg' { 'image/jpeg' }
    '.png' { 'image/png' }
    '.ico' { 'image/x-icon' }
    '.xml' { 'application/xml; charset=utf-8' }
    '.txt' { 'text/plain; charset=utf-8' }
    default { 'application/octet-stream' }
  }
}

while ($listener.IsListening) {
  try {
    $ctx = $listener.GetContext()
    $reqPath = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath.TrimStart('/'))
    if ([string]::IsNullOrWhiteSpace($reqPath)) { $reqPath = 'index.html' }

    $full = Join-Path $root $reqPath
    if (Test-Path $full -PathType Container) {
      $full = Join-Path $full 'index.html'
    }
    if (!(Test-Path $full)) {
      $full = Join-Path $root '404.html'
      $ctx.Response.StatusCode = 404
    } else {
      $ctx.Response.StatusCode = 200
    }

    $bytes = [IO.File]::ReadAllBytes($full)
    $ctx.Response.ContentType = Get-ContentType $full
    $ctx.Response.Headers['Cache-Control'] = 'no-store, max-age=0'
    $ctx.Response.ContentLength64 = $bytes.Length
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    $ctx.Response.OutputStream.Close()
  } catch {
  }
}
