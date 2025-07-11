from main import main

def run_reminder(request):
    main()
    return "Reminder job executed.", 200