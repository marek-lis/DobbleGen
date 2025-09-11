from bootstrap import project_root
from utils.disk_scanner import scan_dir_for_files, fix_path
from verify.template_validator import Template_Validator

cv = Template_Validator()

templates_path = fix_path(project_root + "/lib/templates")
output_path = fix_path(project_root + "/lib/verified")
print("Scanning the template dir.")

found_templates = scan_dir_for_files(templates_path)
for template in found_templates:
    print(f"Started processing template: \t\t{template}")
    cv.validate(template, output_path)