"""
ShadowNet Programming Department
File: programming_data.py

Purpose:
    Central catalogue and curriculum structure for the ShadowNet Programming
    Department. This is an additive file. It does not modify app.py or the
    existing database.

Content standard:
    This file defines the catalogue and a reusable lesson schema. Detailed
    language curricula should be added as separate, reviewed content modules.
    Do not treat a language as professionally covered merely because it appears
    in the catalogue.
"""

from __future__ import annotations

from copy import deepcopy


DEPARTMENT = {
    "name": "Programming Department",
    "brand": "ShadowNet",
    "version": "9.0",
    "description": (
        "A structured technical education library covering programming, "
        "software engineering, systems development, data, and specialist "
        "computing languages."
    ),
    "levels": [
        {
            "id": "beginner",
            "name": "Beginner",
            "description": (
                "Build reliable foundations: environment setup, syntax, "
                "types, expressions, control flow, and computational thinking."
            ),
        },
        {
            "id": "intermediate",
            "name": "Intermediate",
            "description": (
                "Develop maintainable programs using functions, collections, "
                "modules, files, APIs, error handling, and automated tests."
            ),
        },
        {
            "id": "advanced",
            "name": "Advanced",
            "description": (
                "Study algorithms, data structures, concurrency, architecture, "
                "performance, security, and complex software design."
            ),
        },
        {
            "id": "professional",
            "name": "Professional",
            "description": (
                "Apply production engineering practices through system design, "
                "reliability, observability, deployment, secure development, "
                "code review, and substantial industry-style projects."
            ),
        },
    ],
}


