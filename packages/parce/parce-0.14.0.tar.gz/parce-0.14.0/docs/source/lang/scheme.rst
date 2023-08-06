scheme
======

.. automodule:: parce.lang.scheme
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Scheme.root`` and text:

.. code-block:: scheme

    ; scheme example
    ; convert to html entities
    (define (attribute-escape s)
      (string-substitute "\n" "&#10;"
        (string-substitute "\"" "&quot;"
          (string-substitute "&" "&amp;"
            s))))

Result tree::

    <Context Scheme.root at 0-194 (3 children)>
     ├╴<Context Scheme.singleline_comment at 0-16 (2 children)>
     │  ├╴<Token ';' at 0:1 (Comment)>
     │  ╰╴<Token ' scheme example' at 1:16 (Comment)>
     ├╴<Context Scheme.singleline_comment at 17-43 (2 children)>
     │  ├╴<Token ';' at 17:18 (Comment)>
     │  ╰╴<Token ' convert to html entities' at 18:43 (Comment)>
     ╰╴<Context Scheme.list at 44-194 (5 children)>
        ├╴<Token '(' at 44:45 (Delimiter.OpenParen)>
        ├╴<Token 'define' at 45:51 (Keyword)>
        ├╴<Context Scheme.list at 52-72 (4 children)>
        │  ├╴<Token '(' at 52:53 (Delimiter.OpenParen)>
        │  ├╴<Token 'attribute-escape' at 53:69 (Name)>
        │  ├╴<Token 's' at 70:71 (Name)>
        │  ╰╴<Token ')' at 71:72 (Delimiter.CloseParen)>
        ├╴<Context Scheme.list at 75-193 (6 children)>
        │  ├╴<Token '(' at 75:76 (Delimiter.OpenParen)>
        │  ├╴<Token 'string-substitute' at 76:93 (Name)>
        │  ├╴<Context Scheme.string at 94-98 (3 children)>
        │  │  ├╴<Token '"' at 94:95 (Literal.String)>
        │  │  ├╴<Token '\\n' at 95:97 (Literal.String)>
        │  │  ╰╴<Token '"' at 97:98 (Literal.String)>
        │  ├╴<Context Scheme.string at 99-106 (3 children)>
        │  │  ├╴<Token '"' at 99:100 (Literal.String)>
        │  │  ├╴<Token '&#10;' at 100:105 (Literal.String)>
        │  │  ╰╴<Token '"' at 105:106 (Literal.String)>
        │  ├╴<Context Scheme.list at 111-192 (6 children)>
        │  │  ├╴<Token '(' at 111:112 (Delimiter.OpenParen)>
        │  │  ├╴<Token 'string-substitute' at 112:129 (Name)>
        │  │  ├╴<Context Scheme.string at 130-134 (3 children)>
        │  │  │  ├╴<Token '"' at 130:131 (Literal.String)>
        │  │  │  ├╴<Token '\\"' at 131:133 (Literal.String.Escape)>
        │  │  │  ╰╴<Token '"' at 133:134 (Literal.String)>
        │  │  ├╴<Context Scheme.string at 135-143 (3 children)>
        │  │  │  ├╴<Token '"' at 135:136 (Literal.String)>
        │  │  │  ├╴<Token '&quot;' at 136:142 (Literal.String)>
        │  │  │  ╰╴<Token '"' at 142:143 (Literal.String)>
        │  │  ├╴<Context Scheme.list at 150-191 (6 children)>
        │  │  │  ├╴<Token '(' at 150:151 (Delimiter.OpenParen)>
        │  │  │  ├╴<Token 'string-substitute' at 151:168 (Name)>
        │  │  │  ├╴<Context Scheme.string at 169-172 (3 children)>
        │  │  │  │  ├╴<Token '"' at 169:170 (Literal.String)>
        │  │  │  │  ├╴<Token '&' at 170:171 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 171:172 (Literal.String)>
        │  │  │  ├╴<Context Scheme.string at 173-180 (3 children)>
        │  │  │  │  ├╴<Token '"' at 173:174 (Literal.String)>
        │  │  │  │  ├╴<Token '&amp;' at 174:179 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 179:180 (Literal.String)>
        │  │  │  ├╴<Token 's' at 189:190 (Name)>
        │  │  │  ╰╴<Token ')' at 190:191 (Delimiter.CloseParen)>
        │  │  ╰╴<Token ')' at 191:192 (Delimiter.CloseParen)>
        │  ╰╴<Token ')' at 192:193 (Delimiter.CloseParen)>
        ╰╴<Token ')' at 193:194 (Delimiter.CloseParen)>


