import asyncio
import time
import psutil
import logging
from typing import Dict, Any

class PerformanceOptimizer:
    """Real-time performance monitoring and optimization"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("butler.performance")
        self.metrics = {
            'response_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'conversation_lengths': []
        }
        self.optimization_thresholds = {
            'max_response_time': 3.0,  # seconds
            'max_memory_mb': 500,
            'max_conversation_length': 20
        }
        
    async def initialize(self):
        self.logger.info("⚡ Performance optimizer initialized")
        return True
    
    async def monitor_conversation_start(self, session_id: str):
        """Monitor conversation start"""
        self.current_session = {
            'session_id': session_id,
            'start_time': time.time(),
            'interaction_count': 0,
            'total_response_time': 0
        }
    
    async def record_interaction(self, response_time: float, user_input: str, system_response: str):
        """Record interaction metrics"""
        self.current_session['interaction_count'] += 1
        self.current_session['total_response_time'] += response_time
        
        # Store metrics
        self.metrics['response_times'].append(response_time)
        self.metrics['conversation_lengths'].append(len(system_response))
        
        # Monitor system resources
        await self._record_system_metrics()
        
        # Check for optimization needs
        await self._check_optimization_needs()
    
    async def _record_system_metrics(self):
        """Record system performance metrics"""
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        self.metrics['memory_usage'].append(memory_usage)
        self.metrics['cpu_usage'].append(cpu_usage)
    
    async def _check_optimization_needs(self):
        """Check if optimization is needed based on metrics"""
        avg_response_time = sum(self.metrics['response_times'][-10:]) / min(10, len(self.metrics['response_times']))
        avg_memory = sum(self.metrics['memory_usage'][-5:]) / min(5, len(self.metrics['memory_usage']))
        
        optimizations = []
        
        if avg_response_time > self.optimization_thresholds['max_response_time']:
            optimizations.append("response_time")
            self.logger.warning(f"⚠️ High response time: {avg_response_time:.2f}s")
        
        if avg_memory > self.optimization_thresholds['max_memory_mb']:
            optimizations.append("memory_usage")
            self.logger.warning(f"⚠️ High memory usage: {avg_memory:.2f}MB")
        
        if optimizations:
            await self._apply_optimizations(optimizations)
    
    async def _apply_optimizations(self, optimizations: List[str]):
        """Apply real-time optimizations"""
        for optimization in optimizations:
            if optimization == "response_time":
                await self._optimize_response_time()
            elif optimization == "memory_usage":
                await self._optimize_memory_usage()
    
    async def _optimize_response_time(self):
        """Optimize for faster responses"""
        self.logger.info("⚡ Applying response time optimizations")
        # Could include: caching, precomputation, simplified responses
    
    async def _optimize_memory_usage(self):
        """Optimize memory usage"""
        self.logger.info("🧹 Applying memory optimizations")
        # Clear old metrics if too many
        if len(self.metrics['response_times']) > 100:
            for key in self.metrics:
                self.metrics[key] = self.metrics[key][-50:]
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Get current performance report"""
        if not self.metrics['response_times']:
            return {'status': 'no_data'}
        
        return {
            'avg_response_time': sum(self.metrics['response_times'][-10:]) / min(10, len(self.metrics['response_times'])),
            'avg_memory_usage': sum(self.metrics['memory_usage'][-5:]) / min(5, len(self.metrics['memory_usage'])),
            'avg_cpu_usage': sum(self.metrics['cpu_usage'][-5:]) / min(5, len(self.metrics['cpu_usage'])),
            'total_interactions': len(self.metrics['response_times']),
            'status': 'healthy'
        }
    
    async def should_simplify_responses(self) -> bool:
        """Determine if responses should be simplified for performance"""
        report = await self.get_performance_report()
        return (report['avg_response_time'] > 2.0 or 
                report['avg_memory_usage'] > 400)

print("⚡ PerformanceOptimizer class defined")
