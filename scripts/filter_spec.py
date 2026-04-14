#!/usr/bin/env python3
"""Filter an OpenAPI spec to only include specified operations.

Usage: filter_spec.py <spec.yml> <op1> <op2> ... > filtered.yml

Operations are matched by operationId. Keeps all schemas referenced
by the included operations.
"""

import sys

import yaml


def find_refs(obj: object) -> dict[str, set[str]]:
    """Recursively find all $ref names, grouped by component type."""
    refs: dict[str, set[str]] = {}
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref = obj["$ref"]
            if ref.startswith("#/components/"):
                parts = ref.split("/")  # ['#', 'components', 'schemas', 'Name']
                kind, name = parts[2], parts[3]
                refs.setdefault(kind, set()).add(name)
        for v in obj.values():
            for kind, names in find_refs(v).items():
                refs.setdefault(kind, set()).update(names)
    elif isinstance(obj, list):
        for item in obj:
            for kind, names in find_refs(item).items():
                refs.setdefault(kind, set()).update(names)
    return refs


def resolve_deps(components: dict, kind: str, names: set[str]) -> set[str]:
    """Transitively resolve all dependencies within a component type."""
    section = components.get(kind, {})
    resolved: set[str] = set()
    queue = list(names)
    while queue:
        name = queue.pop()
        if name in resolved or name not in section:
            continue
        resolved.add(name)
        for dep_kind, dep_names in find_refs(section[name]).items():
            if dep_kind == kind:
                queue.extend(dep_names - resolved)
    return resolved


def filter_spec(spec: dict, operation_ids: set[str]) -> dict:
    """Return a new spec with only the specified operations."""
    filtered_paths: dict = {}
    all_refs: dict[str, set[str]] = {}

    for path, methods in spec.get("paths", {}).items():
        kept_methods: dict = {}
        for method, operation in methods.items():
            if method in ("parameters", "summary", "description"):
                continue
            if isinstance(operation, dict) and operation.get("operationId") in operation_ids:
                kept_methods[method] = operation
                for kind, names in find_refs(operation).items():
                    all_refs.setdefault(kind, set()).update(names)
        if kept_methods:
            if "parameters" in methods:
                kept_methods["parameters"] = methods["parameters"]
                for kind, names in find_refs(methods["parameters"]).items():
                    all_refs.setdefault(kind, set()).update(names)
            filtered_paths[path] = kept_methods

    # Resolve transitive deps for each component type
    components = spec.get("components", {})
    filtered_components: dict = {}
    for kind, names in all_refs.items():
        section = components.get(kind, {})
        needed = resolve_deps(components, kind, names)
        if needed:
            filtered_components[kind] = {k: v for k, v in section.items() if k in needed}

    # Always keep securitySchemes if present
    if "securitySchemes" in components:
        filtered_components["securitySchemes"] = components["securitySchemes"]

    result = {
        "openapi": spec["openapi"],
        "info": spec["info"],
        "tags": spec.get("tags", []),
        "paths": filtered_paths,
    }
    if filtered_components:
        result["components"] = filtered_components
    if "security" in spec:
        result["security"] = spec["security"]

    return result


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <spec.yml> <op1> [op2] ...", file=sys.stderr)
        sys.exit(1)

    spec_path = sys.argv[1]
    ops = set(sys.argv[2:])

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    filtered = filter_spec(spec, ops)
    yaml.dump(filtered, sys.stdout, default_flow_style=False, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    main()
