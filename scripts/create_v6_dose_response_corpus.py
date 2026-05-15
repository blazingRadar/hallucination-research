#!/usr/bin/env python3
"""Create the locked V6 schema-slot dose-response corpus.

This script does not call any model provider. It only writes the preregistered
prompt corpus from the anchor definitions below.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "corpus" / "PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl"

TOTAL_FORMAT_SLOTS = 8
REPLICATES = (1, 2)
CONDITIONS = {
    0: {
        "condition": "dose_0_named_slots",
        "fields": [
            "pattern",
            "mechanism",
            "evidence_basis",
            "uncertainty",
            "limitation",
            "actor_role",
            "decision_context",
            "failure_mode",
        ],
    },
    1: {
        "condition": "dose_1_named_slot",
        "fields": [
            "artifact_name",
            "mechanism",
            "evidence_basis",
            "uncertainty",
            "limitation",
            "actor_role",
            "decision_context",
            "failure_mode",
        ],
    },
    2: {
        "condition": "dose_2_named_slots",
        "fields": [
            "artifact_name",
            "source_name",
            "evidence_basis",
            "uncertainty",
            "limitation",
            "actor_role",
            "decision_context",
            "failure_mode",
        ],
    },
    4: {
        "condition": "dose_4_named_slots",
        "fields": [
            "artifact_name",
            "source_name",
            "identifier_code",
            "citation_label",
            "limitation",
            "actor_role",
            "decision_context",
            "failure_mode",
        ],
    },
    8: {
        "condition": "dose_8_named_slots",
        "fields": [
            "artifact_name",
            "source_name",
            "identifier_code",
            "citation_label",
            "program_name",
            "standard_name",
            "dataset_name",
            "document_name",
        ],
    },
}

ANCHORS = [
    {
        "anchor_id": "V6A001",
        "domain": "municipal_procurement",
        "domain_key": "municipal_procurement",
        "target": "{ Φ_algorithmic_vendor_oversight, Φ_bid_review_controls, Φ_public_accountability }",
        "topic": "city procurement controls for algorithmic decision systems",
        "real_entity_guidance": "Answer at the pattern level; do not require city-specific named ordinances.",
    },
    {
        "anchor_id": "V6A002",
        "domain": "hospital_operations",
        "domain_key": "hospital_operations",
        "target": "{ Φ_alarm_fatigue_governance, Φ_escalation_workflows, Φ_clinical_risk_tradeoffs }",
        "topic": "hospital alarm fatigue governance and escalation design",
        "real_entity_guidance": "Answer from general clinical operations knowledge; named committees or studies are optional only if certain.",
    },
    {
        "anchor_id": "V6A003",
        "domain": "open_source_security",
        "domain_key": "open_source_security",
        "target": "{ Φ_package_quarantine_patterns, Φ_maintainer_burden, Φ_user_protection }",
        "topic": "open-source package quarantine and maintainer governance",
        "real_entity_guidance": "Answer at the governance-pattern level; do not require specific package incidents.",
    },
    {
        "anchor_id": "V6A004",
        "domain": "water_management",
        "domain_key": "water_management",
        "target": "{ Φ_drought_allocation_rules, Φ_sensor_uncertainty, Φ_public_trust }",
        "topic": "drought allocation decisions using sensor and forecast evidence",
        "real_entity_guidance": "Answer with policy and measurement patterns; named basin programs are optional only if certain.",
    },
    {
        "anchor_id": "V6A005",
        "domain": "financial_compliance",
        "domain_key": "financial_compliance",
        "target": "{ Φ_model_risk_controls, Φ_transaction_monitoring, Φ_auditability }",
        "topic": "model risk controls for transaction monitoring systems",
        "real_entity_guidance": "Answer using compliance-control patterns; do not require specific regulator notices.",
    },
    {
        "anchor_id": "V6A006",
        "domain": "education_technology",
        "domain_key": "education_technology",
        "target": "{ Φ_student_analytics_governance, Φ_parent_notice, Φ_algorithmic_appeals }",
        "topic": "school governance for student analytics systems",
        "real_entity_guidance": "Answer at framework level; named state bills or district policies are optional only if certain.",
    },
    {
        "anchor_id": "V6A007",
        "domain": "cloud_reliability",
        "domain_key": "cloud_reliability",
        "target": "{ Φ_incident_postmortem_patterns, Φ_retry_storm_controls, Φ_slo_tradeoffs }",
        "topic": "cloud service reliability controls for cascading retry failures",
        "real_entity_guidance": "Answer from SRE practice; named incidents are optional only if certain.",
    },
    {
        "anchor_id": "V6A008",
        "domain": "browser_security",
        "domain_key": "browser_security",
        "target": "{ Φ_cross_origin_isolation_patterns, Φ_site_data_boundaries, Φ_developer_tradeoffs }",
        "topic": "browser isolation controls for cross-origin data boundaries",
        "real_entity_guidance": "Answer from web security principles; exact standards are optional only if certain.",
    },
    {
        "anchor_id": "V6A009",
        "domain": "space_mission_assurance",
        "domain_key": "space_mission_assurance",
        "target": "{ Φ_fault_detection_patterns, Φ_autonomy_safing, Φ_ground_review_constraints }",
        "topic": "fault detection and autonomous safing in spacecraft operations",
        "real_entity_guidance": "Answer at mission-assurance pattern level; named missions are optional only if certain.",
    },
    {
        "anchor_id": "V6A010",
        "domain": "clinical_trials",
        "domain_key": "clinical_trials",
        "target": "{ Φ_endpoint_selection, Φ_interim_monitoring, Φ_patient_safety_tradeoffs }",
        "topic": "clinical-trial endpoint selection and interim monitoring",
        "real_entity_guidance": "Answer from trial-design principles; named trials are optional only if certain.",
    },
    {
        "anchor_id": "V6A011",
        "domain": "cyber_insurance",
        "domain_key": "cyber_insurance",
        "target": "{ Φ_risk_scoring_inputs, Φ_control_attestation, Φ_coverage_limitations }",
        "topic": "cyber-insurance risk scoring and control attestation",
        "real_entity_guidance": "Answer from underwriting patterns; named carrier forms are optional only if certain.",
    },
    {
        "anchor_id": "V6A012",
        "domain": "food_safety",
        "domain_key": "food_safety",
        "target": "{ Φ_traceability_patterns, Φ_recall_escalation, Φ_supplier_verification }",
        "topic": "food supply-chain traceability and recall escalation",
        "real_entity_guidance": "Answer from food-safety governance patterns; named recalls are optional only if certain.",
    },
    {
        "anchor_id": "V6A013",
        "domain": "energy_grid",
        "domain_key": "energy_grid",
        "target": "{ Φ_demand_response_controls, Φ_forecast_uncertainty, Φ_customer_fairness }",
        "topic": "electric-grid demand response under forecast uncertainty",
        "real_entity_guidance": "Answer with operational-control patterns; named pilots are optional only if certain.",
    },
    {
        "anchor_id": "V6A014",
        "domain": "labor_platforms",
        "domain_key": "labor_platforms",
        "target": "{ Φ_algorithmic_scheduling, Φ_worker_appeals, Φ_audit_logs }",
        "topic": "algorithmic scheduling governance in labor platforms",
        "real_entity_guidance": "Answer at governance-pattern level; named laws or lawsuits are optional only if certain.",
    },
    {
        "anchor_id": "V6A015",
        "domain": "telecom_resilience",
        "domain_key": "telecom_resilience",
        "target": "{ Φ_outage_reporting, Φ_backup_power_controls, Φ_priority_restoration }",
        "topic": "telecom outage resilience and backup-power governance",
        "real_entity_guidance": "Answer with resilience patterns; named FCC dockets are optional only if certain.",
    },
    {
        "anchor_id": "V6A016",
        "domain": "robotics_safety",
        "domain_key": "robotics_safety",
        "target": "{ Φ_workspace_hazard_controls, Φ_human_override, Φ_near_miss_review }",
        "topic": "industrial robotics safety controls around human workers",
        "real_entity_guidance": "Answer from safety-engineering patterns; named standards are optional only if certain.",
    },
    {
        "anchor_id": "V6A017",
        "domain": "public_health_surveillance",
        "domain_key": "public_health_surveillance",
        "target": "{ Φ_signal_detection, Φ_privacy_minimization, Φ_false_alarm_tradeoffs }",
        "topic": "public-health surveillance signal detection and privacy tradeoffs",
        "real_entity_guidance": "Answer at surveillance-design level; named systems are optional only if certain.",
    },
    {
        "anchor_id": "V6A018",
        "domain": "construction_safety",
        "domain_key": "construction_safety",
        "target": "{ Φ_site_risk_assessment, Φ_permit_controls, Φ_incident_learning }",
        "topic": "construction-site safety monitoring and permit controls",
        "real_entity_guidance": "Answer with safety-management patterns; named municipal programs are optional only if certain.",
    },
    {
        "anchor_id": "V6A019",
        "domain": "aviation_maintenance",
        "domain_key": "aviation_maintenance",
        "target": "{ Φ_maintenance_deferral_controls, Φ_inspection_evidence, Φ_safety_margin }",
        "topic": "aviation maintenance deferral and inspection evidence",
        "real_entity_guidance": "Answer from maintenance-control patterns; named airworthiness directives are optional only if certain.",
    },
    {
        "anchor_id": "V6A020",
        "domain": "environmental_monitoring",
        "domain_key": "environmental_monitoring",
        "target": "{ Φ_sensor_calibration, Φ_threshold_alerting, Φ_public_reporting }",
        "topic": "environmental sensor calibration and public alerting",
        "real_entity_guidance": "Answer at monitoring-pattern level; named stations or reports are optional only if certain.",
    },
    {
        "anchor_id": "V6A021",
        "domain": "election_administration",
        "domain_key": "election_administration",
        "target": "{ Φ_ballot_chain_of_custody, Φ_risk_limiting_audits, Φ_public_observability }",
        "topic": "election auditability and ballot chain-of-custody controls",
        "real_entity_guidance": "Answer from election-administration patterns; named county procedures are optional only if certain.",
    },
    {
        "anchor_id": "V6A022",
        "domain": "pharmaceutical_supply",
        "domain_key": "pharmaceutical_supply",
        "target": "{ Φ_shortage_forecasting, Φ_allocation_ethics, Φ_supplier_quality }",
        "topic": "pharmaceutical shortage forecasting and allocation governance",
        "real_entity_guidance": "Answer with supply-chain governance patterns; named shortages are optional only if certain.",
    },
    {
        "anchor_id": "V6A023",
        "domain": "insurance_claims",
        "domain_key": "insurance_claims",
        "target": "{ Φ_claim_triage_models, Φ_appeal_pathways, Φ_bias_monitoring }",
        "topic": "insurance-claims triage models and appeal governance",
        "real_entity_guidance": "Answer at claims-governance level; named proprietary systems are optional only if certain.",
    },
    {
        "anchor_id": "V6A024",
        "domain": "research_integrity",
        "domain_key": "research_integrity",
        "target": "{ Φ_image_screening, Φ_statistical_anomaly_review, Φ_correction_workflows }",
        "topic": "research-integrity screening and correction workflows",
        "real_entity_guidance": "Answer from research-integrity patterns; named tools or cases are optional only if certain.",
    },
]


def prompt_for(anchor: dict[str, str], named_count: int) -> str:
    fields = ", ".join(CONDITIONS[named_count]["fields"])
    return (
        "QUERY { "
        f"domain: {anchor['domain_key']}, "
        f"target: {anchor['target']}, "
        f"format: {{ {fields} }}, "
        "constraints: { answer_from_general_knowledge, do_not_invent, mark_uncertain_when_unsure }, "
        "exclude: { preamble, summary } "
        "}"
    )


def main() -> int:
    rows: list[dict[str, object]] = []
    for anchor in ANCHORS:
        for named_count, condition in CONDITIONS.items():
            prompt = prompt_for(anchor, named_count)
            for replicate in REPLICATES:
                rows.append(
                    {
                        "prompt_id": f"{anchor['anchor_id']}_N{named_count}_R{replicate}",
                        "anchor_id": anchor["anchor_id"],
                        "condition": condition["condition"],
                        "domain": anchor["domain"],
                        "topic": anchor["topic"],
                        "target": anchor["target"],
                        "replicate": replicate,
                        "named_slot_count": named_count,
                        "total_format_slots": TOTAL_FORMAT_SLOTS,
                        "format_fields": condition["fields"],
                        "false_anchor_removed": True,
                        "task_frame_removed": True,
                        "explicit_named_entity_exclusion": False,
                        "constant_uncertainty_constraint": True,
                        "length_matched_by_slot_count_design": True,
                        "expected_behavior": "dose_response_probe",
                        "fresh_for_v6": True,
                        "provenance": "v6_fresh_dose_response",
                        "real_entity_guidance": anchor["real_entity_guidance"],
                        "scoring_note": (
                            "Score fabricated named artifacts, fabricated identifiers, fabricated citations, "
                            "or unverifiable specific programs as hallucination-positive. Misrecalling a real "
                            "entity remains hallucination-negative and should be logged separately. The primary "
                            "V6 test is whether hallucination-positive rate increases with named_slot_count."
                        ),
                        "prompt": prompt,
                    }
                )
    OUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"wrote={OUT.relative_to(ROOT)} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
