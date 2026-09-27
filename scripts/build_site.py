"""
Build Site Module (尚书令 · 刊印)
Renders static HTML from final_report.json using templates/daily_template.html.
"""
import sys
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"

def build_site(report_data: dict, output_file: Path) -> Path:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("daily_template.html")

    public_data = report_data.get("public_data", report_data)

    rendered_html = template.render(**public_data)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    return output_file

def main():
    if len(sys.argv) > 1:
        report_path = Path(sys.argv[1])
    else:
        # Default report path
        candidate_files = list((REPO_ROOT / "dist").glob("final_report_*.json"))
        if not candidate_files:
            print("Error: No final_report_*.json found. Run pipeline first.")
            sys.exit(1)
        report_path = candidate_files[-1]

    with open(report_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    iso_date = report_data.get("public_data", {}).get("iso_date", "latest")
    output_html = REPO_ROOT / "dist" / f"{iso_date}.html"
    index_html = REPO_ROOT / "dist" / "index.html"

    build_site(report_data, output_html)
    build_site(report_data, index_html)

    print(f" Successfully built static site: {output_html}")
    print(f" Updated default index: {index_html}")

if __name__ == "__main__":
    main()
