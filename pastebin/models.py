from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.slug)


class CodePaste(models.Model):
    text = models.TextField(blank=True)
    htmld_text = models.TextField()
    language = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_on = models.DateField(auto_now_add=1)

    @models.permalink
    def get_absolute_url(self):
        return ('pastebin.views.paste_details', [self.id])

    @models.permalink
    def get_plain_url(self):
        return ('pastebin.views.plain', [self.id])

    @models.permalink
    def get_html_url(self):
        return ('pastebin.views.html', [self.id])

    def save(self, *args, **kwargs):
        """Htmlize text and save to htmld_text. Use Pygments"""

        self.htmld_text = htmlize(self.text, self.language)
        super(CodePaste, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


def htmlize(text, language):
    from pygments import highlight
    from pygments.formatters import HtmlFormatter as Formatter
    if language == 'Python':
        from pygments.lexers import PythonLexer as Lexer
    elif language == 'Perl':
        from pygments.lexers import PerlLexer as Lexer
    elif language == 'Ruby':
        from pygments.lexers import RubyLexer as Lexer
    elif language == 'PythonConsole':
        from pygments.lexers import PythonConsoleLexer as Lexer
    elif language == 'PythonTraceback':
        from pygments.lexers import PythonTracebackLexer as Lexer
    elif language == 'RubyConsole':
        from pygments.lexers import RubyConsoleLexer as Lexer
    elif language == 'HtmlDjango':
        from pygments.lexers import HtmlDjangoLexer as Lexer
    elif language == 'Html':
        from pygments.lexers import HtmlLexer as Lexer
    elif language == 'Cobol':
        from pygments.lexers import CobolLexer as Lexer
    elif language == 'CSharpAspx':
        from pygments.lexers import CSharpAspxLexer as Lexer
    elif language == 'CSharp':
        from pygments.lexers import CSharpLexer as Lexer
    else:
        from pygments.lexers import TextLexer as Lexer
    """
    Todo: I cant get this to work.
    lang_lexer = str(language + 'Lexer')
    Lexer = __import__('pygments.lexers', globals(), locals(), [lang_lexer, ])
    Or
    from pygments.lexers import get_lexer_by_name
    Lexer = get_lexer_by_name(language.lower())
    """
    htmld = highlight(text, Lexer(), Formatter(linenos='table'))
    return htmld

