# ------------------------------------------------------------------------------
# This extension adds support for shortcodes.
# ------------------------------------------------------------------------------

import ivy
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# Use a single parser instance to parse all files.
parser = None


# The shortcodes module is an optional dependency.
if shortcodes:

    @ivy.filters.register('node_text')
    def render(text, node):
        global parser
        if parser is None:
            settings = ivy.site.config.get('shortcodes', {})
            parser = shortcodes.Parser(**settings)

        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as err:
            msg = "Shortcode Error\n"
            msg += f">> Node: {node.url}\n"
            msg += f">> {err.__class__.__name__}: {err}"
            if (cause := err.__cause__):
                msg += f"\n>> Cause: {cause.__class__.__name__}: {cause}"
            sys.exit(msg)
