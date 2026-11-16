---
name: "under-the-hood"
description: "Explain a PR, branch, or subsystem through its data shapes, runtime flow, and state transitions, then hand the verified outline to a presentation skill (an interactive slideshow by default). Use for code walkthroughs, onboarding, design reviews, or whiteboard preparation."
metadata:
  version: "2.0.0"
---

# Under the hood

Build an explanation that prepares the reader to explain how the target works, why its design makes sense, and where it fails. Start with the system's purpose, then connect each detail to that context.

Use the target's own concepts. A command-line tool, library, user interface, service, and background worker may need different explanations. Include state machines, external calls, persistence, concurrency, or costly operations only where the code supports them.

## Ground rules

- Keep the target source read-only. Write explanation artifacts separately.
- Own the content, not the presentation. Research and outline here; let the presentation skill handle layout, navigation, and rendering.
- Trace implementation claims to source files and lines. Distinguish observed behavior from inferred intent. Report disagreements between code and descriptions.
- Use representative tests and fixtures for worked examples. Access production data only with explicit approval.
- Define domain terms on first use. Adapt the explanation to the reader's experience and goal.
- Distinguish calls from reuse of existing output. Describe actual side effects, dependencies, and costs.
- Show short excerpts of real target code with a `path:line` caption and marked omissions. Label illustrative code explicitly.

## Step 1: Scope

Identify the target, the reader's goal, and the intended depth from the request and available context. Ask once for any missing information that prevents useful work.

The target may be a PR, a stack, a branch, a subsystem, or a proposed design. For a proposal, distinguish intended behavior from existing implementation. Note the output format the user wants; an interactive slideshow is the default.

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

Record the evidence for each chapter before presenting it. Connect each detailed chapter back to the larger flow.

## Step 5: Present

Hand the outline to a presentation skill. Use [create-slideshow](../create-slideshow/SKILL.md) by default. If the user asked for another format, such as a video or a written document, use the skill for that format instead. This skill decides what the explanation says; the presentation skill decides how it looks and behaves.

Give the presentation skill everything it needs to work without reading the target:

- The reader, their goal, and the depth they need.
- The chapter outline, with one idea per unit (a slide, a scene, a section) and the order in which its pieces should appear.
- The diagrams from Step 3, named by kind (flow, state machine, lifecycle, decision tree, data journey), with their nodes, transitions, triggers, and guards.
- Short verbatim code excerpts, each captioned `path:line`, with omissions marked and the lines to highlight at each step. Mark them as code.
- Representative values from tests or fixtures for any worked example.
- Speaker notes, and the whiteboard questions with their answers and citations.
- Which claims are inferred rather than observed, and any disagreements between code and descriptions.

Once the artifact is built, check that it kept every `path:line` caption and every uncertainty you handed over. Fix anything the presentation step changed in meaning.

## Step 6: Report

Return the artifact's path, how to open it, the behavior verified, and any limits on verification. Report discrepancies or suspected bugs with source locations. Leave changes to the target implementation for a separate request.
