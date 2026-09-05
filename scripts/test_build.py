import copy
import importlib.util
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT/'scripts/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.data = tomllib.loads((ROOT/'content.toml').read_text(encoding='utf-8-sig'))
        self.template = (ROOT/'templates/page.html').read_text(encoding='utf-8')

    def render(self):
        return build.render(self.data, self.template)

    def test_structure_and_navigation(self):
        html = self.render()
        ids = re.findall(r'\bid="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)))
        for target in re.findall(r'href="#([^"]+)"', html):
            self.assertIn(target, ids)
        self.assertEqual(html.count('class="paper"'), len(self.data['publications']))
        self.assertNotIn('@@MAIN@@', html)
        self.assertEqual(self.render(), html)

    def test_text_edits_and_escaping(self):
        self.data['profile']['name'] = '陈 & <Research> "Name"'
        self.data['profile']['bio'] = '第一段 **重点**\n\n第二段 <script>alert(1)</script>'
        html = self.render()
        self.assertIn('陈 &amp; &lt;Research&gt; &quot;Name&quot;', html)
        self.assertIn('<p>第一段 <strong>重点</strong></p><p>第二段', html)
        self.assertNotIn('<script>', html)

    def test_add_and_remove_entries(self):
        paper = copy.deepcopy(self.data['publications'][0])
        paper['title'] = 'New publication'
        paper['abstract'] = ''
        self.data['publications'].append(paper)
        self.data.pop('honors')
        html = self.render()
        self.assertEqual(html.count('class="paper"'), len(self.data['publications']))
        self.assertEqual(html.count('<details>'), sum(bool(p.get('abstract', '').strip()) for p in self.data['publications']))
        self.assertNotIn('href="#honors"', html)
        self.assertNotIn('id="honors"', html)

    def test_links_and_local_assets(self):
        self.data['contacts'][0]['url'] = 'mailto:you@example.edu'
        self.data['notes'][0]['url'] = 'assets/favicon.svg'
        html = self.render()
        self.assertIn('href="mailto:you@example.edu"', html)
        self.assertIn('href="assets/favicon.svg"', html)
        self.assertNotIn('href=""', html)
        self.assertIn('Google Scholar', html)

    def test_invalid_links_fail(self):
        for invalid in ('javascript:alert(1)', '/assets/x.jpg', '../README.md', 'files/missing.pdf', 'assets/../../README.md'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                build.url(invalid, ROOT)

    def test_invalid_toml_and_boolean_fail(self):
        with self.assertRaises(tomllib.TOMLDecodeError):
            tomllib.loads('[profile]\nname = "unterminated')
        self.data['publications'][0]['neutral'] = 'false'
        with self.assertRaises(ValueError):
            self.render()

if __name__ == '__main__':
    unittest.main()
