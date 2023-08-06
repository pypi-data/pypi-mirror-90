from tests import aiotest
import signal
import pytest


class TestCallback(aiotest.TestCase):
    @pytest.mark.trio
    async def test_call_soon(self, loop):
        result = []

        def hello_world(loop):
            result.append('Hello World')
            loop.stop()

        loop.call_soon(hello_world, loop)
        await loop.stop().wait()
        assert result == ['Hello World']

    @pytest.mark.trio
    async def test_call_soon_control(self, loop):
        result = []

        def func(result, loop):
            loop.call_soon(append_result, loop, result, "yes")
            result.append(str(result))

        def append_result(loop, result, value):
            result.append(value)
            loop.stop()

        loop.call_soon(func, result, loop)
        await loop.wait_stopped()
        # http://bugs.python.org/issue22875: Ensure that call_soon() does not
        # call append_result() immediatly, but when control returns to the
        # event loop, when func() is done.
        assert result == ['[]', 'yes']

    @pytest.mark.trio
    async def test_close(self, loop, config):
        if not config.call_soon_check_closed:
            # http://bugs.python.org/issue22922 not implemented
            self.skipTest("call_soon() doesn't raise if the event loop is closed")

        await loop.stop().wait()
        loop.close()

        async def test():
            pass

        func = lambda: False
        coro = test()
        try:
            with pytest.raises(RuntimeError, match='not a sync loop'):
                loop.run_until_complete(None)
            with pytest.raises(RuntimeError):
                loop.run_forever()
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.call_soon(func)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.call_soon_threadsafe(func)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.call_later(1.0, func)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.call_at(loop.time() + .0, func)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.run_in_executor(None, func)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                await loop.run_aio_coroutine(coro)
            with pytest.raises(RuntimeError, match='Event loop is closed'):
                loop.add_signal_handler(signal.SIGTERM, func)
        finally:
            coro.close()
