variable "files_types_default" {
  type    = string
  default = "application/octet-stream"
}
variable "files_types" {
  type = map(string)
  default = {
    ".3g2"    = "video/3gpp2"
    ".3gp"    = "video/3gpp"
    ".atom"   = "application/atom+xml"
    ".css"    = "text/css; charset=utf-8"
    ".eot"    = "application/vnd.ms-fontobject"
    ".gif"    = "image/gif"
    ".ico"    = "image/vnd.microsoft.icon"
    ".jpeg"   = "image/jpeg"
    ".jpg"    = "image/jpeg"
    ".js"     = "application/javascript"
    ".htm"    = "text/html; charset=utf-8"
    ".html"   = "text/html; charset=utf-8"
    ".jar"    = "application/java-archive"
    ".json"   = "application/json"
    ".jsonld" = "application/ld+json"
    ".otf"    = "font/otf"
    ".pdf"    = "application/pdf"
    ".png"    = "image/png"
    ".rss"    = "application/rss+xml"
    ".svg"    = "image/svg"
    ".swf"    = "application/x-shockwave-flash"
    ".ttf"    = "font/ttf"
    ".txt"    = "text/plain; charset=utf-8"
    ".weba"   = "audio/webm"
    ".webm"   = "video/webm"
    ".webp"   = "image/webp"
    ".woff"   = "font/woff"
    ".woff2"  = "font/woff2"
    ".xhtml"  = "application/xhtml+xml"
    ".xml"    = "application/xml"
  }
}
