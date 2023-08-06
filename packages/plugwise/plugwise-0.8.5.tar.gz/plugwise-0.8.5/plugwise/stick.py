"""
Use of this source code is governed by the MIT license found in the LICENSE file.

Main stick object to control associated plugwise plugs
"""
from datetime import datetime, timedelta
import logging
import queue
import sys
import threading
import time

from plugwise.connections.serial import PlugwiseUSBConnection
from plugwise.connections.socket import SocketConnection
from plugwise.constants import (
    ACCEPT_JOIN_REQUESTS,
    ACK_ACCEPT_JOINING_REQUEST,
    ACK_CLOCK_SET,
    ACK_ERROR,
    ACK_OFF,
    ACK_ON,
    ACK_SCAN_PARAMETERS_SET,
    ACK_SLEEP_SET,
    ACK_SUCCESS,
    ACK_TIMEOUT,
    CB_JOIN_REQUEST,
    CB_NEW_NODE,
    MESSAGE_RETRY,
    MESSAGE_TIME_OUT,
    NACK_ON_OFF,
    NACK_REAL_TIME_CLOCK_SET,
    NACK_SCAN_PARAMETERS_SET,
    NACK_SLEEP_SET,
    NODE_TYPE_CELSIUS_NR,
    NODE_TYPE_CELSIUS_SED,
    NODE_TYPE_CIRCLE,
    NODE_TYPE_CIRCLE_PLUS,
    NODE_TYPE_SCAN,
    NODE_TYPE_SENSE,
    NODE_TYPE_STEALTH,
    NODE_TYPE_SWITCH,
    SLEEP_TIME,
    UTF8_DECODE,
    WATCHDOG_DEAMON,
)
from plugwise.exceptions import (
    CirclePlusError,
    NetworkDown,
    PortError,
    StickInitError,
    TimeoutException,
)
from plugwise.messages.requests import (
    CircleCalibrationRequest,
    CircleClockGetRequest,
    CirclePlusRealTimeClockGetRequest,
    CirclePlusScanRequest,
    CirclePowerUsageRequest,
    CircleSwitchRelayRequest,
    NodeAddRequest,
    NodeAllowJoiningRequest,
    NodeInfoRequest,
    NodePingRequest,
    NodeRemoveRequest,
    NodeRequest,
    StickInitRequest,
)
from plugwise.messages.responses import (
    CircleCalibrationResponse,
    CircleClockResponse,
    CirclePlusRealTimeClockResponse,
    CirclePlusScanResponse,
    CirclePowerUsageResponse,
    NodeAckLargeResponse,
    NodeAckResponse,
    NodeAckSmallResponse,
    NodeAwakeResponse,
    NodeInfoResponse,
    NodeJoinAckResponse,
    NodeJoinAvailableResponse,
    NodePingResponse,
    NodeRemoveResponse,
    NodeResponse,
    StickInitResponse,
)
from plugwise.node import PlugwiseNode
from plugwise.nodes.circle import PlugwiseCircle
from plugwise.nodes.circle_plus import PlugwiseCirclePlus
from plugwise.nodes.scan import PlugwiseScan
from plugwise.nodes.sense import PlugwiseSense
from plugwise.nodes.stealth import PlugwiseStealth
from plugwise.parser import PlugwiseParser
from plugwise.util import inc_seq_id, validate_mac

_LOGGER = logging.getLogger(__name__)


