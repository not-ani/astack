---
name: "create-slideshow"
description: "Build an interactive, offline HTML slideshow that steps through any subject one idea at a time, with animated diagrams, quoted sources, captions, and speaker notes. Use when asked for a slideshow, deck, walkthrough, or explainer, or when another skill hands over an outline to present."
metadata:
  version: "1.0.0"
---

# Create a slideshow

Turn material into a step-through slideshow that a reader can follow alone or present out loud. Each slide carries one idea, and each step adds one piece of it, so the reader never has to take in a whole diagram at once.

The subject can be anything: a process, a system, a policy, a historical event, a product, a paper, a codebase. This skill owns how the slideshow looks and behaves. What it says comes from the caller, either the user or another skill that has already done the research.

## Ground rules

- Every factual claim on a slide comes from the material. Mark anything illustrative or simplified as such.
- Quote sources directly in excerpt panels and caption each one with where it came from: a document and section, a page, a URL, a file and line. Mark omissions.
- Keep source material read-only. Write the slideshow in its own folder.
- One idea per slide and one new piece per step. If a caption needs "and also", split the step.
- Define a term the first time it appears. Match the depth to the reader.

## Step 1: Scope

Settle three things before building: who the reader is, what they should be able to say or do after the last slide, and roughly how long the deck should be. Take them from the request or from the calling skill's handoff. Ask once if something missing would change the deck.

If another skill hands over an outline, keep its chapters and claims, and keep its source captions exactly as given. Your job is the presentation.

## Step 2: Storyboard

Gather the material into an outline before touching the template. Go from the big picture toward the detail, and tie each detailed chapter back to the larger picture.

For each slide, write down:

- The one idea it carries, as a sentence.
- The visual pattern that shows it best (below).
- The steps: one caption per step, each a short full sentence.
- The source behind each claim.
- Speaker notes: one or two sentences to say out loud.

Pick the pattern that matches the shape of the idea. Use only the ones that help.

| The idea is about | Pattern | Template slide |
|---|---|---|
| Where things come from and what collects them | Flow diagram | `flow` |
| What a source actually says | Excerpt panel, read band by band | `excerpt` |
| Two things compared field by field | Side-by-side excerpt panels | `compare` |
| One thing moving through hand-offs, with what each hop carries | Sequence of states | `run` |
| Conditions that send cases to different outcomes | Decision spine | `decision` |
| Several things passing through the same stages | Lifecycle columns | `lifecycle` |
| One value changing form stage by stage | Journey, one slide per stage | `j1` to `j5` |
| Checking understanding | Question, then the answer on the next step | `q1` to `q3` |

End with a few check-yourself questions when the reader needs to explain or defend the subject. Put the hardest or most uncomfortable one last, in the accent color.

## Step 3: Build

Copy [assets/slideshow/](assets/slideshow/) to `<artifact>/src`, then read the instructions at the top of `deck.html`'s script. They describe the slide object, declarative builds (`data-on` and `data-c`), excerpt panels, and the canvas grid.

The template is a gallery about a fictional parcel delivery service. Reuse its layouts, navigation, and step engine. Replace every example, title, caption, note, and source caption with your own material, and delete patterns you don't use. Set `DECK_TITLE` and `CHAPTERS`.

Build with `node src/build.mjs`. The result is one offline `index.html` with embedded fonts and no network dependencies.

Keep these behaviors from the template:

- A fixed 1920x1080 canvas scaled to the window. Every slide renders from its slide and step number alone, so going back, reloading, and deep links all land on the same state.
- Arrow keys or space step through builds. Shift+arrow skips whole slides, number keys jump to chapters, O toggles the outline, N toggles speaker notes, ? shows every key. The URL hash records slide and step.
- SVG or HTML diagrams with progressive highlights and labelled movement. Excerpt panels with real, selectable text and a highlighted band per step.
- The dark theme, reduced-motion support, and the narrow-screen fallback that shows every slide in one scrolling column.
- If a narrated video exists, set `VIDEO` and the `at` times so each slide links to its moment.

## Step 4: Verify

Run `node src/shoot.mjs` from a directory where Playwright resolves (a project that has it, or a global install). It screenshots every slide at every step, reports console errors, and flags excerpt lines wider than their panel. If Playwright's pinned browser is missing, it uses the newest Chromium in the Playwright cache.

Look at every screenshot. Fix clipping, overlap, text under 24px, misaligned columns, and steps that reveal things in a misleading order. Check navigation, a deep link, and the narrow-screen layout in a browser as well.

## Step 5: Report

Return the path to `index.html`, how to open it, what you verified, and anything you could not verify. Note any claims you marked as illustrative or uncertain.