# Catalogue entries are grouped by the work a learner wants to perform.
# "kind" identifies languages that are not general-purpose programming
# languages, such as markup, query, and hardware-description languages.
CATEGORIES = [
    {
        "id": "general",
        "name": "General-purpose programming",
        "description": "Languages used to build a wide range of applications.",
        "languages": [
            ("python", "Python", "programming"),
            ("c", "C", "programming"),
            ("cpp", "C++", "programming"),
            ("csharp", "C#", "programming"),
            ("java", "Java", "programming"),
            ("javascript", "JavaScript", "programming"),
            ("typescript", "TypeScript", "programming"),
            ("go", "Go", "programming"),
            ("rust", "Rust", "programming"),
            ("ruby", "Ruby", "programming"),
            ("php", "PHP", "programming"),
            ("perl", "Perl", "programming"),
            ("r", "R", "programming"),
            ("julia", "Julia", "programming"),
            ("scala", "Scala", "programming"),
            ("kotlin", "Kotlin", "programming"),
            ("swift", "Swift", "programming"),
            ("dart", "Dart", "programming"),
            ("objective-c", "Objective-C", "programming"),
            ("vbnet", "Visual Basic .NET", "programming"),
            ("fsharp", "F#", "programming"),
            ("groovy", "Groovy", "programming"),
            ("lua", "Lua", "programming"),
            ("d", "D", "programming"),
            ("zig", "Zig", "programming"),
            ("nim", "Nim", "programming"),
            ("crystal", "Crystal", "programming"),
            ("ocaml", "OCaml", "programming"),
            ("haskell", "Haskell", "programming"),
            ("elixir", "Elixir", "programming"),
            ("erlang", "Erlang", "programming"),
            ("clojure", "Clojure", "programming"),
            ("common-lisp", "Common Lisp", "programming"),
            ("scheme", "Scheme", "programming"),
            ("prolog", "Prolog", "programming"),
            ("fortran", "Fortran", "programming"),
            ("cobol", "COBOL", "programming"),
            ("pascal", "Pascal", "programming"),
            ("ada", "Ada", "programming"),
            ("assembly", "Assembly", "low-level"),
        ],
    },
    {
        "id": "web",
        "name": "Web development",
        "description": "Browser, server, and web-platform technologies.",
        "languages": [
            ("html", "HTML", "markup"),
            ("css", "CSS", "stylesheet"),
            ("javascript", "JavaScript", "programming"),
            ("typescript", "TypeScript", "programming"),
            ("php", "PHP", "programming"),
            ("python", "Python", "programming"),
            ("ruby", "Ruby", "programming"),
            ("java", "Java", "programming"),
            ("go", "Go", "programming"),
            ("sql", "SQL", "query"),
            ("graphql", "GraphQL", "query"),
            ("wasm", "WebAssembly", "runtime"),
        ],
    },
    {
        "id": "mobile",
        "name": "Mobile application development",
        "description": "Languages used for Android, iOS, and cross-platform apps.",
        "languages": [
            ("kotlin", "Kotlin", "programming"),
            ("java", "Java", "programming"),
            ("swift", "Swift", "programming"),
            ("objective-c", "Objective-C", "programming"),
            ("dart", "Dart", "programming"),
            ("javascript", "JavaScript", "programming"),
            ("typescript", "TypeScript", "programming"),
            ("csharp", "C#", "programming"),
        ],
    },
    {
        "id": "systems",
        "name": "Systems and low-level development",
        "description": "Operating systems, runtimes, memory, and performance-sensitive software.",
        "languages": [
            ("c", "C", "programming"),
            ("cpp", "C++", "programming"),
            ("rust", "Rust", "programming"),
            ("assembly", "Assembly", "low-level"),
            ("zig", "Zig", "programming"),
            ("d", "D", "programming"),
            ("ada", "Ada", "programming"),
            ("fortran", "Fortran", "programming"),
        ],
    },
    {
        "id": "data-ai",
        "name": "Data science and artificial intelligence",
        "description": "Statistical computing, data processing, and machine learning.",
        "languages": [
            ("python", "Python", "programming"),
            ("r", "R", "programming"),
            ("julia", "Julia", "programming"),
            ("sql", "SQL", "query"),
            ("scala", "Scala", "programming"),
            ("matlab", "MATLAB", "technical"),
            ("mojo", "Mojo", "programming"),
        ],
    },
    {
        "id": "cybersecurity",
        "name": "Cybersecurity and automation",
        "description": "Scripting, secure tooling, automation, and systems analysis.",
        "languages": [
            ("python", "Python", "programming"),
            ("bash", "Bash", "shell"),
            ("powershell", "PowerShell", "shell"),
            ("javascript", "JavaScript", "programming"),
            ("ruby", "Ruby", "programming"),
            ("go", "Go", "programming"),
            ("c", "C", "programming"),
            ("cpp", "C++", "programming"),
            ("assembly", "Assembly", "low-level"),
            ("lua", "Lua", "programming"),
        ],
    },
    {
        "id": "databases",
        "name": "Database and query languages",
        "description": "Relational, procedural, graph, and data-query technologies.",
        "languages": [
            ("sql", "SQL", "query"),
            ("plsql", "PL/SQL", "procedural-query"),
            ("tsql", "T-SQL", "procedural-query"),
            ("plpgsql", "PL/pgSQL", "procedural-query"),
            ("graphql", "GraphQL", "query"),
            ("cypher", "Cypher", "query"),
            ("sparql", "SPARQL", "query"),
        ],
    },
    {
        "id": "game-development",
        "name": "Game development",
        "description": "Languages used in game engines, gameplay systems, and graphics.",
        "languages": [
            ("cpp", "C++", "programming"),
            ("csharp", "C#", "programming"),
            ("gdscript", "GDScript", "programming"),
            ("lua", "Lua", "programming"),
            ("javascript", "JavaScript", "programming"),
            ("java", "Java", "programming"),
            ("rust", "Rust", "programming"),
        ],
    },
    {
        "id": "functional",
        "name": "Functional and declarative programming",
        "description": "Functional paradigms, immutable data, and declarative problem solving.",
        "languages": [
            ("haskell", "Haskell", "programming"),
            ("elixir", "Elixir", "programming"),
            ("erlang", "Erlang", "programming"),
            ("clojure", "Clojure", "programming"),
            ("fsharp", "F#", "programming"),
            ("ocaml", "OCaml", "programming"),
            ("scala", "Scala", "programming"),
            ("common-lisp", "Common Lisp", "programming"),
            ("scheme", "Scheme", "programming"),
            ("prolog", "Prolog", "programming"),
        ],
    },
    {
        "id": "embedded-hardware",
        "name": "Embedded systems and hardware description",
        "description": "Firmware, microcontrollers, digital logic, and hardware design.",
        "languages": [
            ("c", "C", "programming"),
            ("cpp", "C++", "programming"),
            ("rust", "Rust", "programming"),
            ("assembly", "Assembly", "low-level"),
            ("micropython", "MicroPython", "programming"),
            ("verilog", "Verilog", "hardware-description"),
            ("vhdl", "VHDL", "hardware-description"),
            ("systemverilog", "SystemVerilog", "hardware-description"),
        ],
    },
    {
        "id": "specialist",
        "name": "Specialist and emerging technologies",
        "description": "Domain-specific languages and specialised computing environments.",
        "languages": [
            ("solidity", "Solidity", "programming"),
            ("vyper", "Vyper", "programming"),
            ("move", "Move", "programming"),
            ("qsharp", "Q#", "programming"),
            ("scratch", "Scratch", "visual"),
            ("processing", "Processing", "programming"),
            ("glsl", "GLSL", "shader"),
            ("hlsl", "HLSL", "shader"),
            ("wasm", "WebAssembly", "runtime"),
        ],
    },
]