class stick:
    """Plugwise connection stick."""

    def __init__(self, port, callback=None):
        self._mac_stick = None
        self.port = port
        self.network_online = False
        self.circle_plus_mac = None
        self._circle_plus_discovered = False
        self._circle_plus_retries = 0
        self.network_id = None
        self.parser = PlugwiseParser(self)
        self._plugwise_nodes = {}
        self._nodes_registered = 0
        self._nodes_to_discover = {}
        self._nodes_not_discovered = {}
        self._nodes_off_line = 0
        self._discovery_finished = False
        self._messages_for_undiscovered_nodes = []
        self._accept_join_requests = ACCEPT_JOIN_REQUESTS
        self._stick_initialized = False
        self._stick_callbacks = {}
        self.last_ack_seq_id = None
        self.expected_responses = {}
        self.timezone_delta = datetime.now().replace(
            minute=0, second=0, microsecond=0
        ) - datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        self._run_receive_timeout_thread = False
        self._run_send_message_thread = False
        self._run_update_thread = False

        self._auto_update_timer = 0
        self._nodes_discovered = None
        self._receive_timeout_thread = None
        self._run_watchdog = None
        self._send_message_queue = None
        self._send_message_thread = None
        self._update_thread = None
        self._watchdog_thread = None
        self.init_callback = None
        self.connection = None

        if callback:
            self.auto_initialize(callback)

    def auto_initialize(self, callback=None):
        """ automatic initialization """

        def init_finished():
            if not self.network_online:
                _LOGGER.Error("plugwise Zigbee network down")
            else:
                self.scan(callback)

        try:
            self.connect()
            self.initialize_stick(init_finished)
        except PortError as e:
            _LOGGER.error("Failed to connect: '%s'", e)
        except StickInitError as e:
            _LOGGER.error("Failed to initialize USBstick: '%s'", e)
        except NetworkDown:
            _LOGGER.error("Failed to communicated: Plugwise Zigbee network")
        except TimeoutException:
            _LOGGER.error("Timeout exception while initializing USBstick")
        except Exception as e:
            _LOGGER.error("Unknown error : %s", e)

    def connect(self, callback=None):
        """ Connect to stick and raise error if it fails"""
        self.init_callback = callback
        # Open connection to USB Stick
        if ":" in self.port:
            _LOGGER.debug("Open socket connection to Plugwise Zigbee stick")
            self.connection = SocketConnection(self.port, self)
        else:
            _LOGGER.debug("Open USB serial connection to Plugwise Zigbee stick")
            self.connection = PlugwiseUSBConnection(self.port, self)
        self.connection.connect()

        _LOGGER.debug("Starting threads...")
        # receive timeout daemon
        self._run_receive_timeout_thread = True
        self._receive_timeout_thread = threading.Thread(
            None, self._receive_timeout_loop, "receive_timeout_thread", (), {}
        )
        self._receive_timeout_thread.daemon = True
        self._receive_timeout_thread.start()
        # send daemon
        self._send_message_queue = queue.Queue()
        self._run_send_message_thread = True
        self._send_message_thread = threading.Thread(
            None, self._send_message_loop, "send_messages_thread", (), {}
        )
        self._send_message_thread.daemon = True
        self._send_message_thread.start()
        # update daemon
        self._run_update_thread = False
        self._auto_update_timer = 0
        self._update_thread = threading.Thread(
            None, self._update_loop, "update_thread", (), {}
        )
        self._update_thread.daemon = True
        _LOGGER.debug("All threads started")

    def initialize_stick(self, callback=None, timeout=MESSAGE_TIME_OUT):
        # Initialize USBstick
        if not self.connection.is_connected():
            raise StickInitError

        def cb_stick_initialized():
            """ Callback when initialization of Plugwise USBstick is finished """
            self._stick_initialized = True

            # Start watchdog daemon
            self._run_watchdog = True
            self._watchdog_thread = threading.Thread(
                None, self._watchdog_loop, "watchdog_thread", (), {}
            )
            self._watchdog_thread.daemon = True
            self._watchdog_thread.start()

            # Try to discover Circle+
            if self.circle_plus_mac:
                self.discover_node(self.circle_plus_mac)
            if callback:
                callback()

        _LOGGER.debug("Send init request to Plugwise Zigbee stick")
        self.send(StickInitRequest(), cb_stick_initialized)
        time_counter = 0
        while not self._stick_initialized and (time_counter < timeout):
            time_counter += 0.1
            time.sleep(0.1)
        if not self._stick_initialized:
            raise StickInitError
        if not self.network_online:
            raise NetworkDown

    def initialize_circle_plus(self, callback=None, timeout=MESSAGE_TIME_OUT):
        # Initialize Circle+
        if (
            not self.connection.is_connected()
            or not self._stick_initialized
            or not self.circle_plus_mac
        ):
            raise StickInitError
        # discover circle+ node
        self.discover_node(self.circle_plus_mac)

        time_counter = 0
        while not self._circle_plus_discovered and (time_counter < timeout):
            time_counter += 0.1
            time.sleep(0.1)
        if not self._circle_plus_discovered:
            raise CirclePlusError

    def disconnect(self):
        """ Disconnect from stick and raise error if it fails"""
        self._run_watchdog = False
        self._run_update_thread = False
        self._auto_update_timer = 0
        self._run_send_message_thread = False
        self._run_receive_timeout_thread = False
        self.connection.disconnect()

    def subscribe_stick_callback(self, callback, callback_type):
        """ Subscribe callback to execute """
        if callback_type not in self._stick_callbacks:
            self._stick_callbacks[callback_type] = []
        self._stick_callbacks[callback_type].append(callback)

    def unsubscribe_stick_callback(self, callback, callback_type):
        """ Register callback to execute """
        if callback_type in self._stick_callbacks:
            self._stick_callbacks[callback_type].remove(callback)

    def do_callback(self, callback_type, callback_arg=None):
        """ Execute callbacks registered for specified callback type """
        if callback_type in self._stick_callbacks:
            for callback in self._stick_callbacks[callback_type]:
                try:
                    if callback_arg is None:
                        callback()
                    else:
                        callback(callback_arg)
                except Exception as e:
                    _LOGGER.error("Error while executing callback : %s", e)

    def _discover_after_scan(self):
        """ Helper to do callback for new node """
        node_discovered = None
        for mac in self._nodes_not_discovered:
            if self._plugwise_nodes.get(mac, None):
                node_discovered = mac
                break
        if node_discovered:
            del self._nodes_not_discovered[node_discovered]
            self.do_callback(CB_NEW_NODE, node_discovered)

    def registered_nodes(self) -> int:
        """ Return number of nodes registered in Circle+ """
        # Include Circle+ too
        return self._nodes_registered + 1

    def nodes(self) -> list:
        """ Return list of mac addresses of discovered and supported plugwise nodes """
        return list(
            dict(
                filter(lambda item: item[1] is not None, self._plugwise_nodes.items())
            ).keys()
        )

    def node(self, mac: str) -> PlugwiseNode:
        """ Return specific Plugwise node object"""
        return self._plugwise_nodes.get(mac, None)

    def discover_node(self, mac: str, callback=None, force_discover=False) -> bool:
        """ Discovery of plugwise node """
        if validate_mac(mac):
            if not self._plugwise_nodes.get(mac):
                if mac not in self._nodes_not_discovered.keys():
                    self._nodes_not_discovered[mac] = (
                        None,
                        None,
                    )
                    self.send(
                        NodeInfoRequest(bytes(mac, UTF8_DECODE)),
                        callback,
                    )
                else:
                    (firstrequest, lastrequest) = self._nodes_not_discovered[mac]
                    if not (firstrequest and lastrequest):
                        self.send(
                            NodeInfoRequest(bytes(mac, UTF8_DECODE)),
                            callback,
                        )
                    elif force_discover:
                        self.send(
                            NodeInfoRequest(bytes(mac, UTF8_DECODE)),
                            callback,
                        )
                return True
            return False
        return False

    def scan(self, callback=None):  # noqa: C901
        """ scan for connected plugwise nodes """
        # TODO: flake8 indicates scan is too complex, level 23 indenting is indeed complex

        def scan_finished(nodes_to_discover):
            """ Callback when scan is finished """
            time.sleep(1)
            _LOGGER.debug("Scan plugwise network finished")
            self._nodes_discovered = 0
            self._nodes_to_discover = nodes_to_discover
            self._nodes_registered = len(nodes_to_discover)
            self._discovery_finished = False

            def node_discovered(nodes_off_line=False):
                if nodes_off_line:
                    self._nodes_off_line += 1
                self._nodes_discovered += 1
                _LOGGER.debug(
                    "Discovered Plugwise node %s (%s off-line) of %s",
                    str(len(self._plugwise_nodes)),
                    str(self._nodes_off_line),
                    str(len(self._nodes_to_discover)),
                )
                if (len(self._plugwise_nodes) - 1 + self._nodes_off_line) >= len(
                    self._nodes_to_discover
                ):
                    if self._nodes_off_line == 0:
                        self._nodes_to_discover = {}
                        self._nodes_not_discovered = {}
                    else:
                        for mac in self._nodes_to_discover:
                            if mac not in self._plugwise_nodes.keys():
                                _LOGGER.info(
                                    "Failed to discover node type for registered MAC '%s'. This is expected for battery powered nodes, they will be discovered at their first awake",
                                    str(mac),
                                )
                            else:
                                if mac in self._nodes_not_discovered:
                                    del self._nodes_not_discovered[mac]
                    self._discovery_finished = True
                    if callback:
                        callback()

            def timeout_expired():
                if not self._discovery_finished:
                    for mac in self._nodes_to_discover:
                        if mac not in self._plugwise_nodes.keys():
                            _LOGGER.info(
                                "Failed to discover node type for registered MAC '%s'. This is expected for battery powered nodes, they will be discovered at their first awake",
                                str(mac),
                            )
                        else:
                            if mac in self._nodes_not_discovered:
                                del self._nodes_not_discovered[mac]
                    if callback:
                        callback()

            # setup timeout for loading nodes
            discover_timeout = (
                10 + (len(nodes_to_discover) * 2) + (MESSAGE_TIME_OUT * MESSAGE_RETRY)
            )
            threading.Timer(discover_timeout, timeout_expired).start()
            _LOGGER.debug("Start discovery of linked node types...")
            for mac in nodes_to_discover:
                self.discover_node(mac, node_discovered)

        def scan_circle_plus():
            """Callback when Circle+ is discovered"""
            if self._plugwise_nodes.get(self.circle_plus_mac):
                _LOGGER.debug("Scan Circle+ for linked nodes...")
                self._plugwise_nodes[self.circle_plus_mac].scan_for_nodes(scan_finished)
            else:
                _LOGGER.error("Circle+ is not discovered in %s", self._plugwise_nodes)

        # Discover Circle+
        if self.circle_plus_mac:
            if self._plugwise_nodes.get(self.circle_plus_mac):
                scan_circle_plus()
            else:
                _LOGGER.debug("Discover Circle+ at %s", self.circle_plus_mac)
                self.discover_node(self.circle_plus_mac, scan_circle_plus)
        else:
            _LOGGER.error(
                "Plugwise stick not properly initialized, Circle+ MAC is missing."
            )

    def get_mac_stick(self) -> str:
        """Return mac address of USB-Stick"""
        if self._mac_stick:
            return self._mac_stick.decode(UTF8_DECODE)
        return None

    def allow_join_requests(self, enable: bool, accept: bool):
        """
        Enable or disable Plugwise network
        Automatically accept new join request
        """
        self.send(NodeAllowJoiningRequest(enable))
        if enable:
            self._accept_join_requests = accept
        else:
            self._accept_join_requests = False

    def node_join(self, mac: str, callback=None) -> bool:
        """Accept node to join Plugwise network by adding it in Circle+ memory"""
        if validate_mac(mac):
            self.send(NodeAddRequest(bytes(mac, UTF8_DECODE), True), callback)
            return True

        _LOGGER.warning("Invalid mac '%s' address, unable to join node manually.", mac)
        return False

    def node_unjoin(self, mac: str, callback=None) -> bool:
        """Remove node from the Plugwise network by deleting it from the Circle+ memory"""
        if validate_mac(mac):
            self.send(
                NodeRemoveRequest(bytes(self.circle_plus_mac, UTF8_DECODE), mac),
                callback,
            )
            return True

        _LOGGER.warning(
            "Invalid mac '%s' address, unable to unjoin node manually.", mac
        )
        return False

    def _append_node(self, mac, address, node_type):
        """ Add Plugwise node to be controlled """
        _LOGGER.debug(
            "Add new node type (%s) with mac %s",
            str(node_type),
            mac,
        )
        if node_type == NODE_TYPE_CIRCLE_PLUS:
            self._plugwise_nodes[mac] = PlugwiseCirclePlus(mac, address, self)
        elif node_type == NODE_TYPE_CIRCLE:
            self._plugwise_nodes[mac] = PlugwiseCircle(mac, address, self)
        elif node_type == NODE_TYPE_SWITCH:
            self._plugwise_nodes[mac] = None
        elif node_type == NODE_TYPE_SENSE:
            self._plugwise_nodes[mac] = PlugwiseSense(mac, address, self)
        elif node_type == NODE_TYPE_SCAN:
            self._plugwise_nodes[mac] = PlugwiseScan(mac, address, self)
        elif node_type == NODE_TYPE_CELSIUS_SED:
            self._plugwise_nodes[mac] = None
        elif node_type == NODE_TYPE_CELSIUS_NR:
            self._plugwise_nodes[mac] = None
        elif node_type == NODE_TYPE_STEALTH:
            self._plugwise_nodes[mac] = PlugwiseStealth(mac, address, self)
        else:
            _LOGGER.warning("Unsupported node type '%s'", str(node_type))
            self._plugwise_nodes[mac] = None

        # process previous missed messages
        msg_to_process = self._messages_for_undiscovered_nodes[:]
        self._messages_for_undiscovered_nodes = []
        for msg in msg_to_process:
            self.new_message(msg)

    def _remove_node(self, mac):
        """
        remove circle from stick

        :return: None
        """
        if mac in self._plugwise_nodes:
            del self._plugwise_nodes[mac]

    def feed_parser(self, data):
        """ Feed parser with new data """
        assert isinstance(data, bytes)
        self.parser.feed(data)

    def send(self, request, callback=None, retry_counter=0):
        """
        Submit request message into Plugwise Zigbee network and queue expected response
        """
        assert isinstance(request, NodeRequest)
        if isinstance(request, CirclePowerUsageRequest):
            response_message = CirclePowerUsageResponse()
        elif isinstance(request, NodeInfoRequest):
            response_message = NodeInfoResponse()
        elif isinstance(request, NodePingRequest):
            response_message = NodePingResponse()
        elif isinstance(request, CircleSwitchRelayRequest):
            response_message = NodeAckLargeResponse()
        elif isinstance(request, CircleCalibrationRequest):
            response_message = CircleCalibrationResponse()
        elif isinstance(request, CirclePlusScanRequest):
            response_message = CirclePlusScanResponse()
        elif isinstance(request, CirclePlusRealTimeClockGetRequest):
            response_message = CirclePlusRealTimeClockResponse()
        elif isinstance(request, CircleClockGetRequest):
            response_message = CircleClockResponse()
        elif isinstance(request, StickInitRequest):
            response_message = StickInitResponse()
        else:
            response_message = None
        self._send_message_queue.put(
            [
                response_message,
                request,
                callback,
                retry_counter,
                None,
            ]
        )

    def _send_message_loop(self):
        """Daemon to send messages waiting in queue."""
        while self._run_send_message_thread:
            try:
                request_set = self._send_message_queue.get(block=True, timeout=1)
            except queue.Empty:
                time.sleep(SLEEP_TIME)
            else:
                if self.last_ack_seq_id:
                    # Calc new seq_id based last received ack message
                    seq_id = inc_seq_id(self.last_ack_seq_id)
                else:
                    # first message, so use a fake seq_id
                    seq_id = b"0000"
                self.expected_responses[seq_id] = request_set
                if (
                    not isinstance(request_set[1], StickInitRequest)
                    and not isinstance(request_set[1], NodeAllowJoiningRequest)
                    and not isinstance(request_set[1], NodeAddRequest)
                ):
                    mac = request_set[1].mac.decode(UTF8_DECODE)
                    _LOGGER.info(
                        "send %s to %s using seq_id %s",
                        request_set[1].__class__.__name__,
                        mac,
                        str(seq_id),
                    )
                    if self._plugwise_nodes.get(mac):
                        self._plugwise_nodes[mac].last_request = datetime.now()
                    if self.expected_responses[seq_id][3] > 0:
                        _LOGGER.debug(
                            "Retry %s for message %s to %s",
                            str(self.expected_responses[seq_id][3]),
                            str(self.expected_responses[seq_id][1].__class__.__name__),
                            self.expected_responses[seq_id][1].mac.decode(UTF8_DECODE),
                        )
                else:
                    mac = ""
                    _LOGGER.info(
                        "send %s using seq_id %s",
                        request_set[1].__class__.__name__,
                        str(seq_id),
                    )
                self.expected_responses[seq_id][4] = datetime.now()
                self.connection.send(request_set[1])
                time.sleep(SLEEP_TIME)
                timeout_counter = 0
                # Wait max 1 second for acknowledge response
                while (
                    self.last_ack_seq_id != seq_id
                    and timeout_counter <= 10
                    and seq_id != b"0000"
                    and self.last_ack_seq_id is not None
                ):
                    time.sleep(0.1)
                    timeout_counter += 1
                if timeout_counter > 10 and self._run_send_message_thread:
                    if seq_id in self.expected_responses:
                        if self.expected_responses[seq_id][3] <= MESSAGE_RETRY:
                            _LOGGER.info(
                                "Resend %s for %s because stick did not acknowledge request (%s), last seq_id=%s",
                                str(
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__
                                ),
                                mac,
                                str(seq_id),
                                str(self.last_ack_seq_id),
                            )
                            self.send(
                                self.expected_responses[seq_id][1],
                                self.expected_responses[seq_id][2],
                                self.expected_responses[seq_id][3] + 1,
                            )
                        else:
                            _LOGGER.info(
                                "Drop %s request with seq_id %s for mac %s because max (%s) retries reached, last seq_id=%s",
                                self.expected_responses[seq_id][1].__class__.__name__,
                                str(seq_id),
                                mac,
                                str(MESSAGE_RETRY),
                                str(self.last_ack_seq_id),
                            )
                        del self.expected_responses[seq_id]
        _LOGGER.debug("Send message loop stopped")

    def _receive_timeout_loop(self):
        """Daemon to time out requests without any (n)ack response message."""
        while self._run_receive_timeout_thread:
            for seq_id in list(self.expected_responses.keys()):
                if self.expected_responses[seq_id][4] is not None:
                    if self.expected_responses[seq_id][4] < (
                        datetime.now() - timedelta(seconds=MESSAGE_TIME_OUT)
                    ):
                        _LOGGER.debug(
                            "Timeout expired for message with sequence ID %s",
                            str(seq_id),
                        )
                        if self.expected_responses[seq_id][3] <= MESSAGE_RETRY:
                            _LOGGER.debug(
                                "Resend request %s",
                                str(
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__
                                ),
                            )
                            self.send(
                                self.expected_responses[seq_id][1],
                                self.expected_responses[seq_id][2],
                                self.expected_responses[seq_id][3] + 1,
                            )
                        else:
                            if isinstance(
                                self.expected_responses[seq_id][1], NodeAddRequest
                            ) or isinstance(
                                self.expected_responses[seq_id][1], StickInitRequest
                            ):
                                _LOGGER.info(
                                    "Drop %s request because max (%s) retries reached for seq id %s",
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__,
                                    str(MESSAGE_RETRY),
                                    str(seq_id),
                                )
                            else:
                                if self.expected_responses[seq_id][1].mac == "":
                                    mac = "<empty>"
                                else:
                                    mac = self.expected_responses[seq_id][1].mac.decode(
                                        UTF8_DECODE
                                    )
                                _LOGGER.info(
                                    "Drop %s request for mac %s because max (%s) retries reached for seq id %s",
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__,
                                    mac,
                                    str(MESSAGE_RETRY),
                                    str(seq_id),
                                )
                        del self.expected_responses[seq_id]
            receive_timeout_checker = 0
            while (
                receive_timeout_checker < MESSAGE_TIME_OUT
                and self._run_receive_timeout_thread
            ):
                time.sleep(1)
                receive_timeout_checker += 1
        _LOGGER.debug("Receive timeout loop stopped")

    def new_message(self, message: NodeResponse):  # noqa: C901
        """ Received message from Plugwise Zigbee network """
        # TODO: flake8 indicates scan is too complex, level 47! indenting is indeed overly complex

        # only save last seq_id and skip special ID's FFFD, FFFE, FFFF
        if self.last_ack_seq_id:
            if int(self.last_ack_seq_id, 16) < int(message.seq_id, 16) < 65533:
                self.last_ack_seq_id = message.seq_id
            elif message.seq_id == b"0000":
                self.last_ack_seq_id = b"0000"

        if not isinstance(message, NodeAckSmallResponse):
            mac = message.mac.decode(UTF8_DECODE)
            if not isinstance(message, NodeAckLargeResponse):
                _LOGGER.info(
                    "Received %s from %s with seq_id %s",
                    message.__class__.__name__,
                    mac,
                    str(message.seq_id),
                )

        if isinstance(message, NodeAckSmallResponse):
            if message.ack_id == ACK_SUCCESS:
                _LOGGER.debug(
                    "Received success response for request with sequence id %s",
                    str(message.seq_id),
                )
                self.message_processed(message.seq_id, message.ack_id, True)
            elif message.ack_id == ACK_TIMEOUT:
                _LOGGER.info(
                    "Received timeout response for request with sequence id %s",
                    str(message.seq_id),
                )
                self.message_processed(message.seq_id, message.ack_id, True)
            elif message.ack_id == ACK_ERROR:
                _LOGGER.info(
                    "Received error response for request with sequence id %s",
                    str(message.seq_id),
                )
                self.message_processed(message.seq_id, message.ack_id, True)
            else:
                if self.expected_responses.get(message.seq_id):
                    _LOGGER.info(
                        "Received unmanaged NodeAckSmallResponse %s message for request %s with sequence id %s",
                        str(message.ack_id),
                        str(
                            self.expected_responses[message.seq_id][
                                1
                            ].__class__.__name__
                        ),
                        str(message.seq_id),
                    )
                else:
                    _LOGGER.info(
                        "Received unmanaged NodeAckSmallResponse %s message for unknown request with sequence id %s",
                        str(message.ack_id),
                        str(message.seq_id),
                    )
        elif isinstance(message, NodeAckLargeResponse):
            if self._plugwise_nodes.get(mac):
                if message.ack_id == ACK_ON:
                    _LOGGER.info(
                        "Received relay switched on in response for CircleSwitchRelayRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self._plugwise_nodes[mac].on_message(message)
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == ACK_OFF:
                    _LOGGER.info(
                        "Received relay switched off in response for CircleSwitchRelayRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self._plugwise_nodes[mac].on_message(message)
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == NACK_ON_OFF:
                    _LOGGER.info(
                        "Received failed response for CircleSwitchRelayRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == ACK_SLEEP_SET:
                    _LOGGER.info(
                        "Received success sleep configuration response for NodeSleepConfigRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self._plugwise_nodes[mac].on_message(message)
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == NACK_SLEEP_SET:
                    _LOGGER.warning(
                        "Received failed sleep configuration response for NodeSleepConfigRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self._plugwise_nodes[mac].on_message(message)
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == ACK_ACCEPT_JOINING_REQUEST:
                    _LOGGER.info(
                        "Received success response for NodeAllowJoiningRequest from (circle+) %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == ACK_CLOCK_SET:
                    _LOGGER.info(
                        "Received success response for CircleClockSetRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self.message_processed(message.seq_id, message.ack_id)
                else:
                    if self.expected_responses.get(message.seq_id):
                        _LOGGER.info(
                            "Received unmanaged NodeAckLargeResponse %s message from %s for request %s with sequence id %s",
                            str(message.ack_id),
                            mac,
                            str(
                                self.expected_responses[message.seq_id][
                                    1
                                ].__class__.__name__
                            ),
                            str(message.seq_id),
                        )
                    else:
                        _LOGGER.info(
                            "Received unmanaged NodeAckLargeResponse %s message from %s for unknown request with sequence id %s",
                            str(message.ack_id),
                            mac,
                            str(message.seq_id),
                        )
            else:
                _LOGGER.info(
                    "Received NodeAckLargeResponse %s message from unknown node %s with sequence id %s",
                    str(message.ack_id),
                    mac,
                    str(message.seq_id),
                )
        elif isinstance(message, NodeAckResponse):
            if self._plugwise_nodes.get(mac):
                if message.ack_id == ACK_SCAN_PARAMETERS_SET:
                    _LOGGER.info(
                        "Received success response for ScanConfigureRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self._plugwise_nodes[mac].on_message(message)
                    self.message_processed(message.seq_id, message.ack_id)
                elif message.ack_id == NACK_SCAN_PARAMETERS_SET:
                    _LOGGER.info(
                        "Received failed response for ScanConfigureRequest from %s with sequence id %s",
                        mac,
                        str(message.seq_id),
                    )
                    self.message_processed(message.seq_id, message.ack_id)
                else:
                    if self.expected_responses.get(message.seq_id):
                        _LOGGER.info(
                            "Received unmanaged NodeAckResponse %s message from %s for request %s with sequence id %s",
                            str(message.ack_id),
                            mac,
                            str(
                                self.expected_responses[message.seq_id][
                                    1
                                ].__class__.__name__
                            ),
                            str(message.seq_id),
                        )
                    else:
                        _LOGGER.info(
                            "Received unmanaged NodeAckResponse %s message from %s for unknown request with sequence id %s",
                            str(message.ack_id),
                            mac,
                            str(message.seq_id),
                        )
            else:
                _LOGGER.info(
                    "Received NodeAckResponse %s message from unknown node %s with sequence id %s",
                    str(message.ack_id),
                    mac,
                    str(message.seq_id),
                )
        elif isinstance(message, StickInitResponse):
            self._mac_stick = message.mac
            if message.network_is_online.value == 1:
                self.network_online = True
            else:
                self.network_online = False
            # Replace first 2 characters by 00 for mac of circle+ node
            self.circle_plus_mac = "00" + message.circle_plus_mac.value[2:].decode(
                UTF8_DECODE
            )
            self.network_id = message.network_id.value
            # The first StickInitResponse gives the actual sequence ID
            if b"0000" in self.expected_responses:
                seq_id = b"0000"
            else:
                seq_id = message.seq_id
            self.message_processed(seq_id)
        elif isinstance(message, NodeInfoResponse):
            _LOGGER.debug(
                "Received node info (%s) for NodeInfoRequest from %s with sequence id %s",
                str(message.node_type.value),
                mac,
                str(message.seq_id),
            )
            if mac not in self._plugwise_nodes:
                if message.node_type.value == NODE_TYPE_CIRCLE_PLUS:
                    self._circle_plus_discovered = True
                    self._append_node(mac, 0, message.node_type.value)
                    if mac in self._nodes_not_discovered:
                        del self._nodes_not_discovered[mac]
                else:
                    for mac_to_discover in self._nodes_to_discover:
                        if mac == mac_to_discover:
                            self._append_node(
                                mac,
                                self._nodes_to_discover[mac_to_discover],
                                message.node_type.value,
                            )
            if self._plugwise_nodes.get(mac):
                self._plugwise_nodes[mac].on_message(message)
                self.message_processed(message.seq_id)
        elif isinstance(message, NodeAwakeResponse):
            # Message from SED node notifying it is currently awake.
            # If node is not known do discovery first.
            _LOGGER.info(
                "Received NodeAwakeResponse message (%s) from %s with sequence id %s",
                str(message.awake_type.value),
                mac,
                str(message.seq_id),
            )
            if self._plugwise_nodes.get(mac):
                self._plugwise_nodes[mac].on_message(message)
            else:
                _LOGGER.info(
                    "Received NodeAwakeResponse message from unknown node with mac %s with sequence id %s, do discovery now",
                    mac,
                    str(message.seq_id),
                )
                self.discover_node(mac, self._discover_after_scan, True)
        elif isinstance(message, NodeJoinAvailableResponse):
            # Message from node that is not part of a plugwise network yet and wants to join
            _LOGGER.info(
                "Received NodeJoinAvailableResponse from node with mac %s",
                mac,
            )
            if not self._plugwise_nodes.get(mac):
                if self._accept_join_requests:
                    # Send accept join request
                    _LOGGER.info(
                        "Accepting network join request for node with mac %s",
                        mac,
                    )
                    self.send(NodeAddRequest(bytes(mac, UTF8_DECODE), True))
                    self.discover_node(mac, self._discover_after_scan)
                else:
                    _LOGGER.debug(
                        "New node with mac %s requesting to join Plugwise network, do callback",
                        mac,
                    )
                    self.do_callback(CB_JOIN_REQUEST, mac)
            else:
                _LOGGER.debug(
                    "Received node available message for node %s which is already joined.",
                    mac,
                )
        elif isinstance(message, NodeJoinAckResponse):
            # Notification message when node (re)joined existing network again.
            # Received when a SED (re)joins the network e.g. when you reinsert the battery of a Scan
            _LOGGER.info(
                "Received NodeJoinAckResponse from %s which has accepted or (re)joined this Plugwise network",
                mac,
            )
            if not self._plugwise_nodes.get(mac):
                self.discover_node(mac, self._discover_after_scan, True)
        elif isinstance(message, NodeRemoveResponse):
            # Conformation message a node is is removed from the Plugwise network
            unjoined_mac = message.node_mac_id.value
            if message.status.value == 1:
                if self._plugwise_nodes.get(unjoined_mac):
                    del self._plugwise_nodes[unjoined_mac]
                    _LOGGER.info(
                        "Received NodeRemoveResponse from node %s it has been unjoined from Plugwise network",
                        unjoined_mac,
                    )
                else:
                    _LOGGER.debug(
                        "Unknown node with mac %s has been unjoined from Plugwise network",
                        unjoined_mac,
                    )
            else:
                _LOGGER.warning(
                    "Node with mac %s failed to unjoin from Plugwise network ",
                    unjoined_mac,
                )
        else:
            if self._plugwise_nodes.get(mac):
                self._plugwise_nodes[mac].on_message(message)
                self.message_processed(message.seq_id)
            else:
                _LOGGER.info(
                    "Queue %s message because node with mac %s is not discovered yet.",
                    message.__class__.__name__,
                    mac,
                )
                self._messages_for_undiscovered_nodes.append(message)
                self.discover_node(mac)

    def message_processed(  # noqa: C901
        self, seq_id, ack_response=None, ack_small=False
    ):
        """ Execute callback of received messages """
        # TODO: flake8 indicates scan is too complex, level 34! indenting is indeed too complex
        do_callback = False
        do_resend = False
        if seq_id in self.expected_responses:
            _LOGGER.debug(
                "Process response to %s with seq id %s",
                self.expected_responses[seq_id][0].__class__.__name__,
                str(seq_id),
            )
            if self.expected_responses[seq_id][1].mac == "":
                mac = "<unknown>"
            else:
                mac = self.expected_responses[seq_id][1].mac.decode(UTF8_DECODE)

            if not ack_response:
                do_callback = True
            elif ack_response == ACK_SUCCESS:
                if ack_small:
                    _LOGGER.debug(
                        "Process small ACK_SUCCESS acknowledge for %s with seq_id %s",
                        str(self.expected_responses[seq_id][1].__class__.__name__),
                        str(seq_id),
                    )
                else:
                    _LOGGER.debug(
                        "Process large ACK_SUCCESS acknowledge for %s from %s with seq_id %s",
                        str(self.expected_responses[seq_id][1].__class__.__name__),
                        mac,
                        str(seq_id),
                    )
                    do_callback = True
            elif ack_response == ACK_TIMEOUT:
                _LOGGER.debug(
                    "Process ACK_TIMEOUT for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            elif ack_response == ACK_ERROR:
                _LOGGER.debug(
                    "Process ACK_ERROR for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            elif ack_response == ACK_ON:
                _LOGGER.debug(
                    "Process ACK_ON response for %s from %s with seq_id %s",
                    self.expected_responses[seq_id][0].__class__.__name__,
                    mac,
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == ACK_OFF:
                _LOGGER.debug(
                    "Process ACK_OFF response for %s from %s with seq_id %s",
                    self.expected_responses[seq_id][0].__class__.__name__,
                    mac,
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == ACK_ACCEPT_JOINING_REQUEST:
                _LOGGER.debug(
                    "Process ACK_ACCEPT_JOINING_REQUEST for %s from %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    mac,
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == ACK_SLEEP_SET:
                _LOGGER.debug(
                    "Process ACK_SLEEP_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == ACK_CLOCK_SET:
                _LOGGER.debug(
                    "Process ACK_CLOCK_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == NACK_SLEEP_SET:
                _LOGGER.debug(
                    "Process NACK_SLEEP_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            elif ack_response == ACK_SCAN_PARAMETERS_SET:
                _LOGGER.debug(
                    "Process ACK_SCAN_PARAMETERS_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_callback = True
            elif ack_response == NACK_SCAN_PARAMETERS_SET:
                _LOGGER.debug(
                    "Process NACK_SCAN_PARAMETERS_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            elif ack_response == NACK_ON_OFF:
                _LOGGER.debug(
                    "Process NACK_ON_OFF for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            elif ack_response == NACK_REAL_TIME_CLOCK_SET:
                _LOGGER.debug(
                    "Process NACK_REAL_TIME_CLOCK_SET for %s with seq_id %s",
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )
                do_resend = True
            else:
                _LOGGER.warning(
                    "Unknown ack_response %s for %s with seq_id %s",
                    str(ack_response),
                    str(self.expected_responses[seq_id][1].__class__.__name__),
                    str(seq_id),
                )

            if do_resend:
                if self.expected_responses[seq_id][3] <= MESSAGE_RETRY:
                    if (
                        isinstance(self.expected_responses[seq_id][1], NodeInfoRequest)
                        and not self._discovery_finished
                        and mac in self._nodes_not_discovered
                        and self.expected_responses[seq_id][2].__name__
                        == "node_discovered"
                    ):
                        # Time out for node which is not discovered yet
                        # to speedup the initial discover phase skip retries and mark node as not discovered.
                        _LOGGER.debug(
                            "Skip retries for %s to speedup discover process",
                            mac,
                        )
                        self.expected_responses[seq_id][2](True)
                    elif isinstance(
                        self.expected_responses[seq_id][1], NodeInfoRequest
                    ) or isinstance(
                        self.expected_responses[seq_id][1], NodePingRequest
                    ):
                        _LOGGER.info(
                            "Resend request %s for %s, retry %s of %s",
                            str(self.expected_responses[seq_id][1].__class__.__name__),
                            mac,
                            str(self.expected_responses[seq_id][3] + 1),
                            str(MESSAGE_RETRY + 1),
                        )
                        self.send(
                            self.expected_responses[seq_id][1],
                            self.expected_responses[seq_id][2],
                            self.expected_responses[seq_id][3] + 1,
                        )
                    else:
                        if (
                            self._plugwise_nodes.get(mac)
                            and self._plugwise_nodes[mac].get_available()
                        ):
                            _LOGGER.info(
                                "Resend request %s for %s, retry %s of %s",
                                str(
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__
                                ),
                                mac,
                                str(self.expected_responses[seq_id][3] + 1),
                                str(MESSAGE_RETRY + 1),
                            )
                            self.send(
                                self.expected_responses[seq_id][1],
                                self.expected_responses[seq_id][2],
                                self.expected_responses[seq_id][3] + 1,
                            )
                        else:
                            _LOGGER.debug(
                                "Do not resend request %s for %s, node is off-line",
                                str(
                                    self.expected_responses[seq_id][
                                        1
                                    ].__class__.__name__
                                ),
                                mac,
                            )
                else:
                    _LOGGER.info(
                        "Drop request for %s for %s because max retries %s reached",
                        str(self.expected_responses[seq_id][1].__class__.__name__),
                        mac,
                        str(MESSAGE_RETRY + 1),
                    )
                    if isinstance(
                        self.expected_responses[seq_id][1], NodeInfoRequest
                    ) or isinstance(
                        self.expected_responses[seq_id][1], NodePingRequest
                    ):
                        # Mark node as unavailable
                        if self._plugwise_nodes.get(mac):
                            if (
                                self._plugwise_nodes[mac].get_available()
                                and not self._plugwise_nodes[mac].is_sed()
                            ):
                                _LOGGER.info(
                                    "Mark %s as unavailabe because no response after %s retries",
                                    mac,
                                    str(MESSAGE_RETRY + 1),
                                )
                                self._plugwise_nodes[mac].set_available(False)
                    else:
                        # Failed request, do a ping to validate if node is available
                        if self._plugwise_nodes.get(mac):
                            if not self._plugwise_nodes[mac].is_sed():
                                self._plugwise_nodes[mac].ping()
                del self.expected_responses[seq_id]

            if do_callback:
                if self.expected_responses[seq_id][2]:
                    try:
                        self.expected_responses[seq_id][2]()
                    except Exception as e:
                        _LOGGER.error(
                            "Error while executing callback after processing message : %s",
                            e,
                        )
                del self.expected_responses[seq_id]

        else:
            if not self.last_ack_seq_id:
                if b"0000" in self.expected_responses:
                    self.expected_responses[seq_id] = self.expected_responses[b"0000"]
                    del self.expected_responses[b"0000"]
                self.last_ack_seq_id = seq_id
            else:
                _LOGGER.info(
                    "Response %s for unknown seq_id %s",
                    str(ack_response),
                    str(seq_id),
                )

    def _watchdog_loop(self):
        """
        Main worker loop to watch all other worker threads
        """
        time.sleep(5)
        circle_plus_retry_counter = 0
        while self._run_watchdog:
            # Connection
            if self.connection.is_connected():
                # Connection reader daemon
                if not self.connection.read_thread_alive():
                    _LOGGER.warning("Unexpected halt of connection reader thread")
                # Connection writer daemon
                if not self.connection.write_thread_alive():
                    _LOGGER.warning("Unexpected halt of connection writer thread")
            # receive timeout daemon
            if self._run_receive_timeout_thread:
                if not self._receive_timeout_thread.isAlive():
                    _LOGGER.warning(
                        "Unexpected halt of receive thread, restart thread",
                    )
                    self._receive_timeout_thread = threading.Thread(
                        None,
                        self._receive_timeout_loop,
                        "receive_timeout_thread",
                        (),
                        {},
                    )
                    self._receive_timeout_thread.daemon = True
                    self._receive_timeout_thread.start()
            # send message daemon
            if self._run_send_message_thread:
                if not self._send_message_thread.isAlive():
                    _LOGGER.warning(
                        "Unexpected halt of send thread, restart thread",
                    )
                    self._send_message_thread = threading.Thread(
                        None, self._send_message_loop, "send_messages_thread", (), {}
                    )
                    self._send_message_thread.daemon = True
                    self._send_message_thread.start()
            # Update daemon
            if self._run_update_thread:
                if not self._update_thread.isAlive():
                    _LOGGER.warning(
                        "Unexpected halt of update thread, restart thread",
                    )
                    self._run_update_thread = True
                    self._update_thread = threading.Thread(
                        None, self._update_loop, "update_thread", (), {}
                    )
                    self._update_thread.daemon = True
                    self._update_thread.start()
            # Circle+ discovery
            if not self._circle_plus_discovered:
                # First hour every once an hour
                if self._circle_plus_retries < 60 or circle_plus_retry_counter > 60:
                    _LOGGER.info(
                        "Circle+ not yet discovered, resubmit discovery request",
                    )
                    self.discover_node(self.circle_plus_mac, self.scan)
                    self._circle_plus_retries += 1
                    circle_plus_retry_counter = 0
                circle_plus_retry_counter += 1
            watchdog_loop_checker = 0
            while watchdog_loop_checker < WATCHDOG_DEAMON and self._run_watchdog:
                time.sleep(1)
                watchdog_loop_checker += 1
        _LOGGER.debug("watchdog loop stopped")

    def _update_loop(self):  # noqa: C901
        """
        When node has not received any message during
        last 2 update polls, reset availability
        """
        # TODO: flake8 indicates scan is too complex, level 28 indenting is indeed complex
        self._run_update_thread = True
        _auto_update_first_run = True
        day_of_month = datetime.now().day
        try:
            while self._run_update_thread:
                for mac in self._plugwise_nodes:
                    if self._plugwise_nodes[mac]:
                        # Check availability state of SED's
                        if self._plugwise_nodes[mac].is_sed():
                            if self._plugwise_nodes[mac].get_available():
                                if self._plugwise_nodes[mac].last_update < (
                                    datetime.now()
                                    - timedelta(
                                        minutes=(
                                            self._plugwise_nodes[
                                                mac
                                            ].maintenance_interval
                                            + 1
                                        )
                                    )
                                ):
                                    _LOGGER.info(
                                        "No messages received within (%s minutes) of expected maintenance interval from node %s, mark as unavailable [%s > %s]",
                                        str(
                                            self._plugwise_nodes[
                                                mac
                                            ].maintenance_interval
                                        ),
                                        mac,
                                        str(self._plugwise_nodes[mac].last_update),
                                        str(
                                            datetime.now()
                                            - timedelta(
                                                minutes=(
                                                    self._plugwise_nodes[
                                                        mac
                                                    ].maintenance_interval
                                                    + 1
                                                )
                                            )
                                        ),
                                    )
                                    self._plugwise_nodes[mac].set_available(False)
                        else:
                            # Do ping request
                            _LOGGER.debug(
                                "Send ping to node %s",
                                mac,
                            )
                            self._plugwise_nodes[mac].ping()

                    # Only power use updates for supported nodes
                    if (
                        isinstance(self._plugwise_nodes[mac], PlugwiseCircle)
                        or isinstance(self._plugwise_nodes[mac], PlugwiseCirclePlus)
                        or isinstance(self._plugwise_nodes[mac], PlugwiseStealth)
                    ):
                        # Don't check at first time
                        _LOGGER.debug("Request current power usage for node %s", mac)
                        if not _auto_update_first_run and self._run_update_thread:
                            # Only request update if node is available
                            if self._plugwise_nodes[mac].get_available():
                                _LOGGER.debug(
                                    "Node '%s' is available for update request, last update (%s)",
                                    mac,
                                    str(self._plugwise_nodes[mac].get_last_update()),
                                )
                                # Skip update request if there is still an request expected to be received
                                open_requests_found = False
                                for seq_id in list(self.expected_responses.keys()):
                                    if isinstance(
                                        self.expected_responses[seq_id][1],
                                        CirclePowerUsageRequest,
                                    ):
                                        if mac == self.expected_responses[seq_id][
                                            1
                                        ].mac.decode(UTF8_DECODE):
                                            open_requests_found = True
                                            break
                                if not open_requests_found:
                                    self._plugwise_nodes[mac].update_power_usage()
                                # Refresh node info once per hour and request power use afterwards
                                if (
                                    self._plugwise_nodes[mac].last_info_message
                                    is not None
                                ):
                                    if self._plugwise_nodes[mac].last_info_message < (
                                        datetime.now().replace(
                                            minute=0,
                                            second=0,
                                            microsecond=0,
                                        )
                                    ):
                                        self._plugwise_nodes[mac].request_info(
                                            self._plugwise_nodes[
                                                mac
                                            ].request_power_buffer
                                        )
                                if not self._plugwise_nodes[mac].last_log_collected:
                                    self._plugwise_nodes[mac].request_power_buffer()
                        else:
                            if self._run_update_thread:
                                _LOGGER.debug(
                                    "First request for current power usage for node %s",
                                    mac,
                                )
                                self._plugwise_nodes[mac].update_power_usage()
                        _auto_update_first_run = False

                        # Sync internal clock of all available Circle and Circle+ nodes once a day
                        if datetime.now().day != day_of_month:
                            day_of_month = datetime.now().day
                            if self._plugwise_nodes[mac].get_available():
                                self._plugwise_nodes[mac].sync_clock()

                # Try to rediscover node(s) which where not available at initial scan
                # Do this the first hour at every update, there after only once an hour
                for mac in self._nodes_not_discovered:
                    (firstrequest, lastrequest) = self._nodes_not_discovered[mac]
                    if firstrequest and lastrequest:
                        if (firstrequest + timedelta(hours=1)) > datetime.now():
                            # first hour, so do every update a request
                            _LOGGER.debug(
                                "Try rediscovery of node %s",
                                mac,
                            )
                            self.discover_node(mac, self._discover_after_scan, True)
                            self._nodes_not_discovered[mac] = (
                                firstrequest,
                                datetime.now(),
                            )
                        else:
                            if (lastrequest + timedelta(hours=1)) < datetime.now():
                                _LOGGER.debug(
                                    "Try rediscovery of node %s",
                                    mac,
                                )
                                self.discover_node(mac, self._discover_after_scan, True)
                                self._nodes_not_discovered[mac] = (
                                    firstrequest,
                                    datetime.now(),
                                )
                    else:
                        _LOGGER.debug(
                            "Try rediscovery of node %s",
                            mac,
                        )
                        self.discover_node(mac, self._discover_after_scan, True)
                        self._nodes_not_discovered[mac] = (
                            datetime.now(),
                            datetime.now(),
                        )
                if self._auto_update_timer and self._run_update_thread:
                    update_loop_checker = 0
                    while (
                        update_loop_checker < self._auto_update_timer
                        and self._run_update_thread
                    ):
                        time.sleep(1)
                        update_loop_checker += 1

        except Exception as e:
            _exc_type, _exc_obj, exc_tb = sys.exc_info()
            _LOGGER.error("Error at line %s of _update_loop : %s", exc_tb.tb_lineno, e)
        _LOGGER.debug("Update loop stopped")

    def auto_update(self, timer=None):
        """ Configure auto update polling daemon for power usage and availability state. """
        if timer:
            self._auto_update_timer = timer
        elif timer == 0:
            self._auto_update_timer = 0
            self._run_update_thread = False
        else:
            # Timer based on number of nodes and 3 seconds per node
            self._auto_update_timer = len(self._plugwise_nodes) * 3
        if not self._run_update_thread:
            self._update_thread.start()
