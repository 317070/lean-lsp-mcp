INSTRUCTIONS = """
This MCP server provides a comprehensive set of tools for interacting with Lean 4 projects, allowing you to inspect proof states, search for declarations, and query the compiler.

## General Constraints
- **1-Based Indexing**: All line and column numbers are 1-indexed.
- **Read-Only**: These tools are for reading state and searching. File modifications are not supported.

## Core Proof & Development Tools
Primary tools for inspecting the local Lean state.
- **`lean_goal`**: Inspects the proof state at a specific position.
    - **Usage**: Provide `line`. Omit `column` to see goals *before* (start of line) and *after* (end of line) the tactic.
    - **Note**: "no goals" indicates the proof is complete.
- **`lean_term_goal`**: Checks the expected type at a specific position.
- **`lean_hover_info`**: Retrieves type signatures and documentation for a symbol.
    - **Requirement**: `column` must be at the START of the identifier.
- **`lean_diagnostic_messages`**: Lists compiler errors, warnings, and information.
    - **Note**: "no goals to be solved" typically implies the tactic is unnecessary.
- **`lean_completions`**: Returns IDE autocompletions for incomplete code (e.g., after `.`).

## Project, File & Utility Tools
- **`lean_file_outline`**: Generates a high-level skeleton of the file (imports, declarations). Efficient for large files.
- **`lean_multi_attempt`**: Tests multiple tactic variants *without* editing the file.
    - **Usage**: Accepts a list of snippets, e.g., `["simp", "ring", "omega"]`. Returns the resulting goal state for each.
- **`lean_declaration_file`**: Retrieves the source code of a declaration.
    - **Warning**: Can produce large output. Use sparingly.
- **`lean_run_code`**: Runs a standalone, self-contained Lean snippet.
- **`lean_build`**: Rebuilds the project and restarts the LSP.
    - **Usage**: Only needed after adding new imports or dependencies. This is SLOW.
- **`lean_profile_proof`**: Profiles a theorem to identify performance bottlenecks.

## Search & Discovery Tools (Rate Limited)
Tools for finding lemmas, definitions, and concepts.

### 1. Local Search (Fast, No Rate Limit)
- **`lean_local_search`**: Checks if a declaration exists in the current environment.
    - **Recommendation**: Use this *before* guessing a lemma name.

### 2. Semantic & Natural Language Search
- **`lean_leansearch`** (Limit: 3/30s): Searches Mathlib using natural language.
    - *Example*: "sum of two even numbers is even"
- **`lean_leanfinder`** (Limit: 10/30s): Searches for mathematical concepts.
    - *Example*: "commutativity of addition"

### 3. Type & Pattern Search
- **`lean_loogle`** (Limit: 3/30s): Searches Mathlib by type signature or pattern.
    - *Example*: `(?a -> ?b) -> List ?a -> List ?b`

### 4. Proof Automation Search
- **`lean_state_search`** (Limit: 3/30s): Finds lemmas that can close the current goal.
- **`lean_hammer_premise`** (Limit: 3/30s): Finds premises (lemmas) to feed into automated tactics like `simp` or `aesop`.

## Choosing a Search Tool

Select the tool that best matches your current information and goal:

### 1. Verifying & Finding Known Names
**Tool**: `lean_local_search`
- **When to use**: You have a guess at the name (e.g., "something with `add_comm`") or want to check if a specific lemma is available in your current imports.
- **Why**: It is the only search tool that is instant, unlimited, and aware of your local environment.

### 2. Searching by Meaning or Description (Natural Language)
**Tools**: `lean_leansearch`, `lean_leanfinder`
- **Use `lean_leansearch`** when you want to find a specific theorem by describing it in English.
    - *Scenario*: "I need a lemma stating that the sum of two even numbers is even."
- **Use `lean_leanfinder`** for broader conceptual searches or to find definitions.
    - *Scenario*: "What is the definition of a 'Group' in Mathlib?" or "Find theorems related to 'compactness'."

### 3. Searching by Mathematical Structure (Type/Pattern)
**Tool**: `lean_loogle`
- **When to use**: You know the *shape* of the theorem or function but not its name.
- **Why**: It allows precise pattern matching on types.
    - *Scenario*: "I need a function that takes a list and returns a boolean (`List ?a -> Bool`)."
    - *Scenario*: "Find a theorem matching `?a * ?b = ?b * ?a`."

### 4. Searching Based on the Current Proof State
**Tools**: `lean_state_search`, `lean_hammer_premise`
- **Use `lean_state_search`** when you have a specific goal you want to close *directly*.
    - *Scenario*: "My goal is `⊢ n + m = m + n`. Is there a single lemma that solves this?"
- **Use `lean_hammer_premise`** when you need *ingredients* for automated tactics.
    - *Scenario*: "I want to run `simp` or `aesop`, but it's stuck. What lemmas should I add to the context to help it?"

**Tip**: Remote search tools (LeanSearch, Loogle, etc.) index Mathlib but do NOT know about your local file's uncommitted changes. Always verify results with `lean_local_search`.

## Error Handling
- **`isError`**: Check this field in responses.
    - `true`: Tool execution failed (e.g., timeout, LSP error).
    - `false` (with empty result `[]`): The tool ran successfully but found no results.
"""
