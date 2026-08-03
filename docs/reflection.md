# Reflection

For this mid-course project, I used ChatGPT as the main AI assistant to reconstruct the Task Tracker baseline from the course transcripts and then extend it with two scoped features: due dates with an overdue filter, and tags with tag filtering. I used the AI assistant for planning, user story drafting, implementation guidance, test case ideas, and documentation structure. I did not treat the first output as final. I reviewed the generated ideas against the project brief and course workflow before deciding what to accept.

One moment AI helped was during feature scoping. The project brief included several possible features, and it would have been easy to choose something too large, such as comments or an activity log. AI helped compare the options and keep the implementation small enough to complete end-to-end with backend validation, frontend usability, and pytest coverage. That matched the course emphasis that a polished, verified feature is better than an ambitious unfinished one.

One moment AI slowed me down was tag design. The first direction suggested storing tags as a comma-separated string. That looked simple at first, but it would make validation and filtering weaker. I rejected that assumption and kept tags as a list in the backend contract. The frontend still accepts comma-separated input, but the API stores clean structured data.

My review changed the result in the overdue feature as well. I decided that overdue should be computed in the backend, not only in the UI. That made the behavior testable with pytest and prevented the frontend from duplicating business logic. I also corrected the frontend edit behavior so it sends only changed fields during PATCH. Without that review, unchanged status values could have triggered the backend transition rule and broken ordinary edits.

Overall, AI helped me move faster, but the important work was inspecting, constraining, testing, and correcting the output. The final result is not just generated code; it is code that was reviewed, run, tested, intentionally broken, restored, and documented.
