# MIT License

# Copyright (c) 2025 rameshsuraparaju

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Provides class for random text generation."""

import logging
import os

import google.generativeai as genai


class Text:
    """Random text generation."""

    _MESSAGE_EMPTY_PROMPT_ZERO_TOKENS = "Prompt is empty or tokens less than / equal to 0."

    _MESSAGE_EMPTY_NAME_OR_INDUSTRY = "Both name and industry must be specified."

    def __init__(self) -> None:

        self.logger = logging.getLogger(__name__)
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        genai.configure(api_key=api_key)

    def __get_account_description_prompt(self, name, industry) -> str:

        return f"""
            You are a sales representative at the company.
            You are responsible for generating, maintaining
            sales accounts (customers / prospects).
            You use salesforce system to track and work on sales opportunities
            and associated with accounts (customers / prospects).

            Generate a company description for {name} in {industry}.
            Include some industry and competitive metrics.
            """

    def __get_contact_description_prompt(self, name: str) -> str:

        return f"""
            You are a sales representative at the company.
            You are responsible for generating, maintaining
            sales accounts (customers / prospects).
            You use salesforce system to track and work on all customer
            contact persons for sales opportunities.
            and associated with accounts (customers / prospects).

            Generate a short text to describe the contact person:
            {name} to enter into a contact description field.
            Include some information about the contact's title
            (examples: CDO, CEO, Data Architect, CIO) and short role
            description and the person's decision making capabilities.
        """

    def __get_opportunity_description_prompt(self, product: str, company: str) -> str:

        return f"""
            You are a sales representative at the company.
            You are responsible for generating, maintaining
            sales opportunities and following up to close wins.
            You use salesforce system to track and work on sales opportunities
            and associated opportunity pipeline.

            Generate a short text to describe the sales opportunity for
            {product} at {company} to enter into an opportunity description field.
            Include some information about the opportunity's requirements
            (examples: changing company policies, regulations,
            cost savings, budget reallocation, employee benefits,
            sustainability etc.)
        """

    def __get_lead_description_prompt(self, product: str) -> str:

        return f"""
            You are a lead generation marketer at the company.
            You are responsible for generating, maintaining
            leads and following up to convert them into sales opportunities.
            You use salesforce system to track and work on leads.

            Generate a short text to describe the customer's / account's
            interest in our product {product} to enter into a lead
            description field.  Include information like why customer is
            interested, how the customer came to know about our product and
            possible next steps for follow-up and or qualification.
        """

    def __get_case_subject_prompt(self, reason: str) -> str:

        return f"""
            You are a customer of the company.
            You encounter problems with the company's products and services.
            You use salesforce system to enter support tickets (cases).

            Generate support ticket subject line for: {reason}
            """

    def __get_case_description_prompt(self, reason: str) -> str:

        return f"""
            You are a customer of the company.
            You encounter problems with the company's products and services.
            You use salesforce system to enter support tickets (cases).

            Generate a short text to describe the problem of: {reason}
            to enter in a support ticket
            """

    def __get_task_description_prompt(self, subject: str, name: str) -> str:

        return f"""
            You are scheduling a calendar task with TODOs in Salesforce.

            Generate a short text to describe the task regarding {subject}
            with the opportunity {name} to enter in a calendar task description.
            Include agenda topics for discussion, action items using {subject}
            """

    def __get_event_description_prompt(self, subject: str, name: str) -> str:

        return f"""
            You are scheduling a calendar event.

            Generate a short text to describe the event regarding {subject}
            with the contact {name} to enter in a calendar event description.
            Include agenda topics for discussion, action items using {subject}
            """

    def __get_youtube_segment_prompt(self, segment_type: str, ad_name: str) -> str:

        return f"""
            You are marketer measuring campaign metrics on DV360 for YouTube.

            Generate a short text with 5-6 words for naming a segment
            with segment type {segment_type} for an ad with name {ad_name}
            Be as concise as possible
            """

    def gen_text(self, prompt: str, max_output_tokens: int) -> str:

        if (prompt == "" or max_output_tokens <= 0):
            msg = __class__._MESSAGE_EMPTY_PROMPT_ZERO_TOKENS
            self.logger.error(msg)
            raise ValueError(msg)

        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(
            prompt,
            generation_config={
                'max_output_tokens': max_output_tokens,
                'temperature': 0.9,
                'top_p': 1,
            },
            stream=False,
        )

        return response.text.replace('*', '').replace('\n', ' ')

    def gen_account_description(self, name, industry) -> str:
        """Generate a random account description."""

        if (name == "" or industry == ""):
            msg = __class__._MESSAGE_EMPTY_NAME_OR_INDUSTRY
            self.logger.error(msg)
            raise ValueError(msg)

        try:
            prompt = self.__get_account_description_prompt(name, industry)
            return self.gen_text(prompt, 100)
        except Exception:
            return f"{name} is a company in {industry} sector."

    def gen_contact_description(self, name) -> str:
        """Generate a random contact description."""

        try:
            prompt = self.__get_contact_description_prompt(name)
            return self.gen_text(prompt, 100)
        except Exception:
            return f"{name} is a senior decision maker."

    def gen_lead_description(self, product: str) -> str:
        """Generate a lead description."""

        try:
            prompt = self.__get_lead_description_prompt(product)
            return self.gen_text(prompt, 300)
        except Exception:
            return product

    def gen_opportunity_description(self, product, company) -> str:
        """Generate a random opportunity description."""

        try:
            prompt = self.__get_opportunity_description_prompt(product, company)
            return self.gen_text(prompt, 100)
        except Exception:
            return f"Regarding requirement for {product} at {company}."

    def gen_task_description(self, subject: str, name: str) -> str:
        """Generate a random task description."""

        try:
            prompt = self.__get_task_description_prompt(subject, name)
            return self.gen_text(prompt, 100)
        except Exception:
            return subject

    def gen_event_description(self, subject: str, name: str) -> str:
        """Generate a random event description."""

        try:
            prompt = self.__get_event_description_prompt(subject, name)
            return self.gen_text(prompt, 100)
        except Exception:
            return subject

    def gen_case_subject(self, reason: str) -> str:
        """Generate a random case subject."""

        try:
            prompt = self.__get_case_subject_prompt(reason)
            return self.gen_text(prompt, 100)
        except Exception:
            return reason

    def gen_case_description(self, reason: str) -> str:
        """Generate a random case description."""

        try:
            prompt = self.__get_case_description_prompt(reason)
            return self.gen_text(prompt, 300)
        except Exception:
            return reason

    def gen_youtube_segment_name(self, segment_type: str, ad_name: str) -> str:
        """Generate a random segment name description."""

        try:
            prompt = self.__get_youtube_segment_prompt(
                segment_type,
                ad_name
            )
            return self.gen_text(prompt, 300)
        except Exception:
            return segment_type + ad_name + "segment"





