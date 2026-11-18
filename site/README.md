# Site

The project's landing page. Plain HTML, CSS and JavaScript with no build step: what is in this folder is what gets served.

| File | What it is |
|---|---|
| `index.html`, `style.css`, `main.js` | The page. Colours are tokens at the top of `style.css`, with a dark set for both the system setting and the theme toggle. |
| `demo/` | The three pages shown in the browser frame, generated from the skill's own scripts by `build.py`. |
| `og.png`, `apple-touch-icon.png` | Social preview (1200×630) and home-screen icon. |
| `404.html` | Not-found page; without it Pages serves the home page for every unknown path. |
| `_headers` | Response headers for Cloudflare Pages. |

Icons are [Phosphor](https://phosphoricons.com) (MIT), inlined as a sprite at the top of `index.html`.

## Preview locally

```sh
python -m http.server 8765 --directory site
```

Then open http://127.0.0.1:8765/.

## Regenerate the demo pages

```sh
python -I site/build.py . <path to a sample topic folder>
```

The sample topic needs a `phase-1-wishes/<module>/notes.md` and session logs under `sessions/`.

## Deploy on Cloudflare Pages

Connect the repository in **Workers & Pages → Create → Pages → Connect to Git**, then:

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `site` |
| Root directory | *(leave empty)* |

Under **Settings → Builds → Build watch paths**, include only `site/*` so changes elsewhere in the repo don't redeploy the page.

To deploy from your machine instead:

```sh
npx wrangler login
npx wrangler pages project create mastery-tutor --production-branch main
npx wrangler pages deploy site --project-name mastery-tutor
```

The page is live at https://mastery-tutor.sohab.dev/. The canonical link, `og:url`, the social image URLs and `sitemap.xml` all use that address, so update them together if the domain changes. `404.html` makes unknown paths return a real 404 instead of the home page.
