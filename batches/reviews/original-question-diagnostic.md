# Original-question retrieval diagnostic

Final session check:112/116 original questions retrieved every required evidence window across batches003–009. This uses the distinct `question` field, not the curated query. Cases without that field are excluded. It is not a blind paraphrase benchmark or generated-answer score; short untimed episodes can fit most source text into returned context, making this an easier test.

Four unresolved misses are recorded in [the exact report](original-question-diagnostic.json): CQ80's broad ranking question; CQ14's store-origin question; CQ15's unspecified follow-ups question; CQ82's broad organizational-work question. Their curated development queries pass, but that does not establish arbitrary wording robustness.

Next retrieval work should route ranking requests to typed prominence, use explicit host/entity expansion for biography and event questions, and expose effective query terms rather than silently ignoring terms after the existing sixteen-term cap. Add held-out paraphrases before claiming conversational readiness. Do not repair this diagnostic by removing required windows or replacing questions with tuned queries. Episode extraction acceptance is separate from a future live answer-interface gate.