def _build_language_index():
    """Create a unique language index while preserving first-seen order."""
    index = {}
    for category in CATEGORIES:
        for slug, name, kind in category["languages"]:
            if slug not in index:
                index[slug] = {
                    "slug": slug,
                    "name": name,
                    "kind": kind,
                    "categories": [],
                    "levels": [level["id"] for level in DEPARTMENT["levels"]],
                    "status": "catalogued",
                    "curriculum_complete": False,
                }
            if category["id"] not in index[slug]["categories"]:
                index[slug]["categories"].append(category["id"])
    return index


LANGUAGES = _build_language_index()


# Curriculum module contract. Use this structure for every lesson.
# A lesson is not complete until its explanations, examples, lab, assessment,
# solutions, common errors, and references have been authored and reviewed.
LESSON_SCHEMA = {
    "id": "unique-lesson-id",
    "title": "Specific technical topic",
    "level": "beginner",
    "estimated_minutes": 45,
    "learning_objectives": [],
    "prerequisites": [],
    "notes": {
        "concept": "",
        "how_it_works": "",
        "why_it_matters": "",
        "technical_details": [],
    },
    "examples": [
        {
            "title": "",
            "purpose": "",
            "code": "",
            "walkthrough": [],
            "expected_result": "",
        }
    ],
    "practical_lab": {
        "scenario": "",
        "requirements": [],
        "tasks": [],
        "acceptance_criteria": [],
        "solution": "",
    },
    "common_mistakes": [
        {
            "mistake": "",
            "cause": "",
            "fix": "",
        }
    ],
    "assessment": [
        {
            "question": "",
            "answer": "",
            "explanation": "",
        }
    ],
    "references": [],
    "review_status": "draft",
}


# A complete curriculum is maintained per language. Empty curricula are
# intentionally marked as not yet authored instead of displaying fake lessons.
CURRICULA = {
    slug: {
        "language": slug,
        "levels": {
            level["id"]: {
                "title": f"{language['name']} {level['name']}",
                "lessons": [],
                "status": "not-authored",
            }
            for level in DEPARTMENT["levels"]
        },
    }
    for slug, language in LANGUAGES.items()
}


def get_catalogue():
    """Return a safe copy of the complete department catalogue."""
    return {
        "department": deepcopy(DEPARTMENT),
        "categories": deepcopy(CATEGORIES),
        "languages": deepcopy(list(LANGUAGES.values())),
    }


def search_languages(query):
    """Search language names, identifiers, and category identifiers."""
    term = (query or "").strip().casefold()
    if not term:
        return deepcopy(list(LANGUAGES.values()))

    matches = []
    for language in LANGUAGES.values():
        searchable = " ".join(
            [language["name"], language["slug"], *language["categories"]]
        ).casefold()
        if term in searchable:
            matches.append(deepcopy(language))
    return matches


def get_language(slug):
    """Return one language entry, or None if the slug is unknown."""
    language = LANGUAGES.get((slug or "").strip().casefold())
    return deepcopy(language) if language else None


def get_curriculum(slug):
    """Return a language curriculum, or None if the language is unknown."""
    curriculum = CURRICULA.get((slug or "").strip().casefold())
    return deepcopy(curriculum) if curriculum else None


__all__ = [
    "DEPARTMENT",
    "CATEGORIES",
    "LANGUAGES",
    "LESSON_SCHEMA",
    "CURRICULA",
    "get_catalogue",
    "search_languages",
    "get_language",
    "get_curriculum",
]
