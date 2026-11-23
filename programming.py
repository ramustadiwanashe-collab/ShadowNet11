"""
ShadowNet Programming Department
File: programming.py

Flask Blueprint for the Programming Department.
Keep this file beside app.py and programming_data.py.

This module does not create or modify database tables. It adds catalogue
routes only. Register the blueprint in app.py when the integration step is
ready:

    from programming import programming_bp
    app.register_blueprint(programming_bp)

Required templates:
    templates/programming/index.html
    templates/programming/language.html
"""

from flask import Blueprint, abort, render_template, request

try:
    from programming_data import (
        DEPARTMENT,
        CATEGORIES,
        LANGUAGES,
        get_catalogue,
        get_language,
        get_curriculum,
        search_languages,
    )
except ImportError:
    # Supports package-style imports if the project is later reorganised.
    from .programming_data import (
        DEPARTMENT,
        CATEGORIES,
        LANGUAGES,
        get_catalogue,
        get_language,
        get_curriculum,
        search_languages,
    )


programming_bp = Blueprint(
    "programming",
    __name__,
    url_prefix="/programming",
)


@programming_bp.get("/")
def programming_home():
    """Show the searchable Programming Department catalogue."""
    query = request.args.get("q", "").strip()
    catalogue = get_catalogue()

    if query:
        languages = search_languages(query)
        matching_slugs = {item["slug"] for item in languages}
        categories = [
            category
            for category in catalogue["categories"]
            if any(
                language[0] in matching_slugs
                for language in category["languages"]
            )
        ]
    else:
        languages = catalogue["languages"]
        categories = catalogue["categories"]

    return render_template(
        "programming/index.html",
        department=DEPARTMENT,
        categories=categories,
        languages=languages,
        search_query=query,
        language_count=len(LANGUAGES),
    )


@programming_bp.get("/<slug>")
def programming_language(slug):
    """Show a language overview and its authored curriculum status."""
    language = get_language(slug)

    if language is None:
        abort(404)

    curriculum = get_curriculum(slug)

    return render_template(
        "programming/language.html",
        department=DEPARTMENT,
        language=language,
        curriculum=curriculum,
    )


@programming_bp.get("/level/<slug>/<level_id>")
def programming_level(slug, level_id):
    """
    Show a level's lessons once its curriculum content has been authored.

    This route deliberately does not fabricate lesson content. It returns
    404 until a curriculum module contains lessons for the requested level.
    """
    language = get_language(slug)
    curriculum = get_curriculum(slug)

    valid_levels = {level["id"] for level in DEPARTMENT["levels"]}

    if language is None or curriculum is None or level_id not in valid_levels:
        abort(404)

    level = curriculum["levels"].get(level_id)

    if not level or not level.get("lessons"):
        abort(404)

    return render_template(
        "programming/level.html",
        department=DEPARTMENT,
        language=language,
        level=level,
        level_id=level_id,
    )
