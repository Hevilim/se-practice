# Traceability — use cases → stories → criteria

One row per use case. All six rows stay, even the ones with nothing behind them: an empty cell is a
finding you report, not a failure you hide. Use real IDs, comma-separated; write `none` where there
is nothing.

| Use case | Stories (US-nn) | Criteria (AC-nn) | Gap? |
| --- | --- | --- | --- |
| UC-01 View availability | US-01 | none | Yes: no criterion tests it. AC-06 and AC-10 only use it to observe a result. |
| UC-02 Book room | US-02 | AC-01, AC-02, AC-03, AC-04, AC-05, AC-11, AC-12 | No |
| UC-03 Cancel booking | US-03 | AC-06, AC-07, AC-08, AC-09 | No rule from section 1 applies to cancelling, so no criterion tests a business rule. |
| UC-04 Block or unblock room | US-05 | AC-10, AC-11, AC-12 | No |
| UC-05 Review usage | US-06 | none | Yes: no criterion tests it. |
| UC-06 Send confirmation | US-04 | AC-09 | Partly: only the cancellation confirmation is tested; the booking confirmation is not. |

**Stories that belong to no use case:** none (the two generated stories outside the six use cases were merged or deleted — see `lab-report.md` section 3)

**What the gaps tell you:** Every use case has a story, but criteria exist only where a business rule
exists. UC-01 and UC-05 have no rule and no criteria, and the booking confirmation of UC-06 is untested.
