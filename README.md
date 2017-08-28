# WorkshopMaker

Sets up EventBrite events for workshops provided by our team.

## Input

Script reads `input.yml` file with definition to setup workshops

```yaml
password: <event password>
capacity: <class capacity>

token: <eventbrite token>
organizer: <eventbrite organizer id>

events:
  - who: Presenter's name
    tz: Present's TimeZone, e.g. America/New_York
    when:
      - Date and time, one workshop instance per list item, in format 
      - Mon-Day Year Time
      - e.g. Sep-11 2017 10am
```

## Output

The script will create the EventBrite events, or will fetch event's information and
print out `result.csv` file in format

```csv
Date,Time,Link,Status,Presenter,Capacity,Password
```

## Running the program

```bash
$ python3 creator.py
```

## License

Released under the [MIT License](https://opensource.org/licenses/MIT).