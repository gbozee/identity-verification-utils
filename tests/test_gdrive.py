import os

import pytest

from tuteria_auth.gdrive import AdminSheetAPI, create_credentials
from tuteria_auth.login import staff_verification
from tuteria_auth.quizzes import (
    CSVUploadInterface,
    GoogleSheetInterface,
    QuizExtractAPI,
)

current_dir = os.path.abspath(os.path.dirname(__name__))
csv_file = os.path.join(current_dir, "..", "quiz-service", "tests", "sample_file.csv")
params = {
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGlE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGlE_PRIVATE_KEY"),
    "client_email": os.getenv("GOOGlE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
}
# instance = AdminSheetAPI(**params)
# # instance = AdminSheetAPI(os.path.join(current_dir, "client_secret.json"))
# instance.load_file(
#     url
# )
# result = instance.match_role("kenny@tuteria.com", "staff")


def test_staff_verification():
    url = "https://docs.google.com/spreadsheets/d/1sI_BrSpetmPMcWBlPnuoKVdNdiLaoeEFD_X9mWHEiUQ/edit?usp=sharing"
    result = staff_verification(
        "kenny@tuteria.com", role="staff", file_url=url, config_obj=params
    )
    print(result)


class ApiHelper:
    async def save_shared_text(self, items):
        return [x.strip() for x in items]
        # return item.strip()

    async def save_media_resource(self, items):
        return [x.strip() for x in items]
        # return item

    async def save_shared_questions(self, items):
        return [x.strip() for x in items]


@pytest.mark.run_loop
async def test_google_sheet_interface():
    url = "https://docs.google.com/spreadsheets/d/132vGcZPoZZxG3lbEx_YNoveOyucp6vWVc7Tw4-s4DwQ/edit?usp=sharing"
    sheet_instance = GoogleSheetInterface(**params)
    api = QuizExtractAPI(sheet_instance.load_file, url, "11+ Non Verbal Reasoning")
    rows = await api.clean_sheet(api_call_class=ApiHelper())
    import ipdb

    ipdb.set_trace()
    print("Hello")


@pytest.mark.run_loop
async def test_regions_section():
    url = "https://docs.google.com/spreadsheets/d/1O0XIhXRvhgJLSyFwlBHaB1ApYTnosRxZM559zNLRdZA/edit?usp=sharing"
    sheet_instance = GoogleSheetInterface(**params)
    sheet_instance.load_file(url, "Regions")
    import ipdb

    ipdb.set_trace()
    print(sheet_instance)


@pytest.mark.run_loop
async def test_csv_file_upload_interface():
    api = QuizExtractAPI(CSVUploadInterface, csv_file)
    rows = await api.clean_sheet(api_call_class=ApiHelper())
    import ipdb

    ipdb.set_trace()
    print("Hello")
