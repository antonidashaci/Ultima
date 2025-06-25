# ULTIMA Cursor Bridge
# Connects Cursor AI with NeoAI Orchestrator for seamless task flow

from .task_detector import CursorTaskDetector
from .result_writer import CursorResultWriter
 
__version__ = "0.1.0"
__all__ = ["CursorTaskDetector", "CursorResultWriter"] 