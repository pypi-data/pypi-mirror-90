from xml.etree import ElementTree

from markdown.inlinepatterns import InlineProcessor

LINK_PATTERN = r'\[([^|]+)\|https?://(.*?)\]'


class LinkProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        a = ElementTree.Element('a')
        print(m.groups())
        a.set('href', 'https://' + m.group(2))
        a.text = m.group(1)
        return a, m.start(0), m.end(0)


link_processor = LinkProcessor(LINK_PATTERN)
