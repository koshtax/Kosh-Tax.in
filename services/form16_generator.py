import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

class Form16GeneratorService:
    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_form16_pdf(self, context_data: dict, output_pdf_path: str) -> str:
        """
        Renders HTML from Jinja2 template and writes direct PDF using WeasyPrint.
        """
        template = self.env.get_template("form16_template.html")
        rendered_html = template.render(data=context_data)

        # Make sure parent directory exists
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

        HTML(string=rendered_html).write_pdf(output_pdf_path)
        return output_pdf_path
