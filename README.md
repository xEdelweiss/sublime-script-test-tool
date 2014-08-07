Script Test Tool - Sublime Text 3 Plugin
========================

Sublime Text 3 plugin to execute the script **without saving the file**.
Interpreter is chosen by scope at the cursor point. Tested only under Windows OS.

### Plug-and-play :)
If you have your **PHP/Python/Ruby/Dart** binary in PATH, then no additional configuration required.
Just create/open new tab, set correct syntax, write some code and **press F5** (by default)

### What..? Why..? We have build systems!
Build system cannot work with unsaved files. This plugin designed for easy testing of simple scripts.

### Installation

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to ``sublime-script-test-tool``
* Copy the folder to your Sublime Text 3 ``Packages`` directory

### How to add new scope / interpreter / arguments list
**Scope** is the Sublime Text scope. To get scope name press ``[Ctrl+Alt+Shift+P]`` _(default ST shortcut)_ — the status bar at the bottom of the screen will display a comprehensive list of all the scope keys that apply to the character immediately following your cursor position. You need the first one.

**Command** is the alias for arguments list (e.g., ``php``, ``php-5.5``, etc.)

**Args** is a list of arguments to be called. Plugin will replace ``%file%`` item of args with the name of the tempfile your script will be saved to.

So, you have to:

1. Add ``command_name:args`` to ``settings.commands_args`` array
2. Add ``scope_name:command_name`` to ``settings.scopes_commands`` array
3. ...
2. Profit!
