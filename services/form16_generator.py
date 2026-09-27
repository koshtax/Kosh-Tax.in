import os
from jinja2 import Environment, FileSystemLoader

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False


class Form16GeneratorService:
    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_form16_pdf(self, context_data: dict, output_pdf_path: str) -> str:
        """
        Renders HTML from Jinja2 template and writes PDF.
        Agar WeasyPrint system dependencies missing hon toh fallback HTML file save karega.
        """
        template = self.env.get_template("form16_template.html")
        rendered_html = template.render(data=context_data)

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

        if WEASYPRINT_AVAILABLE:
            HTML(string=rendered_html).write_pdf(output_pdf_path)
            return output_pdf_path
        else:
            # Fallback agar WeasyPrint binary load na ho sake
            html_output = output_pdf_path.replace(".pdf", ".html")
            with open(html_output, "w", encoding="utf-8") as f:
                f.write(rendered_html)
            return html_output
