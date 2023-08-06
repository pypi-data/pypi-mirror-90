# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bugyocloudclient',
 'bugyocloudclient.endpoints',
 'bugyocloudclient.endpoints.base',
 'bugyocloudclient.models',
 'bugyocloudclient.tasks',
 'bugyocloudclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'bugyocloudclient',
    'version': '0.2.2',
    'description': 'Bugyo Cloud Client',
    'long_description': '# OBC Bugyo Cloud client\n\nOBC 奉行クラウド Pythonクライアント\n\n# Usage\n\nBugyoCloudClientのインスタンスを作成します。\n\n```python\nimport bugyocloudclient as bcc\n\n\ntenant_code = \'The first part of URL path.\'\nclient = bcc.BugyoCloudClient(tenant_code)\n```\n\n最初にLoginTaskを実行して、ログイン状態にします。\n\n```python\nauth_info = bcc.AuthInfo(\'login id\', \'password\')\nlogin_task = bcc.LoginTask(auth_info)\nclient.exec(login_task)\n```\n\nログインしてから、別のタスクを実行します。\n（今は打刻タスクしかありません）。\n\n```python\npunch_info = bcc.PunchInfo()\npunch_info.clock_type = clock_type\npunch_task = bcc.PunchTask(punch_info)\nclient.exec(punch_task)\n```\n\n\n# Installing poetry\n\n```console\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3\n```\n\nChanging python command name from \'python\' to \'python3\'.\n\n```console\nvi ~/.poetry/bin/poetry\n```\n\n\n# Creating environment\n\n```console\npoetry install\n```\n\n\n# Testing\n\n```console\npoetry run pytest\n```\n\n# Build & Publish\n\n```console\npoetry buid\npoetry publish -r testpypi\npoetry publish\n```\n\n\n# 画面あるいはAPI\n\n## 認証画面\n\n* URL: https://id.obc.jp/{{テナント?}}/\n* METHOD: GET\n* Response:\n  * Headers:\n    * Content-Type: text/html; charset=utf-8\n\n\n## 認証方法チェック\n\n* URL: https://id.obc.jp/{{テナント?}}/login/CheckAuthenticationMethod\n* METHOD: POST\n* Headers:\n  * __RequestVerificationToken: 認証画面のフォームにあるhidden value\n  * Content-Type: application/x-www-form-urlencoded; charset=UTF-8\n  * X-Requested-With: XMLHttpRequest\n* Content:\n  * "OBCiD" : ログインID\n  * "isBugyoCloud" : "false"\n* Response:\n  * Headers:\n    * Content-Type: application/json; charset=utf-8\n  * Content:\n    * AuthenticationMethod\n    * SAMLButtonText\n    * PasswordButtonText\n\n\n## 認証\n\n* URL: https://id.obc.jp/{{テナント?}}/login/login/?Length=5\n* METHOD: POST\n* Headers:\n  * Content-Type: application/x-www-form-urlencoded; charset=UTF-8\n* Content:\n  * "btnLogin" : ""\n  * "OBCID" : ログインID\n  * "Password_d1" : ""\n  * "Password_d2" : ""\n  * "Password_d3" : ""\n  * "Password" : パスワード\n  * "__RequestVerificationToken" : 認証画面のフォームにあるinput hidden value\n  * "X-Requested-With" : "XMLHttpRequest"\n* Response:\n  * Headers:\n    * Content-Type: application/json; charset=utf-8\n  * Content:\n    * RedirectURL\n    * LoginOBCiD\n\n\nレスポンスにあるRedirectURLをGETすると302が返ります。\n302に従うと、ユーザ初期画面へ遷移します。URLは、https://hromssp.obc.jp/{{テナント？}}/{{ユニーク文字列？}}/ のようになります。\n\n## ユーザ初期画面\n\n* URL: https://hromssp.obc.jp/{{テナント？}}/{{ユニーク文字列？}}/\n* METHOD: GET\n\n認証後の302応答に従うとたどり着きます。\n\nユニーク文字列の部分を、このあとの処理で使います。\n\n\n## 打刻画面\n\n* URL: https://hromssp.obc.jp/{{テナント？}}/{{ユーザ初期画面URLより}}/timeclock/punchmark/\n* METHOD: GET\n* Response:\n  * Headers:\n    * Content-Type: text/html; charset=utf-8\n\n\n\n## 打刻\n\n* URL: https://hromssp.obc.jp/{{テナント？}}/{{ユーザ初期画面URLより}}/TimeClock/InsertReadDateTime/\n* METHOD: POST\n* Headers:\n  * __RequestVerificationToken: 打刻画面にあるinput hidden value\n  * Content-Type: application/x-www-form-urlencoded; charset=UTF-8\n* Content:\n  * "ClockType" : 打刻種類\n  * "LaborSystemID" : "0"\n  * "LaborSystemCode" : ""\n  * "LaborSystemName" : ""\n  * "PositionLatitude" : 緯度\n  * "PositionLongitude" : 経度\n  * "PositionAccuracy" : "0"\n\n### 打刻種類\n\n* "ClockIn" : 出勤\n* "ClockOut" : 退出\n\n',
    'author': 'sengokyu',
    'author_email': 'sengokyu+gh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sengokyu/bugyo-cloud-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
