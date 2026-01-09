import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TrendEngineService:
    """Service for analyzing skill trends over time"""
    
    # Thresholds for trend classification (percentage change)
    RISING_THRESHOLD = 0.15  # 15% increase to be considered rising
    DECLINING_THRESHOLD = -0.15  # 15% decrease to be considered declining
    STABLE_THRESHOLD_LOW = -0.05  # Within 5% change is considered stable
    STABLE_THRESHOLD_HIGH = 0.05
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize trend engine service
        
        Args:
            data_dir: Optional directory path for storing historical data
        """
        # Get the path to the data directory
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            current_dir = Path(__file__).parent
            self.data_dir = current_dir.parent / 'data' / 'trends'
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_skill_frequencies(self, skill_counts: Dict[str, int], period: Optional[str] = None) -> str:
        """
        Save skill frequency data for a specific period
        
        Args:
            skill_counts: Dictionary with skill names as keys and counts as values
            period: Optional period identifier (e.g., "2024-01", "week-1"). 
                   If not provided, uses current date in YYYY-MM-DD format
        
        Returns:
            The period identifier used
        """
        if not period:
            period = datetime.now().strftime('%Y-%m-%d')
        
        # Create data entry
        data_entry = {
            'period': period,
            'timestamp': datetime.now().isoformat(),
            'skill_counts': skill_counts,
            'total_occurrences': sum(skill_counts.values()),
            'unique_skills': len(skill_counts)
        }
        
        # Load existing data or create new
        data_file = self.data_dir / 'historical_data.json'
        historical_data = self._load_historical_data()
        
        # Add or update period data
        historical_data[period] = data_entry
        
        # Save back to file
        self._save_historical_data(historical_data)
        
        return period
    
    def analyze_trends(self, current_skill_counts: Dict[str, int], 
                      comparison_period: Optional[str] = None,
                      periods_back: int = 1) -> Dict[str, Dict]:
        """
        Analyze trends by comparing current skill frequencies with historical data
        
        Args:
            current_skill_counts: Current period skill counts
            comparison_period: Optional specific period to compare against.
                             If not provided, compares with the most recent period
            periods_back: Number of periods to look back (default: 1)
        
        Returns:
            Dictionary with skill names as keys and trend analysis as values
        """
        historical_data = self._load_historical_data()
        
        if not historical_data:
            # No historical data available
            return self._classify_all_as_new(current_skill_counts)
        
        # Get comparison period data
        if comparison_period:
            comparison_data = historical_data.get(comparison_period)
            if not comparison_data:
                return self._classify_all_as_new(current_skill_counts)
            comparison_counts = comparison_data.get('skill_counts', {})
        else:
            # Get the most recent period
            sorted_periods = sorted(historical_data.keys(), reverse=True)
            if not sorted_periods:
                return self._classify_all_as_new(current_skill_counts)
            
            # Get the period that is 'periods_back' positions from the end
            target_index = min(periods_back - 1, len(sorted_periods) - 1)
            comparison_period_key = sorted_periods[target_index]
            comparison_data = historical_data[comparison_period_key]
            comparison_counts = comparison_data.get('skill_counts', {})
        
        # Calculate trends for all skills
        trends = {}
        
        # Get all unique skills from both periods
        all_skills = set(current_skill_counts.keys()) | set(comparison_counts.keys())
        
        for skill in all_skills:
            current_count = current_skill_counts.get(skill, 0)
            previous_count = comparison_counts.get(skill, 0)
            
            # Calculate percentage change
            if previous_count == 0:
                if current_count > 0:
                    # New skill - 100% increase
                    percentage_change = 1.0
                    classification = 'rising'
                else:
                    # Skill didn't exist in either period
                    continue
            else:
                percentage_change = (current_count - previous_count) / previous_count
                classification = self._classify_trend(percentage_change)
            
            # Calculate absolute change
            absolute_change = current_count - previous_count
            
            trends[skill] = {
                'skill': skill,
                'current_count': current_count,
                'previous_count': previous_count,
                'absolute_change': absolute_change,
                'percentage_change': round(percentage_change * 100, 2),  # As percentage
                'trend': classification
            }
        
        return trends
    
    def _classify_trend(self, percentage_change: float) -> str:
        """
        Classify a skill trend based on percentage change
        
        Args:
            percentage_change: Percentage change as a decimal (e.g., 0.15 for 15%)
        
        Returns:
            Trend classification: 'rising', 'stable', or 'declining'
        """
        if percentage_change >= self.RISING_THRESHOLD:
            return 'rising'
        elif percentage_change <= self.DECLINING_THRESHOLD:
            return 'declining'
        else:
            return 'stable'
    
    def _classify_all_as_new(self, skill_counts: Dict[str, int]) -> Dict[str, Dict]:
        """
        Classify all skills as new/rising when no historical data exists
        
        Args:
            skill_counts: Current skill counts
        
        Returns:
            Dictionary with all skills classified as 'rising'
        """
        trends = {}
        for skill, count in skill_counts.items():
            trends[skill] = {
                'skill': skill,
                'current_count': count,
                'previous_count': 0,
                'absolute_change': count,
                'percentage_change': 100.0,
                'trend': 'rising'
            }
        return trends
    
    def get_trend_summary(self, trends: Dict[str, Dict]) -> Dict[str, List[Dict]]:
        """
        Get summary of trends grouped by classification
        
        Args:
            trends: Dictionary of trend analysis results
        
        Returns:
            Dictionary with 'rising', 'stable', and 'declining' lists
        """
        summary = {
            'rising': [],
            'stable': [],
            'declining': []
        }
        
        for skill_data in trends.values():
            trend_type = skill_data['trend']
            summary[trend_type].append(skill_data)
        
        # Sort each category by absolute change (descending)
        summary['rising'].sort(key=lambda x: abs(x['absolute_change']), reverse=True)
        summary['stable'].sort(key=lambda x: abs(x['absolute_change']), reverse=True)
        summary['declining'].sort(key=lambda x: abs(x['absolute_change']), reverse=True)
        
        return summary
    
    def _load_historical_data(self) -> Dict:
        """Load historical data from JSON file"""
        data_file = self.data_dir / 'historical_data.json'
        
        if not data_file.exists():
            return {}
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_historical_data(self, data: Dict) -> None:
        """Save historical data to JSON file"""
        data_file = self.data_dir / 'historical_data.json'
        
        try:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save historical data: {e}")
    
    def get_historical_periods(self) -> List[str]:
        """
        Get list of all available historical periods
        
        Returns:
            List of period identifiers, sorted by date (most recent first)
        """
        historical_data = self._load_historical_data()
        periods = sorted(historical_data.keys(), reverse=True)
        return periods
    
    def clear_historical_data(self, before_period: Optional[str] = None) -> int:
        """
        Clear historical data
        
        Args:
            before_period: Optional period to clear data before. 
                          If None, clears all data
        
        Returns:
            Number of periods removed
        """
        historical_data = self._load_historical_data()
        
        if not before_period:
            count = len(historical_data)
            historical_data.clear()
        else:
            periods_to_remove = [p for p in historical_data.keys() if p < before_period]
            count = len(periods_to_remove)
            for period in periods_to_remove:
                del historical_data[period]
        
        self._save_historical_data(historical_data)
        return count

