# Xandra redesign tools

`../site` is generated from the original pages on the `main` branch.

```sh
git worktree add ~/Sites/xandrallc-site-main main     # once; override path with XANDRA_SRC
python3 -m venv .venv && .venv/bin/pip install beautifulsoup4 pillow
.venv/bin/python build.py                             # writes ../site and ../netlify.toml
```

Edit `site.css` / `site.js` for design changes, `build.py` for markup.
