#!/usr/bin/env python
"""

Main program

"""

import json
import textract
import cvscan.annotations_parser
import cvscan.configurations
import cvscan.converter
import cvscan.details_parser as dp
import cvscan.dirpath
import cvscan.language_parser as lp


class Cvscan():
    def __init__(self, name, path = dirpath.RESUMEPATH):
        self.path = path
        self.path = name

        if self.exists():
            self.extract()
        else:
            raise OSError("There is no file found at " + self.path)

    def exists(self):
        return configurations.isfile(self.path)

    def extract_text_from_doc(self, doc_path):
        '''
        Helper function to extract plain text from .doc or .docx files

        :param doc_path: path to .doc or .docx file to be extracted
        :return: string of extracted text
        '''
        temp = textract.process(doc_path)
        text = [line.replace('\t', ' ') for line in temp.decode("utf-8").split('\n') if line]
        return ' '.join(text)

    # Extracts raw text from resume
    # Currently only supports PDF
    def extract(self):
        # add functions to convert other formats to text
        if self.path.find(".pdf") != -1:
            self.raw_text = converter.pdf_to_txt(self.path)

        if self.path.find(".doc") != -1 or self.path.find(".docx"):
            self.raw_text =  self.extract_text_from_doc(self.path)

        if self.raw_text is not '':
            self.parse()
        else:
            raise ValueError("Error extracting resume text.")

    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.name = lp.fetch_name(self.raw_text)
        self.emails = dp.fetch_email(self.raw_text)
        self.phone_numbers = dp.fetch_phone(self.raw_text)
        self.address = dp.fetch_address(self.raw_text)
        self.experience = dp.calculate_experience(self.raw_text)
        self.cleaned_resume = lp.clean_resume(self.raw_text)
        self.skills = dp.fetch_skills(self.cleaned_resume)
        (self.qualifications,self.degree_info) = dp.fetch_qualifications(
            self.raw_text)
        self.job_positions, self.category = dp.fetch_jobs(self.cleaned_resume)
        self.current_employers,self.employers = lp.fetch_employers(
            self.raw_text,self.job_positions)
        self.extra_info = dp.fetch_extra(self.raw_text)

    # TODO: Add more fetch here
    def show(self):
        return json.dumps({
            "name" : self.name,
            "experience" : self.experience,
            "address" : self.address,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills,
            "jobs" : self.job_positions,
            "job category" : self.category,
            "employers" : self.employers,
            "current_employers" : self.current_employers,
            "qualifications" : self.qualifications,
            "qualifications_info" : self.degree_info,
            "extra_info" : self.extra_info
        })
