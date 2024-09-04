import gps

# Create a GPS session
session = gps.gps(mode=gps.WATCH_ENABLE)

while True:
    try:
        # Poll for data
        report = session.next()
        if report['class'] == 'TPV':
            # Extract time
            if hasattr(report, 'time'):
                gps_time = report.time
                # Convert GPS time to human-readable format
                formatted_time = gps_time.strftime('%H:%M:%S')
                print(f"GPS Time: {formatted_time}")
    except KeyError:
        pass  # Handle missing keys
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(f"Error: {e}")
