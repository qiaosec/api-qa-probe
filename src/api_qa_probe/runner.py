import json

from .loader import load_cases


def resolve_path(body: dict, path: str):
    current = body
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(path)
        current = current[part]
    return current


def evaluate_case(case: dict) -> dict:
    failures: list[str] = []
    response = case["response"]
    body = response.get("body", {})

    if response.get("status_code") != case["expected_status"]:
        failures.append(
            f"expected status {case['expected_status']} but got {response.get('status_code')}"
        )

    for field in case.get("required_fields", []):
        try:
            resolve_path(body, field)
        except KeyError:
            failures.append(f"missing required field: {field}")

    for assertion in case.get("assertions", []):
        path = assertion["path"]
        expected = assertion["equals"]
        try:
            actual = resolve_path(body, path)
        except KeyError:
            failures.append(f"assertion path not found: {path}")
            continue
        if actual != expected:
            failures.append(f"assertion failed for {path}: expected {expected!r}, got {actual!r}")

    return {
        "case_id": case["case_id"],
        "name": case["name"],
        "passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }


def run_cases(path: str) -> dict:
    cases = load_cases(path)
    results = [evaluate_case(case) for case in cases]
    passed = sum(1 for item in results if item["passed"])
    failed = len(results) - passed
    failing_cases = [item for item in results if not item["passed"]]

    return {
        "summary": {
            "total_cases": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": round((passed / len(results)) * 100, 2) if results else 0.0,
        },
        "failing_cases": failing_cases,
        "results": results,
    }


def to_json_report(report: dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)


def to_markdown_report(report: dict) -> str:
    lines = [
        "# API QA Report",
        "",
        "## Summary",
        "",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Pass rate: {report['summary']['pass_rate']}%",
        "",
        "## Failing Cases",
        "",
    ]

    if not report["failing_cases"]:
        lines.append("- None")
    else:
        for item in report["failing_cases"]:
            lines.append(f"- {item['case_id']} | {item['name']}")
            for failure in item["failures"]:
                lines.append(f"  - {failure}")

    lines.extend(["", "## All Results", ""])
    for item in report["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        lines.append(f"- {item['case_id']} | {item['name']} | {status}")

    return "\n".join(lines)
