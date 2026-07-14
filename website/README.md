# EgoWrist-Gesture30 website

This directory contains the Jekyll source for the EgoWrist-Gesture30 GitHub Pages website.

## Local preview

```bash
cd website
bundle install
bundle exec jekyll serve
```

The site is available at `http://127.0.0.1:4000/EgoWrist-Gesture30/`. GitHub Actions builds this directory and publishes the generated `_site/` output to GitHub Pages.

To preview locally at the domain root instead, run:

```bash
bundle exec jekyll serve --baseurl ""
```
