"""Workflow exports must parse, and they must not carry a secret."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "workflows"

# Raw keys and tokens. An n8n credential id is not this shape.
SECRET = re.compile(
    r"sk-ant-|sk-proj-|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    r"|ghp_[A-Za-z0-9]|github_pat_|xox[baprs]-"
    r"|AIza[0-9A-Za-z_\-]{20,}"
    r"|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"
    r"|Bearer [A-Za-z0-9._\-]{12,}"
)

SENSITIVE = {
    "apikey",
    "api_key",
    "accesstoken",
    "access_token",
    "secret",
    "password",
    "token",
    "authorization",
    "privatekey",
    "private_key",
    "clientsecret",
    "client_secret",
}


def _expression(value: str) -> bool:
    text = value.strip()
    return text.startswith("=") or text.startswith("{{") or "$env." in text or "$secrets." in text


class WorkflowJsonTest(unittest.TestCase):
    def test_workflows_parse_without_embedded_credentials(self) -> None:
        paths = sorted(WORKFLOWS.glob("*.json"))
        self.assertGreater(len(paths), 0, "expected workflow JSON under workflows/")
        for path in paths:
            with self.subTest(file=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsInstance(data, dict)
                self._walk(path.name, data, ())

    def _walk(self, filename: str, node: object, path: tuple[str, ...]) -> None:
        if isinstance(node, dict):
            if path and path[-1] == "credentials":
                self._check_credential_refs(filename, node)
            for key, value in node.items():
                self._check_sensitive(filename, key, value, path)
                self._walk(filename, value, path + (key,))
            return
        if isinstance(node, list):
            for index, value in enumerate(node):
                self._walk(filename, value, path + (str(index),))
            return
        if isinstance(node, str) and SECRET.search(node):
            self.fail(f"{filename} has an embedded credential at {'.'.join(path)}")

    def _check_credential_refs(self, filename: str, node: dict) -> None:
        for cred in node.values():
            self.assertIsInstance(cred, dict, f"{filename} credential reference is not an object")
            extra = set(cred) - {"id", "name"}
            self.assertFalse(
                extra,
                f"{filename} credential reference has fields other than id and name",
            )
            for field in ("id", "name"):
                if field in cred:
                    self.assertIsInstance(
                        cred[field],
                        str,
                        f"{filename} credential {field} is not text",
                    )

    def _check_sensitive(
        self,
        filename: str,
        key: str,
        value: object,
        path: tuple[str, ...],
    ) -> None:
        if key.lower() not in SENSITIVE or not isinstance(value, str):
            return
        text = value.strip()
        if not text or _expression(text):
            return
        where = ".".join(path + (key,))
        self.fail(f"{filename} has an embedded credential at {where}")


if __name__ == "__main__":
    unittest.main()
