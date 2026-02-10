## Student Name: Kyle Williamson
## Student ID: 218953901

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """

    # Constants
    BUSINESS_START = "09:00"
    BUSINESS_END = "17:00"
    FRIDAY_END = "15:00"
    LUNCH_START = "12:00"
    LUNCH_END = "13:00"
    SLOT_INCREMENT = 15  # Generate slots every 30 minutes
    
    def time_to_minutes(time_str: str) -> int:
        """Convert HH:MM format to minutes since midnight."""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def minutes_to_time(minutes: int) -> str:
        """Convert minutes since midnight to HH:MM format."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def is_during_lunch(start_time_min: int, duration: int) -> bool:
            """Check if a meeting overlaps with lunch break."""
            lunch_start_min = time_to_minutes(LUNCH_START)
            lunch_end_min = time_to_minutes(LUNCH_END)
            meeting_end_min = start_time_min + duration
            
            # Meeting overlaps lunch if it starts before lunch ends AND ends after lunch starts
            return start_time_min < lunch_end_min and meeting_end_min > lunch_start_min


    # Convert business hours to minutes for easier calculation
    business_start_min = time_to_minutes(BUSINESS_START)
    business_end_min = time_to_minutes(BUSINESS_END)

    # Adjust business end time for Friday
    if day == "Fri" or (isinstance(day, str) and len(day) > 3):
        # Handle both "Fri" and date strings like "2026-02-01"
        # For simplicity, check if it's explicitly "Fri" or a date string
        if day == "Fri":
            business_end_min = time_to_minutes(FRIDAY_END)


    lunch_event = {"start": LUNCH_START, "end": LUNCH_END}
    all_events = events + [lunch_event]

    # Handle empty calendar - full day available
    if not events:
        available_slots = []
        slot_time = business_start_min
        while slot_time + meeting_duration <= business_end_min:
            if not is_during_lunch(slot_time, meeting_duration):
                available_slots.append(minutes_to_time(slot_time))
            slot_time += SLOT_INCREMENT
        return available_slots
    
    # Sort events by start time to process chronologically
    sorted_events = sorted(events, key=lambda e: time_to_minutes(e["start"]))
    
    # Find available time slots between events
    available_slots = []
    current_time = business_start_min
    
    for event in sorted_events:
        event_start = time_to_minutes(event["start"])
        event_end = time_to_minutes(event["end"])
        
        # Generate slots in the gap before this event
        slot_time = current_time
        while slot_time + meeting_duration < event_start:
            if not is_during_lunch(slot_time, meeting_duration):
                available_slots.append(minutes_to_time(slot_time))
            slot_time += SLOT_INCREMENT
        
        # Move current_time to the end of this event
        current_time = max(current_time, event_end)
    
    # Generate slots from end of last event to end of business day
    slot_time = current_time
    while slot_time + meeting_duration <= business_end_min:
        if not is_during_lunch(slot_time, meeting_duration):
                available_slots.append(minutes_to_time(slot_time))
        slot_time += SLOT_INCREMENT
    
    return available_slots
    # TODO: Implement this function
    raise NotImplementedError("suggest_slots function has not been implemented yet")