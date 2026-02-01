"""
Performance monitoring utilities
"""

import time
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


class FPSCounter:
    """FPS counter with moving average"""
    
    def __init__(self, window_size=30):
        """
        Initialize FPS counter
        
        Args:
            window_size: Number of frames to average over
        """
        self.window_size = window_size
        self.frame_times = []
        self.last_time = time.time()
    
    def update(self):
        """Update FPS counter with new frame"""
        current_time = time.time()
        delta = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(delta)
        
        # Keep only recent frames
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
    
    def get_fps(self):
        """Get current FPS"""
        if not self.frame_times:
            return 0.0
        
        avg_time = np.mean(self.frame_times)
        if avg_time == 0:
            return 0.0
        
        return 1.0 / avg_time
    
    def reset(self):
        """Reset FPS counter"""
        self.frame_times = []
        self.last_time = time.time()


class PerformanceProfiler:
    """Profile performance of different components"""
    
    def __init__(self):
        """Initialize profiler"""
        self.timings = {}
        self.start_times = {}
    
    def start(self, component):
        """Start timing a component"""
        self.start_times[component] = time.time()
    
    def end(self, component):
        """End timing a component"""
        if component not in self.start_times:
            return
        
        elapsed = time.time() - self.start_times[component]
        
        if component not in self.timings:
            self.timings[component] = []
        
        self.timings[component].append(elapsed)
        
        # Keep only recent timings
        if len(self.timings[component]) > 100:
            self.timings[component].pop(0)
    
    def get_stats(self, component):
        """Get statistics for a component"""
        if component not in self.timings or not self.timings[component]:
            return None
        
        timings = self.timings[component]
        
        return {
            'mean': np.mean(timings) * 1000,  # ms
            'std': np.std(timings) * 1000,    # ms
            'min': np.min(timings) * 1000,    # ms
            'max': np.max(timings) * 1000,    # ms
            'count': len(timings)
        }
    
    def print_report(self):
        """Print performance report"""
        print("\n" + "=" * 70)
        print("PERFORMANCE REPORT")
        print("=" * 70)
        
        for component in sorted(self.timings.keys()):
            stats = self.get_stats(component)
            if stats:
                print(f"\n{component}:")
                print(f"  Mean:  {stats['mean']:6.2f} ms")
                print(f"  Std:   {stats['std']:6.2f} ms")
                print(f"  Min:   {stats['min']:6.2f} ms")
                print(f"  Max:   {stats['max']:6.2f} ms")
                print(f"  Count: {stats['count']:6d}")
        
        print("\n" + "=" * 70)
    
    def reset(self):
        """Reset profiler"""
        self.timings = {}
        self.start_times = {}


def draw_fps(frame, fps, position=None, color=None, font_scale=None):
    """
    Draw FPS counter on frame
    
    Args:
        frame: Input frame
        fps: FPS value
        position: Text position (x, y)
        color: Text color (B, G, R)
        font_scale: Font scale
    
    Returns:
        Frame with FPS overlay
    """
    
    if position is None:
        position = config.FPS_POSITION
    if color is None:
        color = config.FPS_COLOR
    if font_scale is None:
        font_scale = config.TEXT_SCALE
    
    text = f"FPS: {fps:.1f}"
    
    cv2.putText(
        frame,
        text,
        position,
        config.TEXT_FONT,
        font_scale,
        color,
        config.TEXT_THICKNESS,
        cv2.LINE_AA
    )
    
    return frame


def draw_performance_overlay(frame, profiler, position=(10, 60)):
    """
    Draw performance overlay on frame
    
    Args:
        frame: Input frame
        profiler: PerformanceProfiler instance
        position: Starting position (x, y)
    
    Returns:
        Frame with performance overlay
    """
    
    x, y = position
    line_height = 25
    
    components = ['face_detection', 'preprocessing', 'inference', 'total']
    
    for i, component in enumerate(components):
        stats = profiler.get_stats(component)
        if stats:
            text = f"{component}: {stats['mean']:.1f}ms"
            cv2.putText(
                frame,
                text,
                (x, y + i * line_height),
                config.TEXT_FONT,
                0.5,
                config.FPS_COLOR,
                1,
                cv2.LINE_AA
            )
    
    return frame


if __name__ == '__main__':
    """Test performance utilities"""
    
    print("Testing FPS counter...")
    
    fps_counter = FPSCounter()
    
    # Simulate frames
    for i in range(60):
        time.sleep(1/30)  # Simulate 30 FPS
        fps_counter.update()
        
        if i % 10 == 0:
            print(f"Frame {i}: {fps_counter.get_fps():.2f} FPS")
    
    print("\nTesting performance profiler...")
    
    profiler = PerformanceProfiler()
    
    # Simulate component timings
    for i in range(50):
        profiler.start('component_a')
        time.sleep(0.01)
        profiler.end('component_a')
        
        profiler.start('component_b')
        time.sleep(0.02)
        profiler.end('component_b')
    
    profiler.print_report()
    
    print("\n✓ Performance utilities test completed!")
