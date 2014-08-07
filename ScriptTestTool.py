import sublime, sublime_plugin, subprocess, threading, base64, os, time

class RunScriptTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings('ScriptTestTool.sublime-settings')
        script = self.get_raw_script()
        self.execute_script(script)
        # sublime.set_timeout_async(lambda: self.execute_script(script, None), 0)

    def get_raw_script(self):
        view_region = sublime.Region(0, self.view.size())
        view_content = self.view.substr(view_region)
        return view_content

    # def prepare_script_encoded(self, raw_script):
    #     no_tags = raw_script.replace('<?php', '')
    #     encoded = base64.b64encode(bytes(no_tags, "utf-8"))
    #     evald = "eval(base64_decode('"+encoded.decode("utf-8")+"'));"
    #     return evaled

    def prepare_script_raw(self, raw_script):
        no_tags = raw_script.replace('<?php', '')
        return no_tags

    def execute_script(self, raw_script):
        script = self.prepare_script_raw(raw_script)
        args = self.get_proccess_args(script)

        self.start_output()

        proc = subprocess.Popen(
            self.get_proccess_args(script),
            cwd         = self.get_current_dir(),
            stdout      = subprocess.PIPE,
            stderr      = subprocess.PIPE,
            startupinfo = self.get_startup_info()
        )

        self.print_communicate(proc)

        self.print_message("\n\nProcess ended, return code: "+str(proc.returncode))

    def get_proccess_args(self, script):
        args = [self.get_settings('php_bin', 'php'), '-r', script]
        return args

    def get_current_dir(self):
        current_dir = None
        return current_dir

    def get_startup_info(self):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return startupinfo

    def get_settings(self, name, default = None):
        return self.settings.get(name, default)

    def start_output(self):
        self.output = sublime.active_window().create_output_panel('stt')
        sublime.active_window().run_command("show_panel", {"panel": "output.stt", "toggle": False})

    def print_output(self, proc):
        data = proc.stdout.readline().decode(encoding='UTF-8')
        if (self.get_settings('replace_win_eol_with_unix', True)):
            data = data.replace('\r\n', '\n')
        self.print_message(data)

    def print_message(self, message):
        self.output.run_command('append', {'characters': message, 'force': True, 'scroll_to_end': self.get_settings('scroll_output_to_end', True)})

    def print_communicate(self, proc):
        (results, errors) = proc.communicate()

        if errors != b'':
            print(errors)
            return

        results = results.decode(encoding='UTF-8')

        if (self.get_settings('replace_win_eol_with_unix', True)):
            results = results.replace('\r\n', '\n')

        self.print_message(results)