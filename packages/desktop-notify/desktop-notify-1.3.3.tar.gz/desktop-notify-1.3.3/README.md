# DESKTOP-NOTIFY

Util for sending desktop notifications over dbus. Supports replace_id, hints and actions(mainloop required).

## Package usage

### Basic notify:
```python
notify = desktop_notify.aio.Notify('summary', 'body')
await notify.show()
```
```python
notify = desktop_notify.glib.Notify('summary', 'body')
notify.set_on_show(callback) # optional
notify.show()
# or
notify.show_async()
```

### Usage with server:
```python
server = desktop_notify.aio.Server('app_name')
notify = server.Notify('summary')
await notify.show()
```
### Configure notify.
You can setnotify options by default property setter `notify.body = 'body'` or using fluent setters:
```python
notify.set_id(0)\
	.set_icon('icon')\
	.set_timeout(10000) # ms
```

### Extra options

#### Hints

For workings with hints use this methods:

```python
notify.set_hint(key, value)
notify.get_hint(key)
notify.del_hint(key)
```

#### Actions

**For using actions and event you need to specify notify server mainloop.**

You can add or delete action:

```python
notify.add_action(desktop_notify.Action('label', callback))
notify.del_action(desktop_notify.Action('label', callback))
```

Also supported `on_show` and `on_close` event:

```python
notify.set_on_show(callback(notify))
notify.set_on_close(callback(notify, close_reason))
```

## Console usage

```bash
usage: desktop-notify [--help] [--icon ICON] [--id REPLACE_ID] [--timeout TIMEOUT]
               [--hints key:value [key:value ...]]
               Summary [Body]

Send desktop notification. Returns created notification's id.

positional arguments:
  Summary               The summary text briefly describing the notification.
  Body                  The optional detailed body text. Can be empty.

optional arguments:
  --help                show this help message and exit
  --icon ICON, -i ICON  The optional program icon of the calling application.
                        Should be either a file path or a name in a
                        freedesktop.org-compliant icon theme.
  --id REPLACE_ID       An optional ID of an existing notification that this
                        notification is intended to replace.
  --timeout TIMEOUT, -t TIMEOUT
                        The timeout time in milliseconds since the display of
                        the notification at which the notification should
                        automatically close.
  --hints key:signature:value [key:signature:value ...], -h key:signature:value [key:signature:value ...]
                        use "--" to separate hints list from positional args
```

