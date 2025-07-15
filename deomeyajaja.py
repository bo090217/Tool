import sys, os; sys.dont_write_bytecode = True; os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from api import *
from api.plugins.log import *
from api.plugins.ui import *
from api.dchelper import *
from api.plugins.client import client
from api.plugins.threads import * 
from urllib.parse import urlparse
from rich.console import Console
from api.plugins.files import *
import asyncio
import tempfile

console = Console()

f = "input/tokens.txt"

class UI:
    def prep(self, toolname):
        self.cls()
        self.banner()
        console.print(f"[bold cyan][[bold magenta]{toolname}[bold cyan]] [bold white]Starting...[/bold white]\n")

    def banner(self):
        console.print("[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold magenta]       ██████╗ ███████╗██╗    ██╗  ██╗       [/bold magenta]")
        console.print("[bold magenta]       ██╔══██╗╚════██║██║    ╚██╗██╔╝[/bold magenta]")
        console.print("[bold cyan]              ██║  ██║   ███╔╝██║     ╚███╔╝ [/bold cyan]")
        console.print("[bold cyan]              ██║  ██║  ██╔╝  ██║     ██╔██╗ [/bold cyan]")
        console.print("[bold magenta]       ██████╔╝ ███████╗██║    ██╔╝╚██╗[/bold magenta]")
        console.print("[bold cyan]              ╚═════╝  ╚══════╝╚═╝    ╚═╝  ╚═╝ [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold green]      Tool By : [bold white]Nguyễn Hiếu[/bold white] - Discord Tool[/bold green]")
        console.print("[bold yellow]      Telegram : [bold blue][link]t.me/frv_23th04[/link][/bold blue] | Zalo : [bold white]0827199814[/bold white][/bold yellow]")
        console.print("[bold cyan]═══════════════════════════════════════════════════════[/bold cyan]")
        print()

    def versionn(self):
        console.print("[bold yellow]Version: [bold cyan]1.0.0[/bold cyan]\n")

    def dume(self):
        console.print("[bold red]Note: [bold white]Please ensure tokens are loaded in input/tokens.txt[/bold white]\n")

    def menu(self):
        console.print("[bold cyan][1] [bold white]Joiner[/bold white]")
        console.print("[bold cyan][2] [bold white]Leaver[/bold white]")
        console.print("[bold cyan][3] [bold white]Reaction[/bold white]")
        console.print("[bold cyan][4] [bold white]Server Checker[/bold white]")
        console.print("[bold cyan][5] [bold white]Token Checker[/bold white]")
        console.print("[bold cyan][6] [bold white]Avatar Changer[/bold white]")
        console.print("[bold cyan][7] [bold white]Display Name Changer[/bold white]")
        console.print("[bold cyan][8] [bold white]Pronouns Changer[/bold white]\n")

    def ask(self, question, boolean=False):
        if boolean:
            console.print(f"[bold cyan][?] [bold white]{question} [Y/N]: [/bold white]", end="")
            choice = input().strip().lower()
            return choice in ['y', 'yes']
        else:
            console.print(f"[bold cyan][?] [bold white]{question}: [/bold white]", end="")
            return input().strip()

    def make_menu(self, items):
        for i, item in enumerate(items, 1):
            console.print(f"[bold cyan][{i}] [bold white]{item}[/bold white]")
        print()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

ui = UI

# Các lớp còn lại giữ nguyên
class reaction:
    def __init__(self):
        self.serverid = None
        self.channelid = None
        self.messageid = None
        self.reaction = None
        self.dodebypass = False

    def bypass(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token

        r = cl.sess.put(
            f'https://discord.com/api/v9/channels/{self.channelid}/messages/{self.messageid}/reactions/{self.reaction}/@me?location=Message&type=0',
            headers=cl.headers,
            cookies=cl.cookies
        )

        log.dbg('Reaction', r.text, r.status_code)

        if r.status_code == 204:
            log.info('Reaction', f'{token[:30]}... >> Added Reaction >> {reactionname}')

        elif 'retry_after' in r.text:
            limit = r.json()['retry_after']
            log.warn('Reaction', f'{token[:30]}... >> Limited for {limit}s')
            time.sleep(float(limit))
            self.bypass(token)

        elif 'Cloudflare' in r.text:
            log.warn('Reaction', f'{token[:30]}... >> CLOUDFLARE BLOCKED >> Waiting for 5 secs and retrying')
            time.sleep(5)
            self.bypass(token)

        elif 'captcha_key' in r.text:
            log.hcap('Reaction', f'{token[:30]}... >> HCAPTCHA')

        elif 'You need to verify' in r.text:
            log.critical('Reaction', f'{token[:30]}... >> LOCKED')

        else:
            error = log.errordatabase(r.text)
            log.error('Reaction', error)
    
    def debypass(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token

        r = cl.sess.delete(
            f'https://discord.com/api/v9/channels/{self.channelid}/messages/{self.messageid}/reactions/{self.reaction}/@me?location=Message&type=0',
            headers=cl.headers,
            cookies=cl.cookies
        )
    
        log.dbg('De Reaction', r.text, r.status_code)

        if r.status_code == 204:
            log.info('De Reaction', f'{token[:30]}... >> Remove Reaction')

        elif 'retry_after' in r.text:
            limit = r.json()['retry_after']
            log.warn('De Reaction', f'{token[:30]}... >> Limited for {limit}s')
            time.sleep(float(limit))
            self.debypass(token)

        elif 'Cloudflare' in r.text:
            log.warn('De Reaction', f'{token[:30]}... >> CLOUDFLARE BLOCKED >> Waiting for 5 secs and retrying')
            time.sleep(5)
            self.bypass(token)

        elif 'captcha_key' in r.text:
            log.hcap('De Reaction', f'{token[:30]}... >> HCAPTCHA')

        elif 'You need to verify' in r.text:
            log.critical('De Reaction', f'{token[:30]}... >> LOCKED')

        else:
            error = log.errordatabase(r.text)
            log.error('De Reaction', error)

    async def main(self):
        ui().prep('Reaction')
        self.serverid = ui().ask('ID Server')
        self.channelid = ui().ask('ID Channel')
        self.messageid = ui().ask('ID Message')
        self.dodebypass = ui().ask('Bạn Có Muốn Xóa Reaction Trước Khi Thêm Lại?', True)

        reacts = []
        messages = discordhelper().get_messages(self.channelid, files.gettokens())
        for message in messages:
            if message['id'] == self.messageid:
                for reaction in message['reactions']:
                    emoji_name = reaction['emoji']['name']
                    count = reaction['count']
                    reacts.append((emoji_name, count))
        
        if not reacts:
            log.info('Reaction', 'Không Tìm Thấy Reaction')
            return

        mn = []
        for _, (reactionname, count) in enumerate(reacts, 1):
            mn.append(f'{reactionname} - {count}')

        ui().make_menu(mn)
        selected = int(ui().ask('Choice')) - 1
        self.reaction = reacts[selected][0]

        if self.dodebypass:
            await thread(
                files.getthreads(),
                self.debypass,
                files.gettokens(),
                []
            )

        await asyncio.sleep(1)

        await thread(
            files.getthreads(),
            self.bypass,
            files.gettokens(),
            []
        )

class joiner:
    def __init__(self):
        self.invite = None
        self.serverid = None
        self.servername = None
        self.delay = 1.5
        self.success_count = 0
        self.faild_count = 0
        self.hcaptcha_count = 0

    def discoverinvite(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        r = cl.sess.get(
            f'https://discord.com/api/v9/invites/{self.invite}?inputValue={self.invite}&with_counts=true&with_expiration=true',
            headers=cl.headers,
            cookies=cl.cookies
        )
        log.dbg('Discover invite', r.text, r.status_code)
        if r.status_code == 200: 
            self.serverid = r.json().get('guild', {}).get('id')
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Joiner [discover invite]', f'{token[:30]}... >> Limited for {limit}s')
            time.sleep(float(limit))
            self.discoverinvite(token)
        elif 'Cloudflare' in r.text:
            log.warn('Joiner [discover invite]', f'{token[:30]}... >> CLOUDFLARE BLOCKED >> Waiting for 5 secs and retrying')
            time.sleep(5)
            self.discoverinvite(token)
        elif 'You need to verify' in r.text:
            log.critical('Joiner [discover invite]', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Joiner [discover invite]', error)

    def join(self, token, cl=None):
        if cl is None:
            cl = client(token)
        cl.headers['Authorization'] = token
        self.sessionid = uuid.uuid4().hex
        payload = {
            'session_id': self.sessionid
        }
        r = cl.sess.post(
            f'https://discord.com/api/v9/invites/{self.invite}',
            headers=cl.headers,
            cookies=cl.cookies,
            json=payload
        )
        log.dbg('Joiner', r.text, r.status_code)
        if r.status_code == 200:
            log.info('Joiner', f'{token[:30]} >> Joiner >> {self.servername} >> discord.gg/{self.invite}')
            self.serverid = r.json().get('guild', {}).get('id')
            self.success_count += 1
            self.check_onboarding(token, cl)
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Joiner', f'{token[:30]}... >> Limited For {limit}s')
            time.sleep(float(limit))
            self.join(token)
        elif 'Cloudflare' in r.text:
            log.warn('Joiner', f'{token[:30]}... >> CLOUDFLARE BLOCKED')
            time.sleep(5)
            self.join(token)
        elif 'captcha_key' in r.text:
            log.hcap('Joiner', f'{token[:30]}... >> HCAPTCHA')
            self.hcaptcha_count += 1
        elif 'You need to verify' in r.text:
            log.critical('Joiner', f'{token[:30]}... >> Verify Account Discord')
            self.faild_count += 1
        else:
            error = log.errordatabase(r.text)
            log.error('Joiner', error)
            self.faild_count += 1

    def check_onboarding(self, token, cl):
        r = cl.sess.get(
            f'https://discord.com/api/v9/guilds/{self.serverid}/onboarding',
            headers=cl.headers,
            cookies=cl.cookies
        )
        if r.status_code == 200 and r.json().get('enabled'):
            prompts = r.json().get('prompts', [])
            if prompts:
                onboarding_responses = []
                onboarding_prompts_seen = {}
                for prompt in prompts:
                    options = prompt.get('options', [])
                    if options:
                        onboarding_responses.append({
                            'prompt_id': prompt['id'],
                            'option_ids': [options[0]['id']]
                        })
                        onboarding_prompts_seen[prompt['id']] = int(time.time() * 1000)
                
                if onboarding_responses:
                    payload = {
                        'onboarding_responses': onboarding_responses,
                        'onboarding_prompts_seen': onboarding_prompts_seen,
                        'onboarding_responses_seen': {}
                    }
                    r2 = cl.sess.put(
                        f'https://discord.com/api/v9/guilds/{self.serverid}/onboarding-responses',
                        headers=cl.headers,
                        cookies=cl.cookies,
                        json=payload
                    )
                    if r2.status_code == 200:
                        log.info('Joiner', f'{token[:30]} >> On Boarding >> discord.gg/{self.invite}')
                    elif 'retry_after' in r.text:
                        limit = r.json().get('retry_after', 1.5)
                        log.warn('Joiner', f'{token[:30]}... >> Limited For {limit}s')
                        time.sleep(float(limit))
                        self.check_onboarding(token, cl)
                    else:
                        error = log.errordatabase(r.text)
                        log.error('Joiner', error)

    def main(self):
        ui().prep('Joiner')
        self.invite = ui().ask('Nhập Link Server')
        self.invite = discordhelper().extract_invite(self.invite)
        invinfo = discordhelper().get_invite_info(self.invite)
        self.serverid = invinfo.get('guild', {}).get('id', None)
        self.servername = invinfo.get('guild', {}).get('name', None)

        self.success_count = 0
        self.faild_count = 0
        self.hcaptcha_count = 0

        thread(
            files.getthreads(),
            self.join,
            files.gettokens(),
            [],
            False,
            self.delay
        )

        console.print(f"[bold black][[bold green]JOINER[bold black]] >> [bold green]{self.success_count} "
              f"[bold black]| [[bold red]FAILD[bold black]] >> [bold red]{self.faild_count} "
              f"[bold black]| [[bold cyan]HCAPTCHA[bold black]] >> [bold cyan]{self.hcaptcha_count}")

class isinserver:
    def __init__(self):
        self.serverid = None
        self.delay = 0.1
        self.valid_tokens = []

    def check(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        r = cl.sess.get(
            f'https://discord.com/api/v9/guilds/{self.serverid}',
            headers=cl.headers,
            cookies=cl.cookies
        )
        log.dbg('Checker Server', r.text, r.status_code)
        if r.status_code == 200:
            log.info('Checker Server', f'{token[:30]}... >> Is in >> {self.serverid}')
            self.valid_tokens.append(token)
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Checker Server', f'{token[:30]}... >> Limited For {limit}s')
            time.sleep(float(limit))
            self.check(token)
        elif 'Cloudflare' in r.text:
            log.warn('Checker Server', f'{token[:30]}... >> CLOUDFLARE BLOCKED')
            time.sleep(5)
            self.check(token)
        elif 'captcha_key' in r.text:
            log.hcap('Checker Server', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Checker Server', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Checker Server', error)
    
    def savetk(self):
        try:
            with open('input/isinserver.txt', 'w') as file:
                for token in self.valid_tokens:
                    file.write(f"{token}\n")

        except Exception as e:
            log.error('Token Saver', f'Lỗi Khi Lưu File: {str(e)}')
    
    def main(self):
        ui().prep('Server Checker')
        self.serverid = ui().ask('Nhập ID Server')
        thread(
            files.getthreads(),
            self.check,
            files.gettokens(),
            [],
            False,
            self.delay
        )
        
        save_choice = ui().ask("Bạn Có Muốn Lưu Token Vào File isinserver.txt Không?", True)
        if save_choice:
            self.savetk()

class checker:
    def __init__(self):
        self.serverid = None
        self.valids = []
        self.delay = 0.1

    def check(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        r = cl.sess.get(
            'https://discord.com/api/v9/users/@me/library',
            headers=cl.headers,
            cookies=cl.cookies
        )
        log.dbg('Checker', r.text, r.status_code)
        if r.status_code == 200:
            self.valids.append(token)
            log.info('Checker', f'{token[:30]}... >> ONLINE', False, True, True)
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Checker', f'{token[:30]}... >> Limited For {limit}s')
            time.sleep(float(limit))
            self.check(token)
        elif 'Cloudflare' in r.text:
            log.warn('Checker', f'{token[:30]}... >> CLOUDFLARE BLOCKED')
            time.sleep(5)
            self.check(token)
        elif 'captcha_key' in r.text:
            log.hcap('Checker', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Checker', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Checker', error)
    
    def main(self):
        ui().prep('Checker Token')
        thread(
            files.getthreads(),
            self.check,
            files.gettokens(),
            [],
            False,
            self.delay
        )
        if self.valids:
            save = ui().ask('Replace tokens.txt With Only Valid Tokens', True)
            if save:
                with open('input/tokens.txt', 'w') as f:
                    f.write('\n'.join(self.valids))

class displaychanger:
    def __init__(self):
        self.newdisplay = None
        self.delay = 0.1

    def change(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        payload = {
            'global_name': self.newdisplay
        }
        r = cl.sess.patch(
            f'https://discord.com/api/v9/users/@me',
            headers=cl.headers,
            cookies=cl.cookies,
            json=payload
        )
        log.dbg('Display Changer', r.text, r.status_code)
        if r.status_code == 200:
            log.info('Display Changer', f'{token[:30]}... >> Changed to >> {self.newdisplay}')
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Display Changer', f'{token[:30]}... >> Limited for {limit}s')
            time.sleep(float(limit))
            self.change(token)
        elif 'Cloudflare' in r.text:
            log.warn('Display Changer', f'{token[:30]}... >> CLOUDFLARE BLOCKED >> Waiting for 5 secs and retrying')
            time.sleep(5)
            self.change(token)
        elif 'captcha_key' in r.text:
            log.hcap('Display Changer', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Display Changer', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Display changer', error)
    
    def main(self):
        ui().prep('Change Name')
        self.newdisplay = ui().ask('Nhập Tên Muốn Set')
        thread(
            files.getthreads(),
            self.change,
            files.gettokens(),
            [],
            False,
            self.delay
        )

class pronchanger:
    def __init__(self):
        self.newpron = None
        self.delay = 0.1

    def change(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        payload = {
            'pronouns': self.newpron
        }
        r = cl.sess.patch(
            f'https://discord.com/api/v9/users/@me/profile',
            headers=cl.headers,
            cookies=cl.cookies,
            json=payload
        )
        log.dbg('Pron Changer', r.text, r.status_code)
        if r.status_code == 200:
            log.info('Pron Changer', f'{token[:30]}... >> Changed To >> {self.newpron}')
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Pron Changer', f'{token[:30]}... >> Limited For {limit}s')
            time.sleep(float(limit))
            self.change(token)
        elif 'Cloudflare' in r.text:
            log.warn('Pron Changer', f'{token[:30]}... >> CLOUDFLARE BLOCKED')
            time.sleep(5)
            self.change(token)
        elif 'captcha_key' in r.text:
            log.hcap('Pron Changer', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Pron Changer', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Pron changer', error)
    
    def main(self):
        ui().prep('Change Pronous')
        self.newpron = ui().ask('Nhập Đại Từ Nhân Xưng')
        thread(
            files.getthreads(),
            self.change,
            files.gettokens(),
            [],
            False,
            self.delay
        )

class leaver:
    def __init__(self):
        self.serverid = None
        self.delay = 0.1

    def leave(self, token):
        cl = client(token)
        payload = {
            'lurking': False,
        }
        cl.headers['Authorization'] = token
        r = cl.sess.delete(
            f'https://discord.com/api/v9/users/@me/guilds/{self.serverid}',
            headers=cl.headers,
            cookies=cl.cookies,
            json=payload
        )
        log.dbg('Leaver', r.text, r.status_code)
        if r.status_code in [200, 201, 204]:
            log.info('Leaver', f'{token[:30]}... >> LEAVER >> {self.serverid}')
        elif 'retry_after' in r.text:
            limit = r.json()['retry_after']
            log.warn('Leaver', f'{token[:30]}... >> Limited For {limit}s')
            time.sleep(float(limit))
            self.leave(token)
        elif 'Cloudflare' in r.text:
            log.warn('Leaver', f'{token[:30]}... >> CLOUDFLARE BLOCKED')
            time.sleep(5)
            self.leave(token)
        elif 'captcha_key' in r.text:
            log.hcap('Leaver', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Leaver', f'{token[:30]}... >> LOCKED')
        else:
            error = log.errordatabase(r.text)
            log.error('Leaver', error)
    
    def main(self):
        ui().prep('Leaver')
        self.serverid = ui().ask('Nhập ID Server')
        thread(
            files.getthreads(),
            self.leave,
            files.gettokens(),
            [],
            False,
            self.delay
        )

class avtchange:
    def __init__(self):
        self.newavatar = None
        self.delay = 0.1
        self.cncak = None

    def check_nitro(self, token):
        cl = client(token)
        cl.headers['Authorization'] = token
        
        r = cl.sess.get('https://discord.com/api/v9/users/@me')
        if r.status_code == 200:
            user_data = r.json()
            return user_data.get('premium_type', 0) > 0
        return False

    def uu(self, token, image_path):
        file_ext = os.path.splitext(image_path.lower())[1]
        
        if file_ext == '.gif':
            if not self.check_nitro(token):
                log.warn('Avatar Changer', f'{token[:30]}... >> Account Dont Have Nitro')
                return

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        payload = {
            'avatar': f'data:image/{"png" if file_ext == ".png" else "jpeg" if file_ext in [".jpg", ".jpeg"] else "gif"};base64,{base64.b64encode(image_data).decode()}'
        }

        cl = client(token)
        cl.headers['Authorization'] = token
        
        r = cl.sess.patch(
            f'https://discord.com/api/v9/users/@me',
            headers=cl.headers,
            cookies=cl.cookies,
            json=payload
        )
        
        log.dbg('Avatar Changer', r.text, r.status_code)
        if r.status_code == 200:
            log.info('Avatar Changer', f'{token[:30]}... >> Avatar Change To >> {self.newavatar}')
        elif 'retry_after' in r.text:
            limit = r.json().get('retry_after', 1.5)
            log.warn('Avatar Changer', f'{token[:30]}... >> Limits {limit}s')
            time.sleep(float(limit))
            self.uu(token, image_path)
        elif 'Cloudflare' in r.text:
            log.warn('Avatar Changer', f'{token[:30]}... >> CLOUDFLARE BLOCK')
            time.sleep(5)
            self.uu(token, image_path)
        elif 'captcha_key' in r.text:
            log.hcap('Avatar Changer', f'{token[:30]}... >> HCAPTCHA')
        elif 'You need to verify' in r.text:
            log.critical('Avatar Changer', f'{token[:30]}... >> Verify Account Discord')
        else:
            error = log.errordatabase(r.text)
            log.error('Avatar Changer', error)

    def download_image(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
                'Referer': 'https://www.google.com/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = 'img_avt.jpg'
            else:
                filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
                
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                filename += '.jpg'

            filepath = os.path.join(tempfile.gettempdir(), filename)
            
            with open(filepath, 'wb') as file:
                file.write(response.content)
            
            return filepath
        except requests.exceptions.RequestException as e:
            log.error('Download Avatar', f'Network Error: {e}')
            return None
        except Exception as e:
            log.error('Download Avatar', f'Error Download: {e}')
            return None

    def main(self):
        ui().prep('Change Avt')
        self.newavatar = ui().ask("Nhập Link Avatar")
        
        if self.newavatar.lower().startswith(('http://', 'https://')):
            self.cncak = self.download_image(self.newavatar)
            if not self.cncak:
                log.error('Avatar Changer', 'Download Image Faild !!')
                return
            image_path = self.cncak
        else:
            image_path = self.newavatar

        thread(
            files.getthreads(),
            lambda token: self.uu(token, image_path),
            files.gettokens(),
            [],
            False,
            self.delay
        )

        if self.cncak and os.path.exists(self.cncak):
            try:
                os.remove(self.cncak)
                pass
            except Exception as e:
                log.error('Delete Image', f'Error: {e}')

while True:
    ui().cls()
    ui().banner()
    ui().versionn()
    ui().dume()
    ui().menu()

    choice = ui().ask('Choice')

    options = {
        '1': lambda: joiner().main(),
        '2': lambda: leaver().main(),
        '3': lambda: reaction().main(),
        '4': lambda: isinserver().main(),
        '5': lambda: checker().main(),
        '6': lambda: avtchange().main(),
        '7': lambda: displaychanger().main(),
        '8': lambda: pronchanger().main(),
    }

    if choice in options:
        selected_function = options[choice]

        result = selected_function()
        if asyncio.iscoroutine(result):
            asyncio.run(result)
        
        log.info('Main', 'Hoàn Thành Tiến Trình, Enter Để Tiếp Tục !!')
        input()
    else:
        log.info('Main', 'Vui Lòng Nhập Số Choice Hợp Lệ')