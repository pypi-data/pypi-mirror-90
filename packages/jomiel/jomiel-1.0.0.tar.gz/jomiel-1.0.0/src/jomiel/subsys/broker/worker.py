#
# jomiel
#
# Copyright
#  2019-2021 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from binascii import hexlify
from logging import DEBUG
from re import compile as rxc
from traceback import format_exc

import jomiel_messages.protobuf.v1beta1.status_pb2 as Status
from google.protobuf.message import DecodeError
from jomiel.cache import opts
from jomiel.dispatcher.media import script_dispatcher
from jomiel.error import InvalidInputError
from jomiel.error import NoParserError
from jomiel.error import ParseError
from jomiel.log import lg
from jomiel.log import log_sanitize_string
from jomiel_comm.formatter import to_json
from jomiel_kore.app import exit_error
from jomiel_messages.protobuf.v1beta1.message_pb2 import Inquiry
from jomiel_messages.protobuf.v1beta1.message_pb2 import Response
from requests.exceptions import RequestException
from validators import url as is_url
from zmq import Context
from zmq import ContextTerminated
from zmq import REP
from zmq import ZMQError


class Worker:
    """The worker class.

    Args:
        worker_id (int): the worker ID

    """

    __slots__ = ["worker_id", "context", "socket", "dealer_endpoint"]

    def __init__(self, worker_id):
        self.dealer_endpoint = opts.broker_dealer_endpoint
        (self.context, self.worker_id) = (Context.instance(), worker_id)
        self.socket = self.new_socket()

    def new_socket(self):
        """Returns a new socket that is connected to the broker (via the
        dealer endpoint).

        """
        sck = self.context.socket(REP)
        try:
            sck.connect(self.dealer_endpoint)
        except ZMQError as error:
            self.log(
                f"{error} ({self.dealer_endpoint})",
                "error",
            )
            exit_error()
        self.log("connected to <%s>" % self.dealer_endpoint)
        return sck

    def renew_socket(self):
        """Renews the zmq socket.

        Disconnects and closes the existing socket connection (to the
        broker, via the dealer endpoint, and reconnects to the dealer
        using the same endpoint.

        """
        self.socket.disconnect(self.dealer_endpoint)
        self.socket.close()
        self.socket = self.new_socket()

    def io_loop(self):
        """The I/O loop."""
        while True:
            try:
                self.log("awaiting")
                self.message_receive()
            except DecodeError as error:
                self.log(
                    "received invalid message: %s" % (error),
                    "error",
                )
                self.renew_socket()
            finally:
                self.log("reset")

    def log(self, text, msgtype="debug"):
        """Write a new (debug) worker entry to the logger."""
        logger = getattr(lg(), msgtype)
        logger(
            "subsystem/broker<worker#%03d>: %s",
            self.worker_id,
            text,
        )

    def run(self):
        """Runs the worker."""
        try:
            self.io_loop()
        except ContextTerminated as msg:
            self.log(msg)
        except KeyboardInterrupt:
            self.log("interrupted")
        finally:
            self.log("exit")

    def message_dump(self, logtext, message):
        """Dump the message details in JSON to the logger

        Ignored unless application uses the debug level.

        Args:
            logtext (string): log entry text to write
            message (obj): the message to log

        """
        if lg().level <= DEBUG:
            json = to_json(message, minified=opts.debug_minify_json)
            self.log(logtext % log_sanitize_string(json))

    def message_log_serialized(self, prefix, message):
        """Logs the given serialized message in hex format.

        Args:
            message (obj): Message to be logged

        """
        if lg().level <= DEBUG:
            _len = len(message)
            _hex = hexlify(bytearray(message))
            self.log(
                "<%s:serialized> [%s] %s"
                % (prefix, _len, log_sanitize_string(_hex)),
            )

    def message_send(self, response):
        """Sends a response message back to the client.

        Args:
            response (obj): Response message to send

        """
        serialized_response = Response.SerializeToString(response)
        self.message_log_serialized("send", serialized_response)
        self.socket.send(serialized_response)
        self.message_dump("sent: %s", response)

    def message_receive(self):
        """Awaits for an inquiry request from a client."""
        recvd_data = self.socket.recv()
        inquiry = Inquiry()

        self.message_log_serialized("recvd", recvd_data)

        inquiry.ParseFromString(recvd_data)
        self.message_dump("received: %s", inquiry)

        if inquiry.WhichOneof("inquiry") == "media":
            self.handle_media_inquiry(inquiry.media)
        else:
            # TODO: Do something useful here
            self.log("ignored unknown inquiry type")

    def handle_media_inquiry(self, inquiry):
        """Handles the incoming inquiry requests."""

        def match_handler():
            """Matches the given input URI to a script.

            Returns:
                obj: A subclass of PluginMediaParser

                    The object data consists of parsed meta data as
                    returned for the input URI.

            """
            return script_dispatcher(inquiry.input_uri)

        def validate_input_uri():
            """Validate the input URI unless configured to skip this."""
            if opts.broker_input_allow_any:
                return

            if not is_url(inquiry.input_uri):
                raise InvalidInputError(
                    "Invalid input URI value given <%s>"
                    % inquiry.input_uri,
                )

        def failed(error):
            """Check if an error occurred."""
            builder = ResponseBuilder(error)
            self.message_send(builder.response)

        try:
            validate_input_uri()
            handler = match_handler()
            self.message_send(handler.response)
        except Exception as error:
            failed(error)


