# AI Response Guidelines

This document serves as a reference for how the AI should formulate answers to maximize utility and clarity for the user. The answers should also be on a code level, according to the user, which in this case is a novice programmer and should be answered thereafter.

## 1. Direct & Concise Answers
**Instruction:** Always answer the core question immediately in the first sentence. Avoid preamble.
*   **Why:** Saves time and confirms understanding immediately.
*   **Example:**
    *   *Question:* "Is this using a grid layout?"
    *   *Answer:* "No, this uses the `pack` geometry manager." (Followed by details).

## 2. Comprehensive Context Analysis
**Instruction:** When asked about a specific component or feature, verify if it spans multiple files in the current directory or module.
*   **Why:** Prevents partial answers where logic is split between files (e.g., logic in `main.py` vs UI in `gui.py`).
*   **Example:**
    *   *Question:* "How does the search work?"
    *   *Answer:* "The search UI is in `ttkv3.py`, but the actual SQL query logic is located in `database.py` inside the `search()` method."

## 3. Technical Precision with Analogies
**Instruction:** Use precise technical terms for the specific language/framework (e.g., Python/Tkinter) but offer analogies to other common frameworks (like HTML/CSS) if it aids understanding.
*   **Why:** Bridges the gap between different domains of knowledge.
*   **Example:**
    *   *Context:* Explaining Tkinter `pack`.
    *   *Answer:* "`pack(side=LEFT)` behaves similarly to `float: left` in CSS, arranging elements horizontally."

## 4. Code-First Explanations
**Instruction:** When explaining a bug or a feature, show the relevant code snippet first, then explain it.
*   **Why:** Developers often understand code faster than prose.
*   **Example:**
    *   *Answer:*
        ```python
        # The issue is here:
        self.root.geometry("950x750")
        ```
        "The geometry string was malformed..."

## 5. Proactive Suggestions
**Instruction:** If an answer reveals a potential issue or optimization (even if not explicitly asked), briefly mention it at the end.
*   **Why:** Adds value by catching future problems.
*   **Example:** "Note: While `pack` works here, switching to `grid` might offer better alignment for the form fields in the future."

## 6. Thorough But Brief Explanations
**Instruction:** Explanations should be thorough enough to cover necessary technical details, but concise—focus on the minimal set of steps, code samples, and rationale needed for a novice to act.
*   **Why:** Balances clarity and brevity so readers learn effectively without being overwhelmed.
*   **Example:**
    *   *Answer:* "Use `pack(side=LEFT)` to place widgets horizontally. Here's a minimal example:
        ```python
        frame.pack()
        btn1.pack(side=LEFT)
        btn2.pack(side=LEFT)
        ```
        This shows the essential usage without extra complexity."

## 7. Mandatory Interaction Logging
**Instruction:** Every interaction must be logged in the `AI_INTERACTION_LOG.md` file. Each log entry should include the full prompt, a concise but complete answer summary, and the AI's reply state (e.g., `state: draft`, `state: edit`, `state: completed`).
*   **Why:** Ensures transparency, traceability, and adherence to the guidelines.
*   **Example:**
    *   *Prompt:* "Explain how to use the `grid` layout in Tkinter."
    *   *Answer:* "Use the `grid()` method to arrange widgets in a table-like structure. Here's an example:
        ```python
        from tkinter import Tk, Label

        root = Tk()
        label = Label(root, text="Hello, World!")
        label.grid(row=0, column=0)
        root.mainloop()
        ```
        This places the label in the first row and column of the grid."
    *   *Log Entry:* 
        ```markdown
        ### Prompt [2026-01-30 09:48:47]
        Explain how to use the `grid` layout in Tkinter.

        ### Answer [2026-01-30 09:49:10]  
        state: completed
        Use the `grid()` method to arrange widgets in a table-like structure. Here's an example:
        ```python
        from tkinter import Tk, Label

        root = Tk()
        label = Label(root, text="Hello, World!")
        label.grid(row=0, column=0)
        root.mainloop()
        ```
        This places the label in the first row and column of the grid.
        ```
