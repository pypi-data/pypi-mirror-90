from docutils.nodes import Element
from sphinx.util.docutils import SphinxDirective

from .iframe import IFrameNode


def setup(app):
    app.add_directive('youtube', Youtube)
    app.add_node(VideoNode,
                 html=(visit_video_html, depart_video_html),
                 latex=(visit_video_latex, depart_video_latex),)
    app.add_node(PlayerNode,
                 html=(visit_player_html, depart_player_html),
                 latex=(visit_player_latex, depart_player_latex),)
    app.add_node(TranscriptNode,
                 html=(visit_transcript_html, depart_transcript_html),
                 latex=(visit_transcript_latex, depart_transcript_latex),)


class VideoNode(Element):
    """The VideoNode contains the PlayerNode and TranscriptNode that together make up the video."""

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('video')


def visit_video_html(self, node):
    self.body.append(self.starttag(node, 'div'))


def depart_video_html(self, node):
    self.body.append('</div>')


def visit_video_latex(self, node):
    pass


def depart_video_latex(self, node):
    pass


class PlayerNode(Element):
    """The PlayerNode represents the video player."""

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('player')


def visit_player_html(self, node):
    self.body.append(self.starttag(node, 'div'))


def depart_player_html(self, node):
    self.body.append('</div>')


def visit_player_latex(self, node):
    pass


def depart_player_latex(self, node):
    pass


class TranscriptNode(Element):
    """The TranscriptNode represents the transcript of a video."""

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('transcript')


def visit_transcript_html(self, node):
    self.body.append(self.starttag(node, 'div'))
    self.body.append('<div class="buttons">')
    self.body.append('<button><span>Show transcript</span><span>Hide transcript</span></button>')
    self.body.append('</div>')
    self.body.append('<div class="content">')


def depart_transcript_html(self, node):
    self.body.append('</div>')
    self.body.append('</div>')


def visit_transcript_latex(self, node):
    self.body.append('\n')


def depart_transcript_latex(self, node):
    pass


class Youtube(SphinxDirective):
    """The Youtube directive supports embedding of YouTube videos.

    :param argument: The identifier of the YouTube video to embed
    :param width: Optional width for the video iframe
    :param height: Optional height for the video iframe
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'width': int,
                   'height': int}

    def run(self):
        video = VideoNode()
        player = PlayerNode()
        video += player
        iframe = IFrameNode()
        player += iframe
        iframe['source'] = f'https://www.youtube.com/embed/{self.arguments[0]}'
        if 'width' in self.options:
            iframe['width'] = self.options['width']
        if 'height' in self.options:
            iframe['height'] = self.options['height']
        if self.content:
            transcript = TranscriptNode()
            video += transcript
            self.state.nested_parse(self.content, self.content_offset, transcript)
        return [video]
