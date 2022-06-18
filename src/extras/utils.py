from django.template.loader import render_to_string


def render_tag(name, content=None, closing_tag=False, **attrs):
    """Return HTML code for rendering a tag."""
    return render_to_string(
        template_name="extras/snippets/tag.html",
        context={
            "name": name,
            "closing_tag": closing_tag,
            "content": content,
            "attrs": attrs,
        },
    ).strip()


def render_link_tag(href, content=None, **attrs):
    """Return HTML code for rendering anchor tag."""

    return render_tag(
        name="a",
        closing_tag=True,
        content=content,
        **{"href": href, **attrs},
    )
