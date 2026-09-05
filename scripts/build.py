"""Build a static homepage from content.toml (Python 3.11+, standard library only)."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, unquote
import argparse
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def text(value):
    return escape(str(value), quote=True)


def inline(value):
    # Support bold text and Markdown links; always escape raw HTML.
    def bold(part):
        return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text(part))

    result = []
    offset = 0
    for match in re.finditer(r'\[([^\]\n]+)\]\(([^\s()]+)\)', str(value)):
        result.append(bold(str(value)[offset:match.start()]))
        address = url(match[2], ROOT)
        result.append(f'<a href="{address}">{bold(match[1])}</a>')
        offset = match.end()
    result.append(bold(str(value)[offset:]))
    return ''.join(result)


def paragraphs(value):
    return ''.join('<p>' + inline(p).replace('\n', '<br>') + '</p>'
                   for p in re.split(r'\n\s*\n', value.strip()) if p.strip())


def url(value, root, image=False):
    if not isinstance(value, str):
        raise ValueError('URL must be quoted text')
    if not value:
        return ''
    if any(c.isspace() or ord(c) < 32 for c in value) or '\\' in value:
        raise ValueError(f'URL contains whitespace or backslashes: {value!r}')
    parts = urlsplit(value)
    if parts.scheme:
        allowed = ('https', 'http') if image else ('https', 'http', 'mailto')
        if parts.scheme not in allowed:
            raise ValueError(f'Unsupported URL scheme: {value}')
        if parts.scheme in ('https', 'http') and not parts.netloc:
            raise ValueError(f'URL is missing a hostname: {value}')
    else:
        path = unquote(parts.path)
        if parts.netloc or path.startswith('/') or '\\' in path or '..' in Path(path).parts:
            raise ValueError(f'Use a relative assets/ or files/ path: {value}')
        if not path.startswith(('assets/', 'files/')):
            raise ValueError(f'Local links must point into assets/ or files/: {value}')
        target = (root / path).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f'Local file does not exist: {value}')
    return text(value)


def render(data, template, root=ROOT):
    s, p, labels = data['site'], data['profile'], data['labels']
    sections = [k for k in ('publications', 'education', 'experience', 'teaching', 'honors', 'notes') if data.get(k)]
    nav = '<a href="#profile">' + text(labels['about']) + '</a>'
    nav += ''.join(f'<a href="#{key}">{text(labels[key])}</a>' for key in sections)

    def links(items, contact=False):
        result = []
        for item in items:
            address = url(item.get('url', ''), root)
            label = text(item['label'])
            if address:
                result.append(f'<a href="{address}">{label} ↗</a>')
            elif contact:
                result.append(f'<span>{label} <small>↗</small></span>')
            else:
                result.append(f'<span class="pending">{label} · {text(labels["coming_soon"])}</span>')
        return ''.join(result)

    photo = url(p.get('photo', ''), root, image=True)
    portrait = (f'<img class="portrait" src="{photo}" alt="{text(p["name"])}">' if photo else
                f'<div class="portrait placeholder"><span class="monogram" aria-hidden="true">{text(p["initials"])}</span><span>{text(labels["portrait"])}</span></div>')
    local_name = f'<span>{text(p["name_local"])}</span>' if p.get('name_local') else ''
    main = f'''<section id="profile" class="profile" aria-labelledby="profile-heading">
<div class="profile-copy"><p class="eyebrow">{text(labels['eyebrow'])}</p>
<h1 id="profile-heading">{text(p['name'])} {local_name}</h1>
<p class="affiliation">{text(p['role'])}<br><span>{text(p['affiliation'])}</span></p>
<div class="contact-links">{links(data.get('contacts', []), True)}</div>
<div class="bio">{paragraphs(p['bio'])}</div></div>
<aside class="profile-aside">{portrait}<p class="aside-label">{text(labels['interests'])}</p>
<ul class="interests">{''.join('<li>'+text(i)+'</li>' for i in p['interests'])}</ul></aside></section>'''
    for number, key in enumerate(sections, 1):
        main += f'<section id="{key}" class="section" aria-labelledby="{key}-heading"><div class="section-heading"><h2 id="{key}-heading">{text(labels[key])}</h2><span class="section-number">{number:02}</span></div>'
        if key == 'publications':
            main += f'<p class="section-note">{text(labels["publications_note"])}</p>'
            groups = {}
            for item in data[key]:
                groups.setdefault(item['group'], []).append(item)
            index = 0
            for group, papers in groups.items():
                main += f'<h3 class="research-group">{text(group)}</h3>'
                for paper in papers:
                    index += 1
                    neutral = paper.get('neutral', False)
                    if not isinstance(neutral, bool):
                        raise ValueError('publications.neutral must be true or false, without quotes')
                    badge = 'badge neutral' if neutral else 'badge'
                    main += f'''<article class="paper"><div class="paper-index">{index:02}</div><div class="paper-content">
<p class="paper-meta">{text(paper['year'])} <span class="{badge}">{text(paper['venue'])}</span></p>
<h4>{text(paper['title'])}</h4><p class="authors">{inline(paper['authors'])}</p>'''
                    if paper.get('summary', '').strip():
                        main += f'<p class="paper-description">{inline(paper["summary"])}</p>'
                    main += f'<div class="paper-links">{links(paper.get("links", []))}</div>'
                    if paper.get('abstract', '').strip():
                        main += f'<details><summary>{text(labels["abstract"])}</summary>{paragraphs(paper["abstract"])}</details>'
                    main += '</div></article>'
        elif key in ('education', 'experience', 'teaching'):
            main += '<div class="timeline">'
            for item in data[key]:
                main += f'''<article class="timeline-entry"><p class="date">{text(item['dates'])}</p><div>
<h3>{text(item['institution'])}</h3><p>{text(item['role'])}</p><p class="muted">{inline(item.get('description', ''))}</p></div></article>'''
            main += '</div>'
        elif key == 'honors':
            main += '<ul class="awards">' + ''.join(f'<li><span>{text(i["title"])}</span><span>{text(i["year"])}</span></li>' for i in data[key]) + '</ul>'
        elif key == 'notes':
            for item in data[key]:
                address = url(item.get('url', ''), root)
                title = text(item['title'])
                if address:
                    title = f'<a href="{address}">{title} ↗</a>'
                main += f'<div class="note-entry"><div><h3>{title}</h3><p class="muted">{inline(item.get("description", ""))}</p></div><span class="pending">{text(item.get("status", ""))}</span></div>'
        main += '</section>'
    main += f'<footer><p>© {text(p["name"])} <span>·</span> {text(labels["updated"])}: {text(s["updated"])}</p><a href="#profile">{text(labels["back_to_top"])}</a></footer>'
    values = dict(MAIN=main, TITLE=text(s['title']), DESCRIPTION=text(s['description']), LANG=text(s['lang']), NAME=text(p['name']), WORDMARK=text(labels['wordmark']), NAV=nav)
    return re.sub(r'@@([A-Z]+)@@', lambda m: values[m[1]], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content', type=Path, default=ROOT / 'content.toml')
    parser.add_argument('--output', type=Path, default=ROOT / 'index.html')
    args = parser.parse_args()
    try:
        data = tomllib.loads(args.content.read_text(encoding='utf-8-sig'))
        html = render(data, (ROOT / 'templates/page.html').read_text(encoding='utf-8'))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding='utf-8')
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        print(f'Build failed: check {args.content}\n{error}', file=sys.stderr)
        return 1
    print(f'Generated {args.output} from {args.content}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
