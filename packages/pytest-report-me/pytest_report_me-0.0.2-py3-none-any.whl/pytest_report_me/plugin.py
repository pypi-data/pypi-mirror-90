from datetime import datetime
from pathlib import Path
import pytest
import jinja2

reports = {"cases":{},
           "summary":
               {"failed":0,
                "passed":0,
                "skip":0,
                "start_ts": 0,
                "end_ts": 0,
                "start_date_time": ""
                }
           }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        fixture_extras = getattr(item.config, "extras", [])
        plugin_extras = getattr(report, "extra", [])
        report.extra = fixture_extras + plugin_extras

def pytest_sessionstart(session):
        start_ts = datetime.now()
        reports['summary']["start_ts"] = start_ts.timestamp()
        reports['summary']["start_date_time"] = start_ts.strftime("%Y-%m-%d %H:%M:%S")


def pytest_sessionfinish(session):
    ts = datetime.now()
    reports["summary"]["end_ts"] = ts.timestamp()

    template_dir = Path(__file__).resolve().parent / 'templates'
    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.Environment(loader=loader)
    template = env.get_template('templates.html')
    report = template.render(result=reports)


    # time_str = ts.strftime("%Y-%m-%d-%H-%M-%S")
    # report_name = "测试报告-" + time_str + ".html"
    report_name = session.config.getoption('--report')
    with open(report_name, mode="w", encoding="utf-8") as f:
        f.write(report)


def pytest_runtest_logreport(report):
    if report.when == "call":
        reports["cases"][report.nodeid] = report
        reports["summary"][report.outcome] += 1


# def pytest_terminal_summary(terminalreporter):
#     reports['summary'] = terminalreporter.stats

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--report",
        action="store",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )

# def pytest_configure(config):
#     htmlpath = config.getoption("htmlpath")


