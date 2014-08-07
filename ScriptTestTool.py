import sublime, sublime_plugin, subprocess, threading, base64, os, tempfile

class RunScriptTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings('ScriptTestTool.sublime-settings')
        script = self.get_raw_script()
        sublime.set_timeout_async(lambda: self.execute_script(script), 0)

    def get_raw_script(self):
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        return content

    def execute_script(self, script):
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)

        try:
            temp_file.write(script)
            temp_file.close()

            self.start_output()
            proc = subprocess.Popen(
                self.get_proccess_args(temp_file.name),
                stdout      = subprocess.PIPE,
                stderr      = subprocess.PIPE,
                startupinfo = self.get_startup_info()
            )

            self.print_communicate(proc)

            self.print_message("\n\nProcess ended, return code: "+str(proc.returncode))

        finally:
            os.remove(temp_file.name)

    def get_proccess_args(self, file_name):
        args = [self.get_setting('php_bin', 'php'), file_name]
        return args

    def get_startup_info(self):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return startupinfo

    def get_setting(self, name, default = None):
        return self.settings.get(name, default)

    def start_output(self):
        self.output = sublime.active_window().create_output_panel('stt')
        sublime.active_window().run_command("show_panel", {"panel": "output.stt", "toggle": False})

    def print_output(self, proc):
        data = proc.stdout.readline().decode(encoding='UTF-8')
        if (self.get_setting('replace_win_eol_with_unix', True)):
            data = data.replace('\r\n', '\n')
        self.print_message(data)

    def print_message(self, message):
        self.output.run_command('append', {'characters': message, 'force': True, 'scroll_to_end': self.get_setting('scroll_output_to_end', True)})

    def print_communicate(self, proc):
        (results, errors) = proc.communicate()

        if errors != b'':
            print(errors)
            return

        results = results.decode(encoding='UTF-8')

        if (self.get_setting('replace_win_eol_with_unix', True)):
            results = results.replace('\r\n', '\n')

        self.print_message(results)