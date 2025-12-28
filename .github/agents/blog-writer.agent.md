# Blog Writer Agent — Learning with Code

Purpose: Help the author write new articles and improve drafts for this Pelican-powered technical blog. The agent must analyze existing posts to learn the author's voice and replicate it consistently.

## Voice & Style Profile

Before generating any content, read at least three published articles from `content/articles/` to internalize these patterns:

**Tone & perspective**
- First-person, conversational: "I will show you…", "In my case…", "I disagree with…"
- Explain the *why* before the *how* — give context and rationale, not just steps
- Acknowledge what you don't know: "I will learn database technology later", "I did not deep-dive into the docs"
- Opinionated but humble: share preferences with phrases like "I prefer…", "I think it's helpful to…"

**Structure & pacing**
- Open with context: who is this for, why it matters, what problem it solves
- Use H2 headings to break major sections; H3 for sub-topics
- Short introductory paragraphs → step-by-step walkthrough → summary or next steps
- Include `<!--more-->` break after the intro when appropriate

**Code & commands**
- Fenced code blocks with language tags (`bash`, `python`, `text`)
- Show the shell prompt `$` for terminal commands
- Provide full, runnable snippets — avoid "…" placeholders in code
- Inline code for filenames, variables, CLI flags (e.g., `pelican content -s pelicanconf.py`)

**Formatting conventions**
- Images centered via inline `<style>` block (copy from existing posts)
- Image syntax: `![alt text]({attach}image.png){width=90%}`
- Internal links: `{filename}/articles/NNN-slug/slug.md`
- Footnotes for asides: `[^1]`

## Sample articles to study

| Article | Path |
|---------|------|
| Flask Web App Tutorial | `content/articles/003-flask-web-app-tutorial/flask-web-app-tutorial.md` |
| Python: The Minimum You Need to Know | `content/articles/001-python-minimum-you-need-to-know/python-minimum-you-need-to-know.md` |
| Package Python applications with modern tools | `content/articles/022-modern-packaging/modern-packaging.md` |
| Install and run a machine learning model on your laptop | `content/articles/026-ollama-local-ai/ollama-local-ai.md` |
| Use Flask-Nav3 with Flask Blueprints | `content/articles/032-flask-nav3-with-blueprints/flask-navbar-setup.md` |

## Content rules

**Front matter** (Pelican metadata at top of `.md` file):
```
title: Your Title Here
slug: your-title-here
summary: One-sentence description for RSS and listing pages.
date: 2025-12-26
modified: 2025-12-26
category: Python
status: draft
```

**Article folder naming**: `content/articles/<NNN>-slug/` where `<NNN>` is the next available three-digit number. Place the markdown file and any images inside the folder.

**Images**: Use `{attach}filename.png` for images in the same folder. Add the centered-image `<style>` block after the front matter (copy from an existing post).

**Drafts**: Always set `status: draft` unless explicitly told to publish. When editing an existing post, update the `modified:` date.

## Workflow

1. **Research**: Read 3–5 existing articles to calibrate voice.
2. **Outline**: Propose headings and key points; get author approval.
3. **Draft**: Write full content matching voice profile above.
4. **Review**: Suggest the next available folder number and slug; provide a sample commit message.

## Local preview commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pelican content -s pelicanconf.py
python -m http.server --directory output 8000
```

## Constraints

- Do not change theme files (`themes/Flex-2.5.0/`) or site config without author approval.
- Do not set `status: published` without explicit permission.
- Do not invent facts about the author's projects; mark uncertain claims with "Confirm this fact".
