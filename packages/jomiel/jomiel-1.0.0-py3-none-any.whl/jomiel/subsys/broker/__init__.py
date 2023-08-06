#
# jomiel
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from jomiel.log import lg
from jomiel_kore.app import exit_error
from jomiel_kore.sig import GracefulExit
from zmq import Context
from zmq import DEALER
from zmq import proxy
from zmq import ROUTER
from zmq import ZMQError


def log(text, msgtype="debug"):
    """Write a new (debug) entry to the logger."""
    logger = getattr(lg(), msgtype)
    logger("subsystem/broker: %s", text)


def init():
    """Initiates the broker."""

    ctx = Context.instance()

    def bind_endpoint(device, endpoint, setup_curve=False):
        """Bind the device to the endpoint."""
        sck = ctx.socket(device)
        auth = None
        if opts.curve_enable and setup_curve:
            log("setup curve support")
            from jomiel.curve import setup

            auth = setup(sck)  # Must come before bind.
        try:
            sck.bind(endpoint)
        except ZMQError as error:
            log(f"{error}: {endpoint}", "error")
            exit_error()
        return (sck, auth)

    from jomiel.cache import opts

    def bind_router():
        """Bind the router device for talking to the clients."""
        router_endpoint = opts.broker_router_endpoint
        (router, auth) = bind_endpoint(
            ROUTER,
            router_endpoint,
            setup_curve=True,
        )
        log("bind router at <%s>" % router_endpoint)
        return (router, auth)

    (router, auth) = bind_router()

    def bind_dealer():
        """Bind the dealer device for talking to the workers."""
        dealer_endpoint = opts.broker_dealer_endpoint
        (dealer, _) = bind_endpoint(DEALER, dealer_endpoint)
        log("bind dealer at <%s>" % dealer_endpoint)
        return dealer

    dealer = bind_dealer()

    def main_loop():
        """The main loop; sits and awaits for new connections."""

        def start_workers():
            """Creates the worker threads and initiates them."""

            from jomiel.subsys.broker.worker import worker_new
            from threading import Thread

            for worker_id in range(opts.broker_worker_threads):
                worker_thread = Thread(
                    target=worker_new,
                    args=(worker_id + 1,),
                )
                worker_thread.start()

            log("%d thread(s) active" % opts.broker_worker_threads)

        start_workers()

        try:
            proxy(router, dealer)
        except KeyboardInterrupt:
            log("<sigint> signal interrupt")
        except ZMQError as error:
            log(error)
        finally:
            dealer.close()
            router.close()
            if auth:
                auth.stop()
            ctx.term()

        log("shutdown")

    with GracefulExit(log):
        main_loop()


# vim: set ts=4 sw=4 tw=72 expandtab:
