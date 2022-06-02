import rumps
import clipboard
import sync
import vika_api
import todoist

rumps.debug_mode(True)

x = 0
current_task = ''


class AwesomeStatusBarApp(rumps.App):

    @rumps.clicked('🔥 start')
    def start(self, sender):
        global x, current_task
        print('start')
        win = rumps.Window("hello", ok="fire", cancel="cancel",
                           default_text=clipboard.paste())
        resp = win.run()
        print(resp)
        if resp.clicked:
            url = resp.text
            task = todoist.get_task_by_url(url)
            current_task = task['task'].content
            if x == 0:
                x = 25*60
                timer.start()

            sync.sync(url)

    @rumps.clicked('💤 relax')
    def relax(self, _):
        global x, current_task
        current_task = ''
        x = 5 * 60
        timer.start()
        vika_api.insert_relax()

    @rumps.clicked('💢 break')
    def break_(self, _):
        vika_api.insert_break()

    @rumps.clicked('🛌 big relax')
    def big(self, _):
        global x
        x = 20 * 60
        timer.start()
        vika_api.insert_label('big')

    @rumps.clicked('⏸️ pause')
    def pause(self, sender):
        global x
        if x == 0:
            return
        if timer.is_alive():
            timer.stop()
            sender.title = '▶️ resume'
        else:
            timer.start()
            sender.title = '⏸️ pause'

    @rumps.clicked("🛑 stop")
    def stop(self, _):
        global x
        x = 0
        timer.stop()
        app.title = 'pomoist'


def tick(sender):
    global x, current_task
    print(sender)
    x -= 1
    app.title = f'{current_task} {time(x)}'
    if x == 0:
        timer.stop()
        rumps.notification("Awesome title", "amazing subtitle", "done")
        app.title = 'pomoist'


def time(x):
    return f'{x // 60:02d}:{x % 60:02d}'


timer = rumps.Timer(tick, 1)
app = AwesomeStatusBarApp("pomoist")
app.run()
