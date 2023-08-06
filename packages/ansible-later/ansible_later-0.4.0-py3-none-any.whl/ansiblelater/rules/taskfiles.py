"""Checks related to ansible task files."""

import re
from collections import defaultdict

from ansiblelater.command.candidates import Error
from ansiblelater.command.candidates import Result
from ansiblelater.utils.rulehelper import get_normalized_tasks
from ansiblelater.utils.rulehelper import get_normalized_yaml


def check_line_between_tasks(candidate, settings):
    options = defaultdict(dict)
    options.update(remove_empty=False)
    options.update(remove_markers=False)

    lines, line_errors = get_normalized_yaml(candidate, settings, options)
    tasks, task_errors = get_normalized_tasks(candidate, settings)
    description = "missing task separation (required: 1 empty line)"

    task_regex = re.compile(r"-\sname:(.*)")
    prevline = "#file_start_marker"

    allowed_prevline = ["---", "tasks:", "pre_tasks:", "post_tasks:", "block:"]

    errors = task_errors + line_errors
    if not errors:
        for i, line in lines:
            match = task_regex.search(line)
            if match and prevline:
                name = match.group(1).strip()

                if not any(task.get("name") == name for task in tasks):
                    continue

                if not any(item in prevline for item in allowed_prevline):
                    errors.append(Error(i, description))

            prevline = line.strip()

    return Result(candidate.path, errors)
