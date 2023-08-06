import os

from .templite import Templite
from .question_list import query

def md():
    os.path.abspath(__file__)
    ppath = os.path.dirname
    ppath_value = ppath(os.path.abspath(__file__))
    tmp_name = 'standard-readme-django-cn.template'
    tmp_path = os.path.join(ppath_value, tmp_name)
    context = query()
    print('@context')
    print(context)
    with open(tmp_path, encoding='utf-8') as f:
        tmp_content = f.read()

    tpl = Templite(tmp_content, context)
    output_path = os.path.join(os.getcwd(), 'README.md')
    ret_txt = tpl.render(output_path=output_path)
    print("README.md generated in current dir")

