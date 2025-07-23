from jinja2 import Environment, PackageLoader, select_autoescape


def get_text(text: str) -> str:
    text = text.replace("_", r"\_")
    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")
    text = text.replace("[", r"\[")
    text = text.replace("]", r"\]")
    text = text.replace("<", r"\<")
    text = text.replace(">", r"\>")
    text = text.replace("(", r"\(")
    text = text.replace(")", r"\)")
    text = text.replace("#", "")
    text = text.replace("+", r"\+")
    text = text.replace("-", r"\-")
    text = text.replace(".", r"\.")
    text = text.replace("!", r"\!")
    text = text.replace("=", r"\=")
    text = text.replace("|", r"\|")
    text = text.replace("**", "*")
    return text


def get_mes(path: str, **kwargs):
    """
    Эта функция принимает путь к файлу шаблона и ключевые аргументы для рендеринга шаблона.
    Она возвращает отрендеренный шаблон в виде строки.

    Args:
        path (str): Путь к файлу шаблона.
        **kwargs: Ключевые аргументы, которые будут использованы в шаблоне.

    Returns:
        str: Отрендеренный шаблон.
    """
    env = Environment(
        loader=PackageLoader(
            package_name="main", package_path="internal/messages", encoding="utf-8"
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )

    if ".md" not in path:
        path = path + ".md"
    tmpl = env.get_template(path)
    return tmpl.render(kwargs)
