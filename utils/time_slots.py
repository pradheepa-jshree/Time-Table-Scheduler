DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI']
HOURS = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']


def generate_slots(days=DAYS, hours=HOURS) -> list[str]:
    """
    Generate all time slots combining days and hours.
    Result: 40 slots total — ['MON-09:00', ..., 'FRI-17:00']
    """
    return [f'{d}-{h}' for d in days for h in hours]
