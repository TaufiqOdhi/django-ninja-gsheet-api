from googleapiclient.errors import HttpError
from ninja import NinjaAPI, Router

from drf_gsheet_api.schemas import ListColData
from drf_gsheet_api.views.helper import auth_google_api, SPREADSHEET_ID, login_auth

router = Router()
api = NinjaAPI(
    title="Python Google Sheet API",
    description="Python client for google sheet api",
)
api.add_router("sheet/", router, tags=['Gsheet'])


@router.get("/{sheet_num}/{row_num}")
def get_row_data(request, sheet_num: int, row_num: int):
    range_value = 'Sheet{0}!{1}:{1}'.format(sheet_num, row_num)
    service = auth_google_api()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_value
        ).execute()
        return result
    except HttpError as err:
        return api.create_response(
            request,
            err.error_details,
            status=403
        )


@router.post("/{sheet_num}")
def append_row_data(request, sheet_num: int, list_value: ListColData):
    service = auth_google_api()
    values = [list_value.col_data]
    body = {
        'values': values
    }
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='sheet{}'.format(sheet_num),
            valueInputOption='USER_ENTERED',
            includeValuesInResponse=True,
            body=body
        ).execute()
        return result
    except HttpError as err:
        return api.create_response(
            request,
            err.error_details,
            status=403
        )


@api.post("/login")
def login(request):
    return login_auth().to_json()
