from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
TITLE_MESSAGE = f"Отчет от {NOW_DATE_TIME}"
SPREEDSHEET_BODY = {
        "properties": {"title": TITLE_MESSAGE, "locale": "ru_RU"},
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {"rowCount": 100, "columnCount": 3},
                }
            }
        ],
    }

async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = SPREEDSHEET_BODY
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(spreadsheet_id: str, wrapper_services: Aiogoogle) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, projects: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table_values = [
        ["Отчет от", now_date_time],
        ["Топ проектов по скорости закрытия"],
        ["Название проекта", "Время сбора", "Описание"],
    ]
    for project in projects:
        name, time, description = project
        new_row = [name, time, description]
        table_values.append(new_row)

    update_body = {"majorDimension": "ROWS", "values": table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1:C100",
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
