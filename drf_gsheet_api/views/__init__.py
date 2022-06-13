from ninja import NinjaAPI

from drf_gsheet_api.schemas import ListColData
from drf_gsheet_api.views.helper import auth_google_api, SPREADSHEET_ID

api = NinjaAPI(title="Python Google Sheet API",)


@api.get("/{sheet_num}/{row_num}")
def get_row_data(request, sheet_num: int, row_num: int):
    range_value = 'Sheet{0}!{1}:{1}'.format(sheet_num, row_num)
    service = auth_google_api()
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_value
    ).execute()
    return result


@api.post("/{sheet_num}")
def append_row_data(request, sheet_num: int, list_value: ListColData):
    service = auth_google_api()
    values = [list_value.col_data]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='sheet{}'.format(sheet_num),
        valueInputOption='USER_ENTERED',
        includeValuesInResponse=True,
        body=body
    ).execute()
    return result
