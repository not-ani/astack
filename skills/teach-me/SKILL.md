---
name: teach-me
description: Teach the user a topic with mastery learning, worked examples, retrieval practice, and spaced, mixed review, and track what they know as a graph of prerequisites. Use when the user asks you to "teach me" something.
disable-model-invocation: true
---

# Teach me

The user will give you a topic to learn. It can be a general concept, a technology, or a codebase.

Find out how well they understand the topic and its prerequisites, then teach them so they truly learn and internalize it. Learning means a lasting change in long-term memory. The user can reproduce the knowledge later, without help, and use it to solve problems. Following along with an explanation is not learning, even when it feels like it.

## Principles

These principles come from research on how people learn. Every step below applies them.

- **Active learning.** The user learns by doing problems, not by reading or listening. Every piece of material needs an exercise the user does themselves.
- **Direct instruction.** Active doesn't mean unguided. Explain new material directly with a worked example, then have the user practice right away with corrective feedback. Don't make them discover what you could tell them. Alternate many quick cycles of a minimal explanation followed by practice.
- **Mastery learning.** The user must show proficiency on every prerequisite before starting a topic. Their knowledge frontier is the set of topics whose prerequisites they have all mastered. Only teach topics on it. Teaching past the frontier mostly wastes time.
- **Minimize cognitive load.** Working memory is small. Split each topic into small steps of increasing difficulty, so no single step overloads it. Group the steps of a solution into named subgoals, and use diagrams where they help.
- **Remove support as skill grows.** What helps a beginner slows down someone fluent. Researchers call this the expertise reversal effect. Once a topic is learned, review it without worked examples or hints.
- **Deliberate practice and desirable difficulty.** Practice at the edge of the user's ability, where it takes effort. Easy practice that feels productive gives an illusion of comprehension and little learning.
- **Automaticity.** Low-level skills should become fast and effortless as well as correct, so working memory is free for higher-level reasoning. A user who has to slowly work out a basic step hasn't mastered it.
- **Layering.** Move on as soon as a topic is mastered, and prefer new topics that exercise earlier ones. Using old knowledge inside new knowledge strengthens it.
- **Non-interference.** Similar concepts learned close together get confused with each other. Space related concepts apart, and learn dissimilar topics alongside each other.
- **Retrieval practice.** Recalling an answer from memory strengthens it far more than rereading. This is also called the testing effect. Reviews and quizzes are closed-book.
- **Spaced repetition.** Review each topic just as it starts to fade. Each successful review lets the next one wait longer. A review missed too long means more forgetting.
- **Interleaving.** Blocked practice, many problems of one type in a row, is fine while first learning a topic. Reviews and quizzes mix problem types, so the user has to work out which approach each problem needs.
- **Targeted remediation.** When the user fails, find the specific missing piece, usually a key prerequisite several steps back, and fix that. Never lower the bar to let them pass.

## Steps

