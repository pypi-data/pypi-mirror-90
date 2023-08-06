import time
import argparse

from selenium import webdriver
from watchdog.observers import Observer
from watchdog.tricks import ShellCommandTrick
from watchdog.utils import WatchdogShutdown


class Handler(ShellCommandTrick):
    def __init__(
        self,
        driver,
        shell_command=None,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        wait_for_process=False,
        drop_during_process=False,
    ):
        super().__init__(
            shell_command=shell_command,
            patterns=["*.rst"],
            ignore_patterns=ignore_patterns,
            ignore_directories=ignore_directories,
            wait_for_process=wait_for_process,
            drop_during_process=drop_during_process,
        )
        self.driver = driver

    def on_any_event(self, event):
        result = super().on_any_event(event)
        self.driver.refresh()
        print("We are doing it!")
        return result


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("watch")
    parser.add_argument("command")
    parser.add_argument("url")
    args = parser.parse_args()

    driver = webdriver.Firefox()
    driver.get(args.url)

    time.sleep(3)

    handler = Handler(
        driver=driver,
        shell_command=args.command,
    )

    observer = Observer()
    observer.schedule(handler, args.watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except WatchdogShutdown:
        observer.stop()
    observer.join()
