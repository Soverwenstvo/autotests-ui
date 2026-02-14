import requests
import time
import uuid
from playwright.sync_api import Page, expect

BASE_URL = "https://lkb-temp-kub.smbconnect.ru"
TUZ_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLWkU4clI5VU81RWhqZWZ5M180VTBzdEhOQmstLW9SSDJ2a29TcmYtd20wIn0.eyJleHAiOjE3NzIyNTM3MjQsImlhdCI6MTc3MTA0NDEyNCwianRpIjoiZWU4YTA0NTYtZTIwNi00NmMyLThkZGEtOTVkZGM3MjgyZTM2IiwiaXNzIjoiaHR0cHM6Ly9kZXYua2tsLnNtYmNvbm5lY3QucnUvYXV0aC9yZWFsbXMvYmstZGV2IiwiYXVkIjpbImJjIiwicmVhbG0tbWFuYWdlbWVudCIsImFkbWluLWNsaSIsImJyb2tlciIsImFjY291bnQiXSwic3ViIjoiOGI2NTZkNDUtOGIwOS00YmY0LWIzMTItYTI1YzQxNDJhNzA3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYmMiLCJzZXNzaW9uX3N0YXRlIjoiNTE3YzNkZjgtYzE2Zi00NDFkLTkwZDItY2ZjMDk3ZDg1ZWEyIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIiLCJodHRwOi8vZGV2LmRhc2hib2FyZHMuc21iY29ubmVjdC5ydS8qIiwiaHR0cHM6Ly9kZXYuZGFzaGJvYXJkcy5zbWJjb25uZWN0LnJ1LyoiLCJodHRwOi8vODEuMTYzLjE5LjE4MDo4MDA1LyIsImh0dHBzOi8vbG9jYWxob3N0OjgwODgvKiIsImh0dHA6Ly84MS4xNjMuMTkuMTgwLyIsImh0dHA6Ly8wLjAuMC4wOjgwMDUiLCJodHRwOi8vbG9jYWxob3N0OjgwODgvKiIsIioiLCJodHRwOi8vbG9jYWxob3N0OjMwMDAvIiwiaHR0cDovLzEyNy4wLjAuMTozMDAwLyIsImh0dHA6Ly8wLjAuMC4wOjg1MDEiXSwicmVzb3VyY2VfYWNjZXNzIjp7ImJjIjp7InJvbGVzIjpbInRlY2gtc3VwcG9ydC1yb2xlIl19LCJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsIm1hbmFnZS1pZGVudGl0eS1wcm92aWRlcnMiLCJpbXBlcnNvbmF0aW9uIiwicmVhbG0tYWRtaW4iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFkbWluLWNsaSI6eyJyb2xlcyI6WyJyZWFsbS1hZG1pbiIsInVtYV9wcm90ZWN0aW9uIl19LCJicm9rZXIiOnsicm9sZXMiOlsicmVhZC10b2tlbiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsInJlYWxtLWFkbWluIiwidmlldy1hcHBsaWNhdGlvbnMiLCJ2aWV3LWNvbnNlbnQiLCJ1bWFfcHJvdGVjdGlvbiIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwibWFuYWdlLWNvbnNlbnQiLCJkZWxldGUtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiI1MTdjM2RmOC1jMTZmLTQ0MWQtOTBkMi1jZmMwOTdkODVlYTIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidXNlcl9jbGllbnRfcm9sZXMiOlsidGVjaC1zdXBwb3J0LXJvbGUiXSwibGFzdF9uYW1lIjoi0KLQtdGF0JDQtNC80LjQvTEiLCJncm91cHMiOltdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbkB0ZXN0LnJ1IiwiZ2l2ZW5fbmFtZSI6ItCQ0L3RgtC-0L0iLCJwaG9uZSI6Iis3MzQzNDM0MzQzNCIsIm5hbWUiOiLQkNC90YLQvtC9INCi0LXRhdCQ0LTQvNC40L0xIiwic2Vjb25kX25hbWUiOiLQntC70LXQs9C-0LLQuNGHIiwiZmFtaWx5X25hbWUiOiLQotC10YXQkNC00LzQuNC9MSIsImZpcnN0X25hbWUiOiLQkNC90YLQvtC9IiwiZW1haWwiOiJhZG1pbkB0ZXN0LnJ1Iiwic3RhdHVzIjoiYWN0aXZlIn0.J1E52IklpWLyEC-JbFxmdSZKow33oc998giNVoj2szdoIvNdxE1pCwxX_vQZttbF78RqeVf5K8_jJRqaXqFwynmvyV712t2Bkn40dh92iT4WZAqiqZZAPCUH0FYFSNHgRqkcX1GM7XSvrZYUP95DDInVZyOaxz6lJ_vtELpiJugGD0-UbmPQmAW3gHj4C8SP-V4_yCSOdXqDz6ksl1FLr7253SbnFyvrrkoyl4f5rws3clwlAiDyiRyXhpereSHAaPAHlfYZf7FRHeOFeU4EUsxcLFdgi_QhLuLcXVs_l3vSQENDDXc3rC5lBke3KKFxaYB7TRn69M2-RK57dFbEBw"

USERNAME = "admin@test.ru"
PASSWORD = "test"
CLIENT_ID = "bc"
CLIENT_SECRET = "hVmB4SG1k5DfKNZoSn6KswvOuKPdaPRv"


class TestRequestWorkflow:

    def test_create_request_and_complete_task(self, page: Page):

        interaction_id = str(uuid.uuid4())

        # ==============================
        # 1. СОЗДАНИЕ ОБРАЩЕНИЯ
        # ==============================

        create_payload = {
            "interactionId": interaction_id,
            "pubCustomerId": "e24abb28-9dd8-485d-b45a-8fb2e8fdcf33",
            "categoryCode": 302,
            "topic": "Обращение",
            "content": {
                "text": "Тестовое обращение",
                "document": "f8b1faf2-a8ac-4bd8-b4ee-56e9c103312a",
            },
            "files": []
        }

        tuz_headers = {
            "Authorization": TUZ_TOKEN,
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{BASE_URL}/api/or/v1/task/request/create",
            json=create_payload,
            headers=tuz_headers
        )

        assert response.status_code == 200
        print(f"✓ InteractionId создан: {interaction_id}")

        time.sleep(10)

        # ==============================
        # 2. ПОЛУЧЕНИЕ USER TOKEN
        # ==============================

        token_resp = requests.post(
            f"{BASE_URL}/auth/realms/bk-dev/protocol/openid-connect/token",
            data={
                "client_id": CLIENT_ID,
                "grant_type": "password",
                "client_secret": CLIENT_SECRET,
                "scope": "openid",
                "username": USERNAME,
                "password": PASSWORD,
            }
        )

        assert token_resp.status_code == 200
        user_token = token_resp.json()["access_token"]

        user_headers = {
            "Authorization": user_token,
            "Content-Type": "application/json",
        }

        # ====================================
        # 1.3 Получение листинга задач
        # ====================================

        listing_url = f"{BASE_URL}/api/mdm/documents/v1/d/task/dynamic_schema"

        listing_payload = {
            "page": 1,
            "page_size": 100,
            "output_type": "json",
            "order_by": "-number",
            "fields": {
                "created_at": {},
                "updated_at": {},
                "schema_name": {},
                "related_notifications": {"is_calculated": True},
                "schema_version": {},
                "fields.uuid": {},
                "fields.topic": {},
                "fields.number": {},
                "fields.client": {},
                "fields.priority": {},
                "fields.deadline": {},
                "fields.task_type": {},
                "fields.status_task": {},
                "fields.task_content": {},
                "fields.task_type_id": {},
                "fields.category_code": {},
                "fields.client_tariff": {},
                "fields.declaration_type": {},
                "fields.responsible_reference": {},
            },
            "filters": {
                "task_type_lookup": "[302,320]"
            },
            "sort": "-number"
        }

        # ====================================
        # 1.4 Поиск задачи по interaction_id (с retry)
        # ====================================

        task_uuid = None
        max_attempts = 5

        for attempt in range(max_attempts):
            response = requests.post(
                listing_url,
                headers=user_headers,
                json=listing_payload
            )

            assert response.status_code == 200, \
                f"Ошибка получения листинга: {response.text}"

            data = response.json()
            results = data.get("results", [])

            for task in results:
                notification = task.get("notification")
                if notification is None:
                    continue
                extra = notification.get("extra", {})
                task_fields = extra.get("task", {}).get("fields", {})
                if task_fields.get("interaction_uuid") == interaction_id:
                    task_uuid = task.get("fields", {}).get("uuid")
                    break

            if task_uuid:
                break

            print(f"Попытка {attempt + 1}/{max_attempts}: задача не найдена, ждём 2 сек...")
            time.sleep(2)

        assert task_uuid is not None, \
            f"Задача с interaction_id={interaction_id} не найдена в листинге"

        print(f"✓ Найдена задача с uuid: {task_uuid}")


if __name__ == "__main__":
    import subprocess
    subprocess.run(["pytest", __file__, "-v", "-s"])