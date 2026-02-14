import requests
import time
import uuid
import pytest
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
        pubDocument_id = str(uuid.uuid4())

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

        # ==============================
        # 3. ПОИСК ЗАДАЧИ В ЛИСТИНГЕ
        # ==============================

        listing_url = f"{BASE_URL}/api/mdm/documents/v1/d/task/dynamic_schema"

        found_uuid = None

        for attempt in range(1, 21):

            print(f"Попытка поиска {attempt}/20")

            payload = {
                "page": 1,
                "page_size": 20,
                "output_type": "json",
                "order_by": "-number",
                "fields": {
                    "fields.uuid": {},
                    "fields.interaction_uuid": {interaction_id},
                },
                "filters": {
                    "task_type_lookup": "[302,320]"
                },
                "sort": "-number"
            }

            resp = requests.post(listing_url, headers=user_headers, json=payload)
            assert resp.status_code == 200

            tasks = resp.json().get("data", [])

            for task in tasks:
                fields = task.get("fields", {})
                if fields.get("interaction_uuid") == interaction_id:
                    found_uuid = fields.get("uuid")
                    print(f"✓ Найдена задача UUID: {found_uuid}")
                    break

            if found_uuid:
                break

            time.sleep(3)

        assert found_uuid is not None, "Задача не найдена в листинге!"

        # ==============================
        # 4. UI – ОБРАБОТКА ЗАДАЧИ
        # ==============================

        page.goto(f"{BASE_URL}/login")
        page.locator("#basic_username").fill(USERNAME)
        page.locator("#basic_password").fill(PASSWORD)
        page.get_by_role("button", name="Войти").click()
        expect(page).to_have_url(f"{BASE_URL}/tasks", timeout=15000)

        page.goto(f"{BASE_URL}/tasks/{found_uuid}")
        page.wait_for_load_state("networkidle")

        select = page.locator("#taskActionSelectId").first
        select.click()

        expect(page.locator(".ant-select-dropdown:visible")).to_be_visible(timeout=5000)

        page.get_by_text("Обработать задачу вручную").click()
        page.get_by_role("button", name="Подтвердить").click()

        page.wait_for_timeout(2000)

        # Проверяем, что селект заблокирован
        assert not select.is_enabled(), "Селект должен быть заблокирован"

        # ==============================
        # 5. ПРОВЕРКА СТАТУСА
        # ==============================

        for attempt in range(1, 31):

            resp = requests.post(
                f"{BASE_URL}/api/or/v1/task/status",
                json={"interactions": [{"interactionId": interaction_id}]},
                headers=user_headers
            )

            assert resp.status_code == 200

            interactions = resp.json().get("interactions", [])
            if interactions:
                status = interactions[0].get("status")
                print(f"{attempt}: {status}")

                if status in ["COMPLETED", "CLOSED", "DONE", "SUCCESS"]:
                    print(f"✅ Финальный статус: {status}")
                    break

            time.sleep(3)

        print("\n✅ ТЕСТ УСПЕШНО ПРОЙДЕН")