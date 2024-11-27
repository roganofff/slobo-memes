from typing import Union, Any

from jinja2 import Environment, PackageLoader, select_autoescape
from aiogram.utils.markdown import hide_link

env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape()
)


def render(
    template_name: str,
    image_url: str = None,
    **kwargs: Union[int, str, dict[str, Any]],
) -> str:
    rendered = env.get_template(template_name).render(**kwargs)
    if image_url is not None:
        rendered = f'{hide_link(image_url)}{rendered}'
    return rendered