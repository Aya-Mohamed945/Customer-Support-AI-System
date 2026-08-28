# app/monitoring/metrics.py
"""
Monitoring and Metrics Collection with JSON persistence
"""

import time
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collect and store metrics for monitoring with JSON persistence"""
    
    def __init__(self, storage_file: str = "metrics_data.json"):
        self.storage_file = storage_file
        self.predictions = []
        self.errors = []
        self.start_time = datetime.now()
        self._load_from_file()
    
    def _load_from_file(self):
        """Load metrics from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.predictions = data.get('predictions', [])
                    self.errors = data.get('errors', [])
                    self.start_time = datetime.fromisoformat(data.get('start_time', datetime.now().isoformat()))
                    logger.info(f"✅ Loaded {len(self.predictions)} predictions from {self.storage_file}")
            except Exception as e:
                logger.warning(f"Could not load metrics file: {e}")
                self.predictions = []
                self.errors = []
                self.start_time = datetime.now()
        else:
            logger.info(f"📁 No existing metrics file found. Starting fresh.")
            self.predictions = []
            self.errors = []
            self.start_time = datetime.now()
    
    def _save_to_file(self):
        """Save metrics to JSON file"""
        try:
            data = {
                'predictions': self.predictions,
                'errors': self.errors,
                'start_time': self.start_time.isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_predictions': len(self.predictions),
                'total_errors': len(self.errors),
                'version': '2.0'
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Could not save metrics file: {e}")
    
    def log_prediction(self, 
                       user_id: str,  # ✅ جديد
                       title: str,
                       description: str,
                       category: str,
                       priority: str,
                       sentiment: str,
                       suggested_solution: str,
                       source: str,
                       priority_confidence: float,
                       rag_confidence: float = 0.0,
                       rag_results: List = None,
                       response_time_ms: float = 0) -> str:
        """
        Log a complete prediction with all details
        Returns ticket_id
        """
        ticket_id = str(uuid.uuid4())[:8]
        
        entry = {
            'ticket_id': ticket_id,
            'user_id': user_id,  # ✅ جديد
            'timestamp': datetime.now().isoformat(),
            'title': title[:200],
            'description': description[:1000],
            'category': category,
            'priority': priority,
            'sentiment': sentiment,
            'suggested_solution': suggested_solution[:500],
            'source': source,
            'priority_confidence': round(priority_confidence, 4),
            'rag_confidence': round(rag_confidence, 4),
            'rag_results': rag_results[:3] if rag_results else [],
            'response_time_ms': round(response_time_ms, 2),
            'user_feedback': None
        }
        self.predictions.append(entry)
        
        # Keep last 10000 predictions
        if len(self.predictions) > 10000:
            self.predictions = self.predictions[-10000:]
        
        # Save to file after each prediction
        self._save_to_file()
        
        return ticket_id
    
    def log_error(self, error: Dict):
        """Log an error"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'error_id': str(uuid.uuid4())[:8],
            'error_type': error.get('error_type', 'unknown'),
            'error_message': error.get('error_message', ''),
            'context': error.get('context', {})
        }
        self.errors.append(entry)
        
        # Keep last 1000 errors
        if len(self.errors) > 1000:
            self.errors = self.errors[-1000:]
        
        # Save to file
        self._save_to_file()
    
    def get_summary(self) -> Dict:
        """Get summary metrics"""
        total = len(self.predictions)
        
        if total == 0:
            return {
                'total_predictions': 0,
                'status': 'no_data',
                'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
                'priority_distribution': {},
                'sentiment_distribution': {},
                'source_distribution': {},
                'avg_priority_confidence': 0,
                'avg_rag_confidence': 0,
                'errors_count': len(self.errors),
                'last_prediction': None
            }
        
        # Priority distribution
        priority_counts = defaultdict(int)
        sentiment_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for p in self.predictions:
            priority_counts[p.get('priority', 'unknown')] += 1
            sentiment_counts[p.get('sentiment', 'unknown')] += 1
            source_counts[p.get('source', 'unknown')] += 1
        
        # Average confidence
        avg_priority_conf = sum(p.get('priority_confidence', 0) for p in self.predictions) / total
        avg_rag_conf = sum(p.get('rag_confidence', 0) for p in self.predictions) / total
        
        return {
            'total_predictions': total,
            'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'priority_distribution': dict(priority_counts),
            'sentiment_distribution': dict(sentiment_counts),
            'source_distribution': dict(source_counts),
            'avg_priority_confidence': avg_priority_conf,
            'avg_rag_confidence': avg_rag_conf,
            'errors_count': len(self.errors),
            'last_prediction': self.predictions[-1] if self.predictions else None
        }
    
    def get_all_predictions(self) -> List[Dict]:
        """Get all predictions for export"""
        return self.predictions
    
    def get_prediction_by_id(self, ticket_id: str) -> Optional[Dict]:
        """Get a specific prediction by ticket_id"""
        for p in self.predictions:
            if p.get('ticket_id') == ticket_id:
                return p
        return None
    
    # app/monitoring/metrics.py

    def get_user_tickets(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get tickets for a specific user"""
        user_tickets = [t for t in self.predictions if t.get('user_id') == user_id]
        return user_tickets[-limit:][::-1]
    
    def get_predictions_by_category(self, category: str) -> List[Dict]:
        """Get predictions filtered by category"""
        return [p for p in self.predictions if p.get('category') == category]
    
    def get_predictions_by_priority(self, priority: str) -> List[Dict]:
        """Get predictions filtered by priority"""
        return [p for p in self.predictions if p.get('priority') == priority]
    
    def get_predictions_by_sentiment(self, sentiment: str) -> List[Dict]:
        """Get predictions filtered by sentiment"""
        return [p for p in self.predictions if p.get('sentiment') == sentiment]
    
    def get_predictions_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get predictions within a date range"""
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            result = []
            for p in self.predictions:
                p_time = datetime.fromisoformat(p.get('timestamp'))
                if start <= p_time <= end:
                    result.append(p)
            return result
        except:
            return []
    
    def update_user_feedback(self, ticket_id: str, feedback: str, rating: int = None):
        """Update user feedback for a specific ticket"""
        for p in self.predictions:
            if p.get('ticket_id') == ticket_id:
                p['user_feedback'] = {
                    'feedback': feedback,
                    'rating': rating,
                    'timestamp': datetime.now().isoformat()
                }
                self._save_to_file()
                return True
        return False
    
    def export_csv(self, filename: str = "predictions_export.csv"):
        """Export predictions to CSV"""
        import pandas as pd
        if not self.predictions:
            logger.info("No predictions to export")
            return
        
        df = pd.DataFrame(self.predictions)
        df.to_csv(filename, index=False)
        logger.info(f"✅ Exported {len(df)} predictions to {filename}")
        
        return filename
    
    def get_recent_tickets(self, limit: int = 20) -> List[Dict]:
        """Get most recent tickets"""
        return self.predictions[-limit:][::-1]


_metrics = None

def get_metrics(storage_file: str = "metrics_data.json"):
    """Get singleton metrics collector"""
    global _metrics
    if _metrics is None:
        _metrics = MetricsCollector(storage_file)
    return _metrics