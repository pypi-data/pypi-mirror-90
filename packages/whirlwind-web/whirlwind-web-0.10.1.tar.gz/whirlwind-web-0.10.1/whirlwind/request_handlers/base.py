from whirlwind.store import create_task

from delfick_project.norms import sb, dictobj, Meta
from tornado.web import RequestHandler, HTTPError
from tornado import websocket
import binascii
import logging
import asyncio
import json
import uuid

log = logging.getLogger("whirlwind.request_handlers.base")


class Finished(Exception):
    def __init__(self, status=500, **kwargs):
        self.kwargs = kwargs
        self.kwargs["status"] = status

    def as_dict(self):
        return self.kwargs


def reprer(o):
    if type(o) is bytes:
        return binascii.hexlify(o).decode()
    return repr(o)


class MessageFromExc:
    def __init__(self, *, log_exceptions=True):
        self.log_exceptions = log_exceptions

    def __call__(self, exc_type, exc, tb):
        if isinstance(exc, Finished):
            return exc.kwargs
        else:
            return self.process(exc_type, exc, tb)

    def process(self, exc_type, exc, tb):
        if self.log_exceptions:
            log.error(exc, exc_info=(exc_type, exc, tb))

        return {
            "status": 500,
            "error": "Internal Server Error",
            "error_code": "InternalServerError",
        }


class AsyncCatcher(object):
    def __init__(self, request, info, final=None):
        self.info = info
        self.final = final
        self.request = request

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            self.complete(self.info.get("result"), status=200)
            return

        msg = self.request.message_from_exc(exc_type, exc, tb)
        self.complete(msg, status=500, exc_info=(exc_type, exc, tb))

        # And don't reraise the exception
        return True

    def send_msg(self, msg, status=200, exc_info=None):
        if self.request._finished and not hasattr(self.request, "ws_connection"):
            if type(msg) is dict:
                msg = json.dumps(msg, default=self.request.reprer, sort_keys=True, indent="    ")
                self.request.hook("request_already_finished", msg)
            return

        if hasattr(msg, "exc_info") and exc_info is None:
            exc_info = msg.exc_info

        if self.final is None:
            self.request.send_msg(msg, status, exc_info=exc_info)
        else:
            self.final(msg, exc_info=exc_info)

    def complete(self, msg, status=sb.NotSpecified, exc_info=None):
        if type(msg) is dict:
            result = json.loads(json.dumps(msg, default=self.request.reprer, indent="    "))
        else:
            result = msg

        self.send_msg(result, status=status, exc_info=exc_info)


class RequestsMixin:
    """
    A mixin class you may use for your handler which provides some handy methods
    for dealing with data
    """

    _merged_options_formattable = True

    def hook(self, func, *args, **kwargs):
        if hasattr(self, func):
            return getattr(self, func)(*args, **kwargs)

    # def process_reply(self, msg, exc_info=None):
    #     """A hook that provides the msg sent as reply or progress"""
    #     pass

    # def request_already_finished(self, msg):
    #     """Hook for when we would send a message to an already closed websocket"""

    @property
    def reprer(self):
        if not hasattr(self, "_reprer"):
            self._reprer = reprer
        return self._reprer

    @reprer.setter
    def reprer(self, value):
        self._reprer = value

    @property
    def message_from_exc(self):
        if not hasattr(self, "_message_from_exc"):
            self._message_from_exc = MessageFromExc(
                log_exceptions=getattr(self, "log_exceptions", True)
            )
        return self._message_from_exc

    @message_from_exc.setter
    def message_from_exc(self, value):
        self._message_from_exc = value

    def async_catcher(self, info, final=None):
        return AsyncCatcher(self, info, final=final)

    def body_as_json(self, body=None):
        """
        Return the body of the request as a json object

        If there is a special ``__body__`` file in the request, we will consider this
        to be the body instead of the request body
        """
        if body is None:
            if "__body__" in self.request.files:
                body = self.request.files["__body__"][0]["body"].decode()
            else:
                body = self.request.body.decode()

        try:
            if type(body) is str:
                body = json.loads(body)
        except (TypeError, ValueError) as error:
            log.error("Failed to load body as json\t%s", body)
            raise Finished(status=400, reason="Failed to load body as json", error=error)

        return body

    def send_msg(self, msg, status=sb.NotSpecified, exc_info=None):
        """
        This determines what content-type and exact body to write to the response

        If ``msg`` has ``as_dict``, we call it.

        If ``msg`` is a dictionary and has status, we use that as the status of
        the request, otherwise we say it's a 200.

        If there is ``html`` in ``msg``, we use that as the body of the request.

        If ``msg`` is None, we close without a body.

        * If ``msg`` is a ``dict`` or ``list``, we write it as a json object.
        * If ``msg`` starts with ``<html>`` or ``<!DOCTYPE html>`` we treat it
          as html content
        * Otherwise we write ``msg`` as ``text/plain``
        """
        if hasattr(msg, "exc_info") and exc_info is None:
            exc_info = msg.exc_info

        if hasattr(msg, "as_dict"):
            msg = msg.as_dict()

        self.hook("process_reply", msg, exc_info=exc_info)

        if type(msg) is dict and "status" in msg:
            status = msg["status"]
        elif exc_info and exc_info[1]:
            if hasattr(exc_info[1], "status"):
                status = exc_info[1].status
            else:
                status = 500

        if status is sb.NotSpecified:
            status = 200

        self.set_status(status)

        if type(msg) is dict and "html" in msg:
            msg = msg["html"]

        if msg is None:
            self.finish()
            return

        if type(msg) in (dict, list):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(json.dumps(msg, default=self.reprer, sort_keys=True, indent="    "))
        elif msg.lstrip().startswith("<html>") or msg.lstrip().startswith("<!DOCTYPE html>"):
            self.write(msg)
        else:
            self.set_header("Content-Type", "text/plain; charset=UTF-8")
            self.write(msg)
        self.finish()


