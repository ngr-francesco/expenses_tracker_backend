"""
This serves as a simulation to test the backend components
"""
from expenses_tracker_backend.utils.logging import Logger, LogLevel
from expenses_tracker_backend.sim.application import application
from expenses_tracker_backend.cls.manager import ProfileManager

if __name__ == '__main__':
    Logger.set_log_level(LogLevel.DEBUG)
    ProfileManager()
    app = application()
    app.run()