import logging
import threading
import crochet
from twisted.internet import reactor, defer


class CallbackRunner(object):

    def __init__(self, callbacks, err_back, *cb_args):
        """
        Initialize the callback runner. Accepts a list of callbacks to be
        called in a chained manner through defereds.
        :param callbacks: List of methods to be added as defered callbacks.
        :param err_back: Error callback handling method.
        :param cb_args: Args to be passed to the first callback in the list.
        :return:
        """
        assert callbacks
        self.__interval = 0
        self.__callbacks = callbacks
        self.__err_back = err_back
        self.__args = cb_args

        self.__reactor = reactor
        crochet._main._reactor = self.__reactor
        self.__event = threading.Event()
        self.__start_reactor()

    def __create_daemon_thread(self, *args, **kwargs):
        """
        Create the thread in which the reactor will do its job.
        :param args:
        :param kwargs:
        :return:
        """
        t = threading.Thread(*args, **kwargs)
        t.setDaemon(True)
        return t

    def __start_reactor(self):
        """
        The reactor is thread blocking, thus we start the reactor
        in the context of another thread, rather then the main one.
        Never leave home without crochet!
        :return:
        """
        from twisted.python import threadpool
        threadpool.ThreadPool.threadFactory = self.__create_daemon_thread
        crochet.setup()
        logging.getLogger('twisted').setLevel(logging.ERROR)
        self.__reactor.callFromThread(self.__event.set)
        self.__event.wait()

    @classmethod
    def on_error(cls, error):
        """
        Default error callback, if none is provided at init time.
        :param error:
        :return:
        """
        print "Log me, error: %s" % error

    def set_interval(self, interval):
        """
        Number of seconds which the reactor will
        wait until firing the current defered.
        :param interval: Wait time (seconds)
        :return:
        """
        self.__interval = interval

    def run(self):
        d = defer.execute(self.__callbacks[0], *self.__args)
        if not self.__err_back:
            self.__err_back = self.on_error
        d.addErrback(self.__err_back)

        for cb in self.__callbacks[1:]:
            d.addCallback(cb)

        self.__reactor.callLater(self.__interval, self.run)

    def stop(self):
        if self.__reactor.running:
            self.__reactor.stop()
