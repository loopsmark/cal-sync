import time
import yaml
from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeEvent, EKAuthorizationStatusAuthorized, EKEvent

# Load YAML configuration file
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()

# Get values from the configuration
SRC_ACCOUNT = config.get("source_account", "Exchange")
SRC_CAL = config.get("source_calendar", "Calendar")
DST_ACCOUNT = config.get("destination_account", "iCloud")
DST_CAL = config.get("destination_calendar", "Work")
TIME_BACK = config.get("time_back", 0)
TIME_FRW = config.get("time_forward", 1)

def create_event_key(event):
    start_time = event.startDate().timeIntervalSince1970()
    end_time = event.endDate().timeIntervalSince1970()
    return (event.title(), start_time, end_time)

def copy_calendar_events():
    store = EKEventStore.alloc().init()

    # Check the current authorization status
    authorization_status = EKEventStore.authorizationStatusForEntityType_(EKEntityTypeEvent)
    access_granted = False
    access_done = False

    if authorization_status != EKAuthorizationStatusAuthorized:
        def completion_handler(granted, error):
            nonlocal access_granted, access_done
            access_granted = granted
            access_done = True

        # Request access to the Calendar
        store.requestAccessToEntityType_completion_(EKEntityTypeEvent, completion_handler)

        # Wait until the user responds to the permission dialog
        while not access_done:
            time.sleep(0.1)

        if not access_granted:
            print("Access to Calendar not granted")
            return  # Exit the function gracefully
    else:
        access_granted = True

    if access_granted:
        # Get source and destination calendars
        calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
        source_calendar = None
        destination_calendar = None

        for cal in calendars:
            if cal.title() == SRC_CAL and cal.source().title() == SRC_ACCOUNT:
                source_calendar = cal
            if cal.title() == DST_CAL and cal.source().title() == DST_ACCOUNT:
                destination_calendar = cal

        if not source_calendar:
            print(f"Source calendar '{SRC_CAL}' not found.")
            return

        if not destination_calendar:
            print(f"Destination calendar '{DST_CAL}' not found.")
            return

        # Define the date range for events to copy (adjust as needed)
        start_date = NSDate.dateWithTimeIntervalSinceNow_(-3600*24*TIME_BACK)
        end_date = NSDate.dateWithTimeIntervalSinceNow_(3600*24*TIME_FRW)

    # Fetch events from both calendars
    source_events = store.eventsMatchingPredicate_(store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [source_calendar]))
    destination_events = store.eventsMatchingPredicate_(store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [destination_calendar]))

    # Index destination events by title, start, and end time for quick lookup
    destination_event_map = {create_event_key(event): event for event in destination_events}

    # Copy or update events
    for source_event in source_events:
        key = create_event_key(source_event)
        if key in destination_event_map:
            dest_event = destination_event_map[key]
            # If the event exists but has changed, update it
            if source_event.notes() != dest_event.notes() or source_event.location() != dest_event.location():
                print(f"Updating event: {source_event.title()}")
                dest_event.setNotes_(source_event.notes())
                dest_event.setLocation_(source_event.location())
                store.saveEvent_span_error_(dest_event, 0, None)
            del destination_event_map[key]
        else:
            # Create a new event in the destination calendar
            new_event = EKEvent.eventWithEventStore_(store)
            new_event.setTitle_(source_event.title())
            new_event.setStartDate_(source_event.startDate())
            new_event.setEndDate_(source_event.endDate())
            new_event.setLocation_(source_event.location())
            new_event.setCalendar_(destination_calendar)
            new_event.setNotes_(source_event.notes())
            store.saveEvent_span_error_(new_event, 0, None)

            success, error = store.saveEvent_span_error_(new_event, 0, None)
            if success:
                print(f"Copied event: {new_event.title()}")
            else:
                print(f"Failed to copy event: {source_event.title()}, Error: {error}")

    # Delete events in the destination calendar that no longer exist in the source calendar
    for event_key, dest_event in destination_event_map.items():
        print(f"Deleting event: {dest_event.title()}")
        store.removeEvent_span_error_(dest_event, 0, None)

if __name__ == "__main__":
    copy_calendar_events()