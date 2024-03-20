Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from fpdf import FPDF
import csv

# Function to parse the VCF file and generate CSV
def parse_vcf_and_generate_csv(file_path, csv_file_path):
    with open(file_path, 'rt') as vcf_file, open(csv_file_path, 'wt', newline='') as csv_file:
        vcf_data = csv.reader(vcf_file, delimiter='\t')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Chromosome', 'Position', 'Ref Allele', 'Alt Allele', 'Quality', 'Filter', 'ACMG Classification'])
        for line in vcf_data:
            if not line[0].startswith('#'):
                chromosome = line[0]
                position = line[1]
                ref_allele = line[3]
                alt_allele = line[4]
                quality = line[5]
                filter_value = line[6]
                acmg_classification = "Placeholder_Classification"
                csv_writer.writerow([chromosome, position, ref_allele, alt_allele, quality, filter_value, acmg_classification])

# PDF generation class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Clinical Genomic Variant Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def table_row(self, data, widths):
        self.set_font('Arial', '', 10)
        for index, item in enumerate(data):
            self.cell(widths[index], 10, item, border=1)
        self.ln()

# Path to VCF file and CSV file
vcf_file_path = "/export/home/railuri/normal_sample.deepvariant.vcf/normal_sample.deepvariant.vcf"
csv_file_path = "Genomic_Variants.csv"

# Parsing the VCF file and generate CSV
parse_vcf_and_generate_csv(vcf_file_path, csv_file_path)

# Creating instance of FPDF class
pdf = PDF()

# Adding a page
pdf.add_page()

# Adding patient information
pdf.chapter_title('Patient Information')
patient_info = """
Patient ID: [Insert Patient ID]
Date of Birth: [Insert Date of Birth]
Gender: [Insert Gender]
Ethnicity: [Insert Ethnicity]
Family History: [Insert Family History]
"""
pdf.chapter_body(patient_info)

# Adding genomic variant information from CSV
pdf.chapter_title('Genomic Variant Information')
column_widths = [30, 30, 30, 30, 30, 30, 50]  
pdf.set_fill_color(200, 220, 255)  
pdf.set_text_color(0, 0, 0)  
pdf.set_font('Arial', 'B', 10)
pdf.table_row(['Chromosome', 'Position', 'Ref Allele', 'Alt Allele', 'Quality', 'Filter', 'ACMG Classification'], column_widths)

# Reading data from CSV and add to PDF
with open(csv_file_path, 'rt') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        pdf.set_font('Arial', '', 10)
        pdf.table_row(row, column_widths)

# Saving the PDF
pdf.output("Clinical_Report_From_CSV.pdf")
print("PDF report generated from CSV.")
