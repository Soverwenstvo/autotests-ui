import asyncio
import enum
import json
import os
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Optional, Callable
from botocore.config import Config

import boto3

S3_REGION_NAME = "ru-7"
S3_SERVER_PUBLIC_KEY = "4c27c5e10fa84e2fa091ccb2de240c7b"
S3_SERVER_SECRET_KEY = "dfdfa410b8664e8da56ba34bcb03f8bb"
S3_ENDPOINT_URL = "https://s3.ru-7.storage.selcloud.ru"
S3_BUCKET_NAME = "devk8"
S3_DIRTY_BUCKET_NAME = "devk8"
S3_CLEAN_BUCKET_NAME = "devk8"
S3_FILE_PREFIX = "dev"

PROJECT_NAME = 'lkb'


class S3ConfigTypes(enum.Enum):
    bank = 'bank'
    internal = 'internal'


S3_CONFIG_MAPPINGS = {
    S3ConfigTypes.internal.name: {
        'S3_REGION_NAME': S3_REGION_NAME,
        'S3_SERVER_PUBLIC_KEY': S3_SERVER_PUBLIC_KEY,
        'S3_SERVER_SECRET_KEY': S3_SERVER_SECRET_KEY,
        'S3_ENDPOINT_URL': S3_ENDPOINT_URL,
        'S3_BUCKET_NAME': S3_BUCKET_NAME,
        'S3_DIRTY_BUCKET_NAME': S3_DIRTY_BUCKET_NAME,
        'S3_CLEAN_BUCKET_NAME': S3_CLEAN_BUCKET_NAME,
        'S3_FILE_PREFIX': S3_FILE_PREFIX,
    },  # Внутренний s3
}


def s3_connection(s3_action: Callable):
    """Декоратор для ретрая"""

    async def wrapper(*args, **kwargs):
        raw_url = kwargs['s3_handler'].S3_ENDPOINT_URL
        list_of_s3_endpoint_urls = []
        if raw_url and raw_url.strip():
            list_of_s3_endpoint_urls = raw_url.replace(' ', '').split(',')

        servers_available = False
        handler = kwargs.pop('s3_handler')

        dict_of_errors = {}
        for _ in range(2):
            try:
                for s3_endpoint_url in list_of_s3_endpoint_urls:
                    handler.make_boto3_client(s3_endpoint_url=s3_endpoint_url)
                    try:
                        response = await s3_action(*args, **kwargs)
                    except Exception as e:
                        dict_of_errors.update({s3_endpoint_url: str(e)})
                        print('-----------------')
                        print(e)
                        continue
                    servers_available = True
                    return response
            except Exception as e:
                print(e)
                continue

        if not servers_available:
            print(dict_of_errors)
            raise Exception(dict_of_errors)

    return wrapper


class StorageS3FileHandler:
    """Класс для работы с s3 хранилищем"""

    def __init__(
            self,
            config_type: Optional[str] = S3ConfigTypes.internal.name
    ):
        self.config_type = config_type
        self.S3_REGION_NAME = None
        self.S3_SERVER_PUBLIC_KEY = None
        self.S3_SERVER_SECRET_KEY = None
        self.S3_ENDPOINT_URL = None
        self.S3_DIRTY_BUCKET_NAME = None
        self.S3_CLEAN_BUCKET_NAME = None
        self.S3_BUCKET_NAME = None
        self.S3_FILE_PREFIX = None
        self.client = None
        self.s3_paginator = None
        self.S3_CLIENT_CERT = ''
        self.S3_API_RETRIES = 5

        config_map = S3_CONFIG_MAPPINGS[config_type]

        for attribute_key, attribute_value in config_map.items():
            setattr(self, attribute_key, attribute_value)

    @s3_connection
    async def get_file_stream(self, s3_file_name: str) -> bytes:
        """Возвращает файл из с3 в виде стрима"""
        return self.client.get_object(Bucket=self.S3_BUCKET_NAME, Key=f"{self.S3_FILE_PREFIX}/{s3_file_name}")

    @s3_connection
    async def get_file_stream_by_s3_key(self, s3_key: str) -> bytes:
        """Возвращает файл из с3 в виде стрима по ключу"""
        return self.client.get_object(Bucket=self.S3_BUCKET_NAME, Key=s3_key)

    def make_boto3_client(self, s3_endpoint_url: str) -> None:
        """Функция по созданию клиента для работы с S3"""
        if self.S3_CLIENT_CERT:
            config = Config(
                client_cert=self.S3_CLIENT_CERT,
                signature_version="s3v4",
                s3={"addressing_style": "path"}
            )
        elif self.config_type == S3ConfigTypes.bank.name:
            config = Config()
        else:
            config = Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"}
            )

        self.client = boto3.client(
            's3',
            # region_name=self.S3_REGION_NAME,
            aws_access_key_id=self.S3_SERVER_PUBLIC_KEY,
            aws_secret_access_key=self.S3_SERVER_SECRET_KEY,
            endpoint_url=s3_endpoint_url,
            config=config,
            verify=False,
        )

        self.s3_paginator = self.client.get_paginator('list_objects_v2')

    @s3_connection
    async def upload_file_to_s3_path(self, file_name: str, upload_from_hard_drive_path: str) -> str:
        """Сохраняет файл в s3 и вовзращает уникальный путь из s3"""
        s3_unique_file_path = f'{PROJECT_NAME}/{self.S3_FILE_PREFIX}/{file_name}'

        self.client.upload_file(
            upload_from_hard_drive_path,
            self.S3_BUCKET_NAME,
            s3_unique_file_path
        )

        return s3_unique_file_path

    @s3_connection
    async def upload_file_to_bank_s3(self, file_path: str, file_uuid: str):
        return await self._upload_file_to_bank_s3_from_internal_s3(
            file_path=file_path,
            file_uuid=file_uuid,
            uploaded_keys=[],
        )

    @s3_connection
    async def download_file_from_s3(self, s3_key) -> str:
        separator = f'lkb/{self.S3_FILE_PREFIX}/'
        s3_key_without_path = s3_key.split(separator, 1)[-1]
        self.client.download_file(self.S3_BUCKET_NAME, s3_key, rf'/media/{s3_key_without_path}')
        return rf'/media/{s3_key_without_path}'

    @s3_connection
    async def get_file_stream(self, s3_file_name: str) -> bytes:
        """Возвращает файл из с3 в виде стрима"""
        return self.client.get_object(Bucket=self.S3_BUCKET_NAME, Key=f"{self.S3_FILE_PREFIX}/{s3_file_name}")

    async def check_if_file_exist_in_s3(
            self,
            s3_file_key: str
    ) -> None:
        """Загрузка файлов внутрь S3"""

        return await self.get_file_stream(s3_file_name=s3_file_key)


async def check_if_file_exist() -> dict:
    s3_handler = StorageS3FileHandler()

    s3_rezult=await s3_handler.get_file_stream_by_s3_key(
        s3_key='lkb/dev/test/c603b6ed-a47c-4c50-a3fa-d5895d350ec8_Close.xlsx',
        s3_handler=s3_handler
    )
    print(s3_rezult)

    return {'response_status': 'success'}


async def main():
    await check_if_file_exist()


if __name__ == "__main__":
    asyncio.run(main())