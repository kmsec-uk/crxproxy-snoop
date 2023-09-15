# CRXSnooper
This was built to snoop a backdoored extension's activity.

Simply run with `docker compose up -d --scale snooper=<number of snoopers>`. Running multiple snoopers maximises the chance of receiving interesting commands from the C2.

Check logs in the ./logs directory, or run `docker compose logs -f` to tail output live

## Backdoored extension
The culprit extension is `lnebjgioddkafaldaaeooeghlcholnnp`: Find website used fonts.

Two days after installation the extension initiates a background websocket connection to wss://ext.hanaila[.]com. The infected host then listens for commands from the C2.

I created this project to listen in on the commands being sent to the infected hosts to understand what the purpose of this backdoor is.

## Findings
Initial findings suggest that this extension is being used as a botnet to piggyback off of infected clients to proxy web requests.

The C2 sends a message like this and expects the infected client to retrieve the contents of the url and return them in the response payload:

```JSON
{
  "action": "request",
  "url": "https://stackoverflow.com/",
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0.14393......"
  },
  "browser": "tcp",
  "incognito": "true"
}
```
Disparate user agents across these `request` payloads suggest these are coming from many different clients (or one client that is randomising their user agent). One working theory is that this is backend infrastructure for a morally questionable proxy service.

One consistency among all infected hosts are periodic requests from the C2 to visit api.ipgeolocation[.]io with a hardcoded, consistent API key across infected users. The API key is 04121b22f4244f55a04a496edcc8fd9a. It appears that this API key

## IOCs

```
ext.hanaila[.]com
https://https://api.ipgeolocation[.].io/ipgeo?apiKey=04121b22f4244f55a04a496edcc8fd9a&include=hostname,security,useragent&ip=<some_ip>
```