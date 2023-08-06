import concurrent

import blinker

from narration._misc.constants import DispatchMode, NARRATION_DEBUG_HANDLER_PREFIX
from narration._handler.common.callable import Record_Signal
from narration._handler.common.handler.base_handler import BaseHandler
from narration._handler.common.misc.op_type import OpType
from narration._handler.common.payload.record_payload import RecordPayload
from narration._debug.myself import get_debug_logger

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_PREFIX)


class BaseClientHandler(BaseHandler):
    def __init__(
        self,
        uuid: str = None,
        name: str = None,
        record_emitter: Record_Signal = blinker.Signal(),
        level=None,
        on_close_timeout: float = 1.0,
        message_dispatching: DispatchMode = DispatchMode.SYNC,
        group_id: str = None,
    ):
        super().__init__(
            uuid=uuid,
            name=name,
            type=OpType.SEND,
            level=level,
            on_close_timeout=on_close_timeout,
            message_dispatching=message_dispatching,
            group_id=group_id,
        )
        self._server_notified = False
        self._record_emitter = record_emitter

    def emit(self, record):
        try:
            payload = RecordPayload(record=record, handler_id=self._uuid)
            if self._record_emitter is None:
                _log.error(
                    f"Not record emitter set for sending message to shared processor. Handler id: {self._uuid}. Record: {record}"
                )
                self.handleError(record)
                return

            for receiver, dispatch_status in self._record_emitter.send(payload):
                timeout = None if self._message_dispatching == DispatchMode.SYNC else 2.0
                _log.debug(f"handler to send message {payload.record} with timeout={timeout}")
                dispatch_status.future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            # Record may still be sent later. no error
            _log.warning(
                f"Record sending timeout. Record may not have been dispatch yet. Record: {record}"
            )
        except (concurrent.futures.CancelledError, BaseException):
            # Record will not be sent later.
            _log.error(f"Record sending failed. Record: {record}", exc_info=1)
            self.handleError(record)
        else:
            _log.debug(f"Record dispatched: {record}")
