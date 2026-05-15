# V4 Direction Memo: Injection-Vector Replication

Date: 2026-05-02  
Status: ACTIVE DIRECTIVE — supersedes earlier V4 draft  
Author: Principal  

---

## What V4 Is

A larger-scale replication of a single, clean observation from the morning session:

> **False premise + task frame → hallucination.**  
> **Same domain, no task frame → accurate answer from real knowledge.**

That observation held in 4 manual tests across 3 models. V4 runs it at scale across
12 domains and 3 models, using the same false anchors the V3 lab built.

V4 is not a novel intervention. It is not claiming to solve hallucination.
It is a replication. Frame it exactly that way.

---

## What V4 Is Not

- Not "premise removal solves hallucination." That claim is too strong and not the point.
- Not a deployable intervention (users don't know their premises are false).
- Not a replacement for V3's verify-gate finding.
- Not V5. The task-operator question (what makes the model step into the trap) comes next.

The auditing agent's tautology critique is noted. It is correct in the abstract.
The reason to run V4 anyway: the morning session was informal and small. Before the lab
moves to mechanism-level questions in V5, the replication should be on record at scale,
cleanly preregistered, with the same anchors and rubric the lab already built.

---

## The Comparison

V4 runs two conditions for each of the 12 V3 anchors:

| Condition | Description | Source |
|---|---|---|
| `false_anchor_forced` | Fake entity embedded as typed object + `type: explain` | Reuse V3 data |
| `false_anchor_open_structure` | Same domain, no fake entity, no task frame | New — V4 corpus |

That is the complete experiment. V3's `false_anchor_plain` and `verify_gate` conditions
are already in the record and provide context. V4 adds only the open-structure arm.

**Models:** OpenAI (`gpt-5-chat-latest`) and Anthropic (`claude-sonnet-4-6`) only.
V4 compares directly against V3 matched forced-condition data, so model scope must
match V3 exactly. xAI is out of scope for V4 and requires a separate preregistration
to add. **Total calls: 12 × 1 × 2 = 24.**

---

## The Hypothesis

> In each of the 12 V3 anchor domains, the open-structure query (false anchor removed,
> no task frame) will produce zero or near-zero hallucination-positive responses, while
> the `false_anchor_forced` condition (same anchors, same models) produced hallucination
> in the majority of OpenAI responses in V3.

**Preregistered threshold:**  
`open_structure hallucination-positive rate ≤ 0.10` across both models combined.

Do not use the word "significant." Report the observed rate and Wilson 95% CI.
The comparison claim is: "open-structure rate is lower under the preregistered
threshold than the V3 forced condition rate, with exact intervals reported."

---

## What V4 Would Establish If the Hypothesis Holds

> In a preregistered 12-anchor replication, removing the fabricated entity and
> task frame from the prompt while holding domain and output format constant
> reduced the hallucination-positive rate to X/24 (Wilson 95% CI [lo, hi]),
> compared to 8/12 in the matched `false_anchor_forced` condition in V3.
> This is consistent with the injection-vector account: the prompt schema causes
> the model to complete a nonexistent object rather than retrieve real knowledge.
> It does not establish whether the false anchor or the task frame is the primary
> driver — that is the V5 question.

The last sentence is the honest boundary and must appear in the results memo.

---

## What Comes After: V5

The task-operator question:

> Holding domain, output format, and false anchor constant, does varying the task
> operator — `{no_directive, explain, summarize, analyze, prove, verify, critique}` —
> change the hallucination rate?

This is the mechanism-level experiment. The morning session showed one word
(`type: explain` vs `type: prove`) flipped Claude's epistemic behavior. V5 replicates
that at scale. V5 is a separate preregistration. Do not scope it into V4.

---

## The Corpus

The V4 open-structure corpus is at:  
`corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`

12 prompts. Three scoring note corrections have been applied:
- VG008: Removed "Avoid-the-Interruptor suite" (not a real benchmark name)
- VG009: Corrected OECD Pillar Two reference (tax policy, not climate)
- VG012: Removed specific unverified bill number HB 4337; generalized to framework level

Principal has verified the corpus. Agents may proceed to preregistration.

---

## Preregistration Steps (in order)

1. SHA256 the corpus file. Record in `proofs/SHA256_INPUTS_V4.txt`.
2. Write `protocols/OSF_PREREG_V4_OPEN_STRUCTURE.md` with:
   - Hypothesis (as stated above)
   - Threshold: open_structure rate ≤ 0.10
   - Models: gpt-5-chat-latest, claude-sonnet-4-6
   - Scoring: same rubric as V3 (`scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`)
   - Analysis plan: report per-model and combined rates with Wilson 95% CIs;
     compare to V3 `false_anchor_forced` condition
3. Commit prereg before any model call. Gate commit must precede run commit.
4. Run. Record deviation if any cell truncates beyond the 10% threshold.
5. Score. Use dual-judge (OpenAI + Claude) per V3 Auditor A's recommendation.
6. Report. Results memo must include Wilson 95% CIs and the honest boundary
   sentence about V5.

---

## Pointers

- V3 close-out: `proofs/CLOSEOUT_MEMO_20260502.md`
- V4 corpus: `corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`  
- Morning session paper: `archive/EXPLORATORY_PAPER_V1_20260502_SUPERSEDED.md`
- V5 scope (task-operator): noted above, not yet designed
