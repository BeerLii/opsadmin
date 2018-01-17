from ansible.plugins.callback import CallbackBase
import json

class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        self.data = json.dumps({host.name: result._result}, indent=4)

class AdHocResultCallBack(CallbackBase):
    def __init__(self, display=None):
        self.result_q = dict(contacted={}, dark={})

        super(AdHocResultCallBack, self).__init__(display)

    def gather_result(self, n, res):
        if res._host.name in self.result_q[n]:
            self.result_q[n][res._host.name].append(res._result)

        else:
            self.result_q[n][res._host.name] = [res._result]
        for host in self.result_q['contacted']:
            print(host)

    def v2_runner_on_ok(self, result):

        self.gather_result("contacted", result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.gather_result("dark", result)

    def v2_runner_on_unreachable(self, result):
        self.gather_result("dark", result)

    def v2_runner_on_skipped(self, result):
        self.gather_result("dark", result)