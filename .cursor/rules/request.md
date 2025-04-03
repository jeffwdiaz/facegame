{
create the HTML and CSS portion of the described below. start with the structure and ask me if I want to continue preiodically.

Context:   
FaceGame
A game about faces

FaceGame (placeholder name) is a name learning game. The goal is to match the face to the correct name. This is a web application that will be designed mobile-first. The game will have two modes. An easy mode that will pull first names, and a hard mode that will pull last names. The game will have user profiles with game history data and a leaderboard.

How it works: An image appears in the middle. One name appears above the image and another below it. The user then has to flick the image up or down to match the image with the correct name. The user will gain a point for each correct answer, and lose one point for incorrect answers. There will also be a loss of 1 point per second to encourage speed. The user will start with 10 points, and lose if the points reach 0. Then the game will stop and show the user’s highest score achieved. }

---

Design and implement the request described above using a systematic, validation-driven approach:

1. **Map System Context**:
   - Explore the codebase structure with `tree -L 4 --gitignore | cat` to locate where the feature belongs.
   - Identify relevant patterns, conventions, or domain models using `codebase_search` to ensure seamless integration.
   - Pinpoint integration points—e.g., UI components, data layers, or APIs—affected by the request.

2. **Specify Requirements**:
   - Break the request into clear, testable criteria—e.g., “Button triggers save, shows success state.”
   - Define use cases (normal and edge) and constraints (e.g., performance, UI consistency).
   - Set scope boundaries to keep the implementation focused and maintainable.

3. **Leverage Reusability**:
   - Search for existing components or utilities with `codebase_search` that can be adapted—e.g., a “button” component or “save” function.
   - Use `grep_search` to confirm similar implementations, ensuring consistency with project standards.
   - Evaluate if the feature could be abstracted for future reuse, noting potential opportunities.

4. **Plan Targeted Changes**:
   - List all files requiring edits (relative to workspace root), dependencies to update, and new files if needed.
   - Assess impacts on cross-cutting concerns—e.g., error handling, logging, or state management.
   - Balance immediate needs with long-term code health, planning minimal yet effective changes.

5. **Implement with Precision**:
   - Provide a step-by-step plan with specific code changes—include file paths, line numbers, and snippets.
   - Adhere to project conventions (e.g., naming, structure) and reuse existing patterns where applicable.
   - Highlight enhancements to organization or clarity—e.g., “Extract logic to a helper function.”

6. **Validate and Stabilize**:
   - Define test scenarios—e.g., “Save with valid data,” “Save with no input”—to confirm functionality.
   - Suggest validation methods: unit tests, UI checks, or logs, tailored to the project’s practices.
   - Recommend a stability check—e.g., “Monitor save API calls”—with rollback steps if issues arise.

This process delivers a well-integrated, reliable solution that enhances the codebase while meeting the request’s goals.