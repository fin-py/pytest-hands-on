import subprocess
import connpass_client
from typer.testing import CliRunner


def test_version_v1():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--version"], capture_output=True, text=True
    )

    output = output.stdout.rstrip()
    assert output == connpass_client.__version__


def test_version_v2():
    runner = CliRunner()
    result = runner.invoke(connpass_client.app, ["--version"])
    output = result.stdout.rstrip()
    assert output == connpass_client.__version__


def test_1(capsys):
    # 標準出力
    print(connpass_client.__version__)

    # with capsys.disabled():
    #     print(capsys.readouterr())

    assert capsys.readouterr().out.strip() == "0.3.0"

