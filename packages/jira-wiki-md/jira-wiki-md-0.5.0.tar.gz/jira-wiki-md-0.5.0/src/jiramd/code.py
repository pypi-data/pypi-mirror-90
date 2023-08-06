from typing import List

from markdown.preprocessors import Preprocessor
from markdown.util import code_escape

CODE_PATTERN = r'\{code\}(.+?)\{code\}'


class CodeProcessor(Preprocessor):
    def run(self, lines: List[str]) -> List[str]:
        text = '\n'.join(lines)
        while text.count('{code}') >= 2:
            before, _, tail = text.partition('{code}')
            inside, _, after = tail.partition('{code}')
            text = '{}<pre><code>{}</code></pre>{}'.format(before, code_escape(inside), after)
        return text.split('\n')


code_processor = CodeProcessor()