class Simple(RequestsMixin, RequestHandler):
    """
    Helper for using ``self.async_catcher`` from ``RequestsMixin`` for most HTTP verbs.

    .. code-block:: python

        class MyRequestHandler(Simple):
            async def do_get():
                return "<html><body><p>lol</p></body></html>"

    Essentially you define ``async def do_<verb>(self)`` methods for each verb
    you want to support.

    This supports

    * get
    * put
    * post
    * patch
    * delete
    """

    log_exceptions = True

    async def get(self, *args, **kwargs):
        if not hasattr(self, "do_get"):
            raise HTTPError(405)

        info = {"result": None}
        async with self.async_catcher(info):
            info["result"] = await self.do_get(*args, **kwargs)

    async def put(self, *args, **kwargs):
        if not hasattr(self, "do_put"):
            raise HTTPError(405)

        info = {"result": None}
        async with self.async_catcher(info):
            info["result"] = await self.do_put(*args, **kwargs)

    async def post(self, *args, **kwargs):
        if not hasattr(self, "do_post"):
            raise HTTPError(405)

        info = {"result": None}
        async with self.async_catcher(info):
            info["result"] = await self.do_post(*args, **kwargs)

    async def patch(self, *args, **kwargs):
        if not hasattr(self, "do_patch"):
            raise HTTPError(405)

        info = {"result": None}
        async with self.async_catcher(info):
            info["result"] = await self.do_patch(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        if not hasattr(self, "do_delete"):
            raise HTTPError(405)

        info = {"result": None}
        async with self.async_catcher(info):
            info["result"] = await self.do_delete(*args, **kwargs)


json_spec = sb.match_spec(
    (bool, sb.any_spec()),
    (int, sb.any_spec()),
    (float, sb.any_spec()),
    (str, sb.any_spec()),
    (list, lambda: sb.listof(json_spec)),
    (type(None), sb.any_spec()),
    fallback=lambda: sb.dictof(sb.string_spec(), json_spec),
)


class SimpleWebSocketBase(RequestsMixin, websocket.WebSocketHandler):
    """
    Used for websocket handlers

    Implement ``process_message``

    .. automethod:: whirlwind.request_handlers.base.SimpleWebSocketBase.process_message

    This class takes in messages of the form ``{"path": <string>, "message_id": <string>, "body": <dictionary}``

    It will respond with messages of the form ``{"reply": <reply>, "message_id": <message_id>}``

    It treats path of ``__tick__`` as special and respond with ``{"reply": {"ok": "thankyou"}, "message_id": "__tick__"}``

    It relies on the client side closing the connection when it's finished.
    """

    log_exceptions = True

    def initialize(self, final_future, server_time, wsconnections):
        self.server_time = server_time
        self.final_future = final_future
        self.wsconnections = wsconnections

    class WSMessage(dictobj.Spec):
        path = dictobj.Field(sb.string_spec, wrapper=sb.required)
        message_id = dictobj.Field(
            sb.or_spec(sb.string_spec(), sb.tupleof(sb.string_spec())), wrapper=sb.required
        )
        body = dictobj.Field(json_spec, wrapper=sb.required)

    message_spec = WSMessage.FieldSpec()

    class Closing(object):
        pass

    def open(self):
        self.key = str(uuid.uuid1())
        self.connection_future = asyncio.Future()
        if self.final_future.done():
            self.connection_future.cancel()
            return

        canceller = lambda res: self.connection_future.cancel()
        self.final_future.add_done_callback(canceller)
        self.connection_future.add_done_callback(
            lambda res: self.final_future.remove_done_callback(canceller)
        )

        if self.server_time is not None:
            self.reply(self.server_time, message_id="__server_time__")
        self.hook("websocket_opened")

    def reply(self, msg, message_id=None, exc_info=None):
        if msg is None:
            msg = {"done": True}

        # I bypass tornado converting the dictionary so that non jsonable things can be repr'd
        if hasattr(msg, "as_dict"):
            msg = msg.as_dict()
        reply = {"reply": msg, "message_id": message_id}
        reply = json.dumps(reply, default=self.reprer).replace("</", "<\\/")

        if message_id not in ("__tick__", "__server_time__"):
            self.hook("process_reply", msg, exc_info=exc_info)

        if self.ws_connection:
            self.write_message(reply)

    def on_message(self, message):
        self.hook("websocket_message", message)
        try:
            parsed = json.loads(message)
        except (TypeError, ValueError) as error:
            self.reply({"error": "Message wasn't valid json\t{0}".format(str(error))})
            return

        if type(parsed) is dict and "path" in parsed and parsed["path"] == "__tick__":
            parsed["message_id"] = "__tick__"
            parsed["body"] = "__tick__"

        try:
            msg = self.message_spec.normalise(Meta.empty(), parsed)
        except Exception as error:
            self.hook("websocket_invalid_message", error, parsed)

            if hasattr(error, "as_dict"):
                error = error.as_dict()
            else:
                error = str(error)

            self.reply({"error_code": "InvalidMessage", "error": error})
        else:
            path = msg.path
            body = msg.body
            message_id = msg.message_id
            message_key = str(uuid.uuid4())

            if path == "__tick__":
                self.reply({"ok": "thankyou"}, message_id=message_id)
                return

            def on_processed(final, exc_info=None):
                if final is self.Closing:
                    self.reply({"closing": "goodbye"}, message_id=message_id)
                    self.close()
                else:
                    self.reply(final, message_id=message_id, exc_info=exc_info)

                try:
                    self.message_done(msg, final, message_key, exc_info=exc_info)
                except Exception as error:
                    log.exception(error)

            async def doit():
                info = {}

                def progress_cb(progress, **kwargs):
                    for m in self.transform_progress(msg, progress, **kwargs):
                        self.reply(m, message_id=message_id)

                async with self.async_catcher(info, on_processed):
                    result = await self.process_message(
                        path, body, message_id, message_key, progress_cb
                    )

                    if isinstance(result, asyncio.Future) or hasattr(result, "__await__"):
                        result = await result

                    info["result"] = result

            def done(res):
                if message_key in self.wsconnections:
                    del self.wsconnections[message_key]

                if not res.cancelled():
                    exc = res.exception()
                    if exc and self.log_exceptions:
                        log.exception(exc, exc_info=(type(exc), exc, exc.__traceback__))

            t = create_task(doit(), name=f"<process_command: {body}>")
            t.add_done_callback(done)
            self.wsconnections[message_key] = t

    def message_done(self, request, final, message_key, exc_info=None):
        """
        Hook for when we have finished processing a request

        By default nothing is done.

        request
            The original request

        final
            The last response to be sent back.

        message_key
            The uuid the server generated for this request

        exc_info
            The (exc_type, exc, traceback) for any exception that stopped the processing of the request
        """

    def transform_progress(self, body, progress, **kwargs):
        """
        Hook for transforming progress messages. This must be a generator that yields 0 or more messages

        So when the ``progress_cb`` is called like ``progress_cb("some message", arg=1)`` we will do:

        .. code-block:: python

            for m in self.transform_progress(<request>, "some message", arg=1):
                # write ``{"reply": m, "message_id": <message_id>}``

        where ``<request>`` is the entire message that started this stream.

        By default kwargs are ignored and we just yield ``{"progress": progress}`` once
        """
        yield {"progress": progress}

    async def process_message(self, path, body, message_id, message_key, progress_cb):
        """
        Return the response to be sent back when we get a message from the conn.

        path
            The uri specified in the message

        body
            The body specified in the message

        message_id
            The unique message_id for this stream of requests as supplied in the request

        message_key
            A unique id for this stream created by the server

        progress_cb
            A callback that will send a message of the form ``{"progress": <progress>, "message_id": <message_id}``
            where ``<progress>`` is the argument passed into the callback
        """
        raise NotImplementedError

    def on_close(self):
        """Hook for when a websocket connection closes"""
        self.connection_future.cancel()
