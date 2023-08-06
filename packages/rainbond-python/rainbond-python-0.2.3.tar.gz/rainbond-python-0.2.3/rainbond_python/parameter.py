import json
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class Parameter():
    def __init__(self, request):
        self.method = request.method  # 请求方法
        self.headers = dict(request.headers)  # 请求头
        # GET方法的取参
        self.param_url = request.args
        # 非GET方法取值
        try:
            self.param_json = json.loads(
                request.get_data(as_text=True)
            )
        except json.decoder.JSONDecodeError:
            self.param_json = {}
        # 表单提交取值
        self.param_form = request.form

    def get_content(self) -> dict:
        return {
            'method': self.method,
            'headers': self.headers,
            'param_url': self.param_url,
            'param_json': self.param_json,
            'param_form': self.param_form
        }

    def verification(self, checking: dict, verify: dict) -> bool:
        if not set(verify.keys()).issubset(set(checking.keys())):
            logging.warning('请求参数不完整: {0}'.format(json.dumps(checking)))
            return False
        for _k, _v in checking.items():
            if type(_v) != verify[_k]:
                logging.warning('请求参数类型校验失败: {0}'.format(json.dumps(checking)))
                return False
        return True
