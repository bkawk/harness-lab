#!/usr/bin/env bash
# External review using Claude Code CLI (uses your Max plan, not API credits).
# Called automatically by the lab when a review trigger fires.

set -euo pipefail

INDEX="$HARNESS_LAB_CANDIDATE_INDEX_PATH"
HINDSIGHT="$HARNESS_LAB_HINDSIGHT_PATH"
POLICY="$HARNESS_LAB_POLICY_PATH"
RESULT="$HARNESS_LAB_EXTERNAL_REVIEW_RESULT_PATH"
TRIGGER="$HARNESS_LAB_EXTERNAL_REVIEW_TRIGGER"

PROMPT="You are reviewing an automated research lab. The review was triggered by: ${TRIGGER}.

Here is the candidate index (recent candidates, outcome counts):
$(cat "$INDEX" | head -200)

Here is the hindsight analysis:
$(cat "$HINDSIGHT" | head -100)

Here is the current policy:
$(cat "$POLICY" | head -50)

Respond with ONLY a JSON object (no markdown fences) with these fields:
- \"situation_summary\": one paragraph summarizing the lab's current state
- \"lab_advice\": array of {\"kind\": string, \"summary\": string} objects with actionable advice for the automated lab
- \"human_advice\": array of {\"kind\": string, \"summary\": string} objects with advice requiring human intervention
- \"confidence\": float between 0 and 1"

claude -p "$PROMPT" --output-format text > "$RESULT"
