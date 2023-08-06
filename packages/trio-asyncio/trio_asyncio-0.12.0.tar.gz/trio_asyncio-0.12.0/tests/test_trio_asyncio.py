import pytest
import sys
import asyncio
from async_generator import async_generator, yield_
import trio_asyncio


async def use_asyncio():
    await trio_asyncio.aio_as_trio(asyncio.sleep)(0)


@pytest.fixture()
async def asyncio_fixture_with_fixtured_loop(loop):
    await use_asyncio()
    yield None


@pytest.fixture()
async def asyncio_fixture_own_loop():
    async with trio_asyncio.open_loop():
        await use_asyncio()
        yield None


@pytest.mark.trio
async def test_no_fixture():
    async with trio_asyncio.open_loop():
        await use_asyncio()


@pytest.mark.trio
async def test_half_fixtured_asyncpg_conn(asyncio_fixture_own_loop):
    await use_asyncio()


@pytest.mark.trio
async def test_fixtured_asyncpg_conn(asyncio_fixture_with_fixtured_loop):
    await use_asyncio()


@pytest.mark.trio
async def test_get_running_loop():
    async with trio_asyncio.open_loop() as loop:
        try:
            from asyncio import get_running_loop
        except ImportError:
            pass  # Python 3.6
        else:
            assert get_running_loop() == loop
