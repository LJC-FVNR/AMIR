#!/usr/bin/env python3
"""Freeze held-out HotpotQA retrieval rows for hybrid calibration."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vw_rag.io_utils import load_jsonl, sha256_file, write_json, write_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-data", type=Path, required=True)
    parser.add_argument("--source-evaluation", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "data/hotpot_hybrid_calibration.jsonl"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = {str(row["example_id"]): row for row in load_jsonl(args.source_data)}
    evaluation = load_jsonl(args.source_evaluation)
    if len(evaluation) != 200:
        raise RuntimeError(f"Expected 200 held-out rows, found {len(evaluation)}")
    evaluation_ids = [str(row["example_id"]) for row in evaluation]
    if len(set(evaluation_ids)) != len(evaluation_ids):
        raise RuntimeError("Duplicate held-out HotpotQA IDs")
    source_order = [str(row["example_id"]) for row in load_jsonl(args.source_data)]
    calibration_ids = set(source_order[:50])
    if calibration_ids & set(evaluation_ids):
        raise RuntimeError("Hybrid calibration overlaps direction-fitting examples")

    rows = []
    for rank, example_id in enumerate(evaluation_ids, 1):
        row = source[example_id]
        documents = []
        for document in row["documents"]:
            item = dict(document)
            item["support_roles"] = []
            documents.append(item)
        rows.append(
            {
                "example_id": example_id,
                "source_split": row["source_split"],
                "split": "hybrid_calibration",
                "split_rank": rank,
                "question": row["question"],
                "answer": row["answer"],
                "answer_aliases": [],
                "depths": [10],
                "documents": documents,
                "retrieved_support_document_ids": list(row["support_document_ids"]),
                "direction_calibration_overlap": False,
            }
        )
    write_jsonl(args.output, rows)
    id_hash = hashlib.sha256(("\n".join(evaluation_ids) + "\n").encode()).hexdigest()
    write_json(
        args.output.with_suffix(".summary.json"),
        {
            "source_data": args.source_data.as_posix(),
            "source_data_sha256": sha256_file(args.source_data),
            "source_evaluation": args.source_evaluation.as_posix(),
            "source_evaluation_sha256": sha256_file(args.source_evaluation),
            "direction_calibration_examples": 50,
            "held_out_examples": 200,
            "direction_calibration_overlap": 0,
            "held_out_id_sha256": id_hash,
            "output_sha256": sha256_file(args.output),
        },
    )
    print(f"Wrote {len(rows)} held-out HotpotQA calibration rows")


if __name__ == "__main__":
    main()