def worker_new(worker_id):
    """Creates a new worker objecta

    Args:
        worker_id (int): the worker ID

    """
    Worker(worker_id).run()


class ResponseBuilder:
    """Builds a new Response (protobuf) message which is sent back to to
    client.

    Determines the message content based on the exception passed to the
    class.

    Args:
        error (obj): an exception that occurred while processing the
            input URI (or leave None, if none occurred)

    Attributes:
        response (obj): the created Response object

    """

    __slots__ = ["response"]

    def __init__(self, error=None):
        self.response = Response()
        self.init(
            "Not an error",
            Status.STATUS_CODE_OK,
            Status.ERROR_CODE_UNSPECIFIED,
        )
        if error:
            self.determine(error)

    def determine(self, error):
        """Determine error, and set the response values to indicates
        this.

        Args:
            error (obj): the raised exception

        """
        error_type = type(error)

        if error_type == ParseError:
            self.parse_failed(error)
        elif error_type == NoParserError:
            self.handler_not_found(error)
        elif error_type == InvalidInputError:
            self.invalid_input_given(error)
        else:
            if not self.is_requests_error(error, error_type):
                self.fail_with_traceback()

    def init(self, msg, status, error, http=200):
        """Initialize the response with the given values.

        Args:
            msg (string): explanation of the error
            status (int): status code (see status.proto)
            error (int): error code (see status.proto)
            http (int): HTTP code (default is 200)

        """
        self.response.status.http.code = http
        self.response.status.message = msg
        self.response.status.code = status
        self.response.status.error = error
        return True

    def parse_failed(self, error):
        """System raised ParseError, initalize response accordingly."""
        self.init(
            error.message,
            Status.STATUS_CODE_INTERNAL_SERVER,
            Status.ERROR_CODE_PARSE,
        )

    def handler_not_found(self, error):
        """System raised NoParserError, initalize response accordingly."""
        self.init(
            error.message,
            Status.STATUS_CODE_NOT_IMPLEMENTED,
            Status.ERROR_CODE_NO_PARSER,
        )

    def invalid_input_given(self, error):
        """System raised InvalidInputError, initialize response accordingly."""
        self.init(
            error.message,
            Status.STATUS_CODE_BAD_REQUEST,
            Status.ERROR_CODE_INVALID_INPUT,
        )

    def is_requests_error(self, error, error_type):
        """Handle Requests error (if any)

        If Requests error occurred, initialize response accordingly,
        otherwise fall through.

        Args:
            error (obj): the raised exception
            error_type (obj): the type of the exception

        """
        if issubclass(error_type, RequestException):

            def get_http_code():
                """Return HTTP code from the HTTP header."""
                regex = rxc(r"^(\d{3}) Server Error:")
                result = regex.match(message)
                return result.group(1) if result else 200

            message = str(error)
            code = get_http_code()

            return self.init(
                message,
                Status.STATUS_CODE_INTERNAL_SERVER,
                Status.ERROR_CODE_HTTP,
                code,
            )
        return False

    def fail_with_traceback(self):
        """Pass the Python stack traceback to the client."""
        self.init(
            format_exc(),
            Status.STATUS_CODE_INTERNAL_SERVER,
            Status.ERROR_CODE_UNKNOWN_SEE_MESSAGE,
        )


# vim: set ts=4 sw=4 tw=72 expandtab:
