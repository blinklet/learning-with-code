# Copilot / AI Agent Instructions — Learning with Code

Purpose: Help an AI coding agent be immediately productive with this Pelican-powered technical blog.

**Big Picture**
- **Site Generator**: Pelican (Python static site generator). See `pelicanconf.py` and `publishconf.py`.
- **Source vs Output**: Source content lives in `content/`. Built site files live in `output/`.
- **Theme**: Theme is `themes/Flex-2.5.0` (set in `pelicanconf.py`).
- **Hosting**: The site produces a static `output/` directory suitable for static hosts (Cloudflare Pages, Netlify, etc.). Example pages in `output/` include `add-custom-domain-to-cloudflare-pages.html`.

**How to set up locally**
- **Create venv**: `python -m venv .venv`
- **Activate**: `source .venv/bin/activate`
- **Install deps**: `pip install -r requirements.txt`
- **Build**: from repo root run:
  - `pelican content -s pelicanconf.py`  
    (Pelican uses `PATH = 'content'` and `OUTPUT_PATH = 'output'` from config.)
- **Serve locally** (simple static server):
  - `python -m http.server --directory output 8000`
- **Clean build**: remove `output/` then re-run build, or use `DELETE_OUTPUT_DIRECTORY = True` in `publishconf.py` when appropriate.

**Content structure & conventions**
- **Article layout**: `content/articles/<NNN>-slug/` directories hold article markdown files and attachments (images). Filenames use numeric prefixes for ordering.
- **Front matter**: Markdown files use Pelican-style metadata at top. Common fields:
  - `title`, `slug`, `summary`, `date`, `modified`, `category`, `status`
  - `status` commonly `published` or `draft` (see `DEFAULT_METADATA` in `pelicanconf.py`)
- **Images & attachments**: images live in `content/.../` or `content/images/`. Posts use `{attach}image.png` (site already uses this pattern).
- **Static paths**: `STATIC_PATHS = ['images','extras']` — use `content/extras` for extra static files you want copied.

**Markdown & rendering**
- `pelicanconf.py` sets `MARKDOWN` extensions including `codehilite`, `extra`, `meta`, `admonition`, `toc`. Follow those conventions for code blocks and TOCs.

**Theme / UI notes**
- Theme variables and settings in `pelicanconf.py`: `SITELOGO`, `SITETITLE`, `SITESUBTITLE`, `PYGMENTS_STYLE`, `MAIN_MENU`, `MENUITEMS`.
- Keep to theme-compatible HTML/CSS in posts (the author uses small inline `<style>` snippets in some articles).

**Editing workflow**
- Edit or add markdown under `content/`.
- Rebuild with Pelican; verify output in `output/`.
- For publishing deployments, push `output/` to static host, or configure CI to run `pelican content -s pelicanconf.py` and upload `output/`.

**Project-specific patterns**
- **Numbered article folders**: used for ordering & slugging (e.g., `003-flask-web-app-tutorial/`).
- **Local references**: internal links use `{filename}/articles/...` patterns — keep relative paths intact.
- **No test suite**: repository contains no automated tests. Changes rely on local build verification.

**Files to reference when making changes**
- `pelicanconf.py` — primary build/site settings
- `publishconf.py` — publish-time overrides
- `requirements.txt` — Python dependencies
- `content/` — source markdown, images, pages
- `themes/Flex-2.5.0/` — theme templates and assets
- `output/` — generated site (useful for quick visual checks)