---
name: "under-the-hood"
description: "Explain a PR, branch, or subsystem through its data shapes, runtime flow, and state transitions in an interactive HTML slideshow. Use for code walkthroughs, onboarding, design reviews, or whiteboard preparation."
metadata:
  version: "1.0.0"
---

# Under the hood

Create an interactive slideshow that prepares the reader to explain how the target works, why its design makes sense, and where it fails. Start with the system's purpose, then connect each detail to that context.

Use the target's own concepts. A command-line tool, library, user interface, service, and background worker may need different explanations. Include state machines, external calls, persistence, concurrency, or costly operations only where the code supports them.

## Ground rules

- Keep the target source read-only. Write explanation artifacts separately.
- Trace implementation claims to source files and lines. Distinguish observed behavior from inferred intent. Report disagreements between code and descriptions.
- Use representative tests and fixtures for worked examples. Access production data only with explicit approval.
- Define domain terms on first use. Adapt the explanation to the reader's experience and goal.
- Distinguish calls from reuse of existing output. Describe actual side effects, dependencies, and costs.
- Show short excerpts of real target code with a `path:line` caption and marked omissions. Label illustrative code explicitly.

## Step 1: Scope

Identify the target, the reader's goal, and the intended depth from the request and available context. Ask once for any missing information that prevents useful work.

The target may be a PR, a stack, a branch, a subsystem, or a proposed design. For a proposal, distinguish intended behavior from existing implementation. Deliver an interactive HTML slideshow by default.

## Step 2: Research

Trace the target through these areas where applicable:

- Entry points, inputs, outputs, and external dependencies.
- Core types and the transformations between them.
- Mutable state, transition writers, triggers, and guards.
- The central algorithm and its boundaries with I/O.
- Concurrency, ordering, retries, cancellation, and failure handling.
- Tests and fixtures with observable expected outcomes.
- Commit history, descriptions, and review comments that explain intent and tradeoffs.

For a large target, delegate independent read-only areas when agents are available. Give each a self-contained scope and require verbatim code, source locations, and explicit uncertainty. Read the key implementation files yourself before using their claims.

Finish with an evidence-backed outline of the target's runtime flow, data shapes, and relevant decisions.

## Step 3: Model behavior

Choose the diagrams the system needs:

- Use a flow diagram for calls and data movement across boundaries.
- Use a state machine for an entity whose behavior depends on its current state. Name each transition's trigger and guard, including failure exits.
- Use a lifecycle diagram when several entities pass through shared stages.
- Use a decision tree when conditions select different outcomes.
- Use a data journey when a value changes representation across stages.

Identify unreachable states, missing transitions, and behavior the user cannot observe. Cite the code responsible. Use only the diagrams that clarify this target.

## Step 4: Outline the chapters

Move from the broad context toward the details. Select and reorder chapters to fit the target:

1. Purpose and domain context.
2. Inputs, outputs, and ownership of each responsibility.
3. Runtime flow and system boundaries.
4. Core types and data transformations.
5. Algorithms and decisions, using a representative example.
6. State transitions and lifecycle, if present.
7. Side effects, resource costs, and concurrency, if present.
8. Failure cases, recovery, and practical limits.
9. One value or operation traced end to end.
10. Whiteboard questions about alternatives, assumptions, misuse, and failure.

Record the evidence for each chapter before building the slides. Connect each detailed chapter back to the larger flow.

## Step 5: Build and verify

Start from [assets/slideshow/](assets/slideshow/). Copy the folder to `<artifact>/src` and read the engine instructions at the top of `deck.html`'s script.

The template is a gallery of fictional software examples. Reuse its layouts, navigation, and step engine. Replace all sample content and source captions with verified material from the target, and delete layouts you do not need. Its example task queue, states, storage operations, and transformations prescribe no architecture for the target.

Build with `node src/build.mjs`. The result is one offline `index.html` with embedded fonts and no network dependencies.

Keep these presentation behaviors:

- Render a fixed-size slide canvas scaled to the window. Each slide must render entirely from its slide and step number so back navigation, reloads, and deep links reproduce the same state.
- Step through builds with arrow keys or space. Support whole-slide navigation, a toggleable outline, a progress indicator, keyboard help, and slide-and-step URL hashes.
- Use SVG or HTML diagrams with progressive highlights and labelled data movement. Use selectable code with line highlights and source captions.
- Include speaker notes and questions whose answers appear on the next step.
- Keep the dark theme, minimal visual clutter, reduced-motion support, and narrow-screen fallback.

Run `node src/shoot.mjs` from a directory where Playwright resolves. It captures each slide and build step, reports console errors, and checks code-panel width. If the pinned browser is unavailable, use an installed cached Chromium. Inspect every image and fix clipping, overlap, unreadable text, and misleading reveal order. Check navigation, deep links, and the narrow-screen layout as well.

Finish with a working offline artifact whose claims are supported by the target, with uncertainty stated explicitly.

## Step 6: Report

Return the artifact's path, how to open it, the behavior verified, and any limits on verification. Report discrepancies or suspected bugs with source locations. Leave changes to the target implementation for a separate request.