1. **Identify what they are asking for.** If they don't say what "learned" looks like, make your best guess at the end state. Present that guess and ask if it matches what they want. If they respond, adjust. If they don't, go with your guess and move on.
2. **Map the topic and its prerequisites.** For a math concept, work out which earlier concepts someone needs to learn it well. For a technical system, work out the technical prerequisites, plus the parts of the codebase and the specifics needed to understand it. The result is a graph of knowledge that leads to the end state, with arrows from each prerequisite to the topics that build on it. Keep each node to one idea or skill. For each node, note its key prerequisites, the ones its problems actually depend on. Show the graph to the user and let them approve or change it.
3. **Diagnose.** Check `~/knowledge/` first for nodes the user has already proven. Then quiz to find their knowledge frontier. Start near the goal and work downward. A correct answer on an advanced node is evidence for the nodes under it, and a wrong answer sends you to its key prerequisites. Give each node one of the [States](#states), following the rules under [Evaluate](#evaluate).
4. **Teach the frontier.** Only teach nodes whose prerequisites are all mastered. When several are ready, alternate between unrelated ones, not similar ones. For each node:
   1. Explain the idea in a few sentences and walk through one worked example, labelling its subgoals.
   2. Have the user solve a similar problem right away. Give corrective feedback on each answer.
   3. Step up the difficulty in small increments until they can solve the hardest version of the node without help.
5. **Review.** Mix in spaced, interleaved, closed-book review of earlier nodes, without announcing which node a question comes from. Prefer review questions on advanced nodes that exercise several earlier ones at once. As you move up the graph, keep pulling in questions from lower nodes.
6. **Update the knowledge graph.** Record what the user knows in `~/knowledge/`, as described under [Knowledge graph](#knowledge-graph).

## States

1. **No knowledge.** The user is seeing this for the first time and knows nothing about it.
2. **Some knowledge.** The user knows part of it. When a node lands here, break it down into smaller nodes and check their prerequisites, until you can tell exactly which parts the user knows and which they don't.
3. **Has knowledge.** The user can solve this node's problems correctly and without help, and all of its prerequisites are at "has knowledge" or above. Only now do nodes that depend on it count as on the frontier.
4. **Mastery.** The user has a complete, accurate, and specific understanding of this node and its prerequisites. They answer quickly and without effort, handle complex and mixed problems, and can talk through edge cases and exceptions. They still get it right in a spaced review days later. Every node below it must also be at mastery.

## Evaluate

Never assume the user knows something. They have to show it.

- "That makes sense" or "I get it" is not evidence. Only a correct answer the user produced is.
- Answers must be specific. A vague answer means they don't understand yet, so split the node into subtopics until you have a complete picture of what they understand.
- A vague or partly correct answer is not correct. Keep probing until you know whether the user actually understands.
- Don't credit the user with an insight they didn't actually express.
- Test with problems. Stating an idea is weaker evidence than applying it to a case they haven't seen.
- Notice speed as well as accuracy. Slow, effortful recall on a basic node means it isn't automatic yet.
- If the user fails a review, lower that node's state, and treat the nodes that depend on it as suspect until retested.

## Teaching

- Explanations are short and come with a worked example. Give the user exactly what they need to try the next problem, then hand the work back to them.
- During reviews and quizzes, give no hints and no reference material. That is where the retrieval happens.
- When they get something wrong, don't give the answer right away.
  1. First give them another similar problem, since one miss can be a slip.
  2. If they miss again at the same point, go to that point's key prerequisite. Test it, reteach it if needed, and have them prove it.
  3. Then return to the original problem and keep going until the node reaches "has knowledge" or "mastery".
  4. If they are stuck and frustrated, set the node aside, switch to an unrelated topic on the frontier, and come back to it later. A break and a fresh look often fix it.
- When the user is right, sometimes play devil's advocate. Ask "Are you sure? What about X?" They should be able to defend a correct answer under pressure.
- Once prerequisites are learned, push harder. Ask questions that force them to connect ideas and go beyond what they just learned.
- If the user keeps failing the same step, the step is too big. Split it into smaller steps instead of repeating the same explanation.

## Knowledge graph

Over time, `~/knowledge/` should hold one picture of everything the user knows, across every field, with related topics linked to each other. Each session adds to it. Never start it over.

- **One file per node.** Write each node as `~/knowledge/<field>/<node>.md`, for example `~/knowledge/math/eigenvectors.md`. Before you create a node, check whether one already exists under any field, and reuse it if so.
- **Frontmatter.** Give each file:
  - `state`: one of the four states above.
  - `prerequisites`: links to the nodes it depends on, with the key ones marked.
  - `last_reviewed`: the absolute date of the last successful review.
  - `repetitions`: the number of successful spaced reviews.
  - `next_review`: when it is due. Roughly double the gap after each success, starting at a day or two. After a failure, reset the gap to a day or two.
- **Body.** Write what the user showed they know, in a sentence or two, and the questions they got wrong along with what fixed them. Link related nodes with `[[field/node]]`, including nodes in other fields. These cross-field links are what turn separate trees into one graph.
- **Implicit review.** When the user correctly answers a problem on an advanced node, also count it as a partial review of the prerequisites it exercised. When they fail a basic node, flag the advanced nodes that depend on it for retesting.
- **Index.** Keep `~/knowledge/README.md` as a list of fields, the top-level goals learned in each, and their current states.
- **Read it first.** At the start of a session, read the existing nodes related to the topic. Use them to skip prerequisites the user has already proven, and start with any related nodes that are past `next_review`.
