import sublime
import sublime_plugin
import re


mItems = dict()


class review_fileCommand(sublime_plugin.WindowCommand):
	def run(self, mark, edit = None):
		view = sublime.active_window().active_view()
		tab = creat_tab(view, "Review", "md")

		global mItems
		mItems.clear()
		output = ""

		# Get contents to be parsed
		lines = view.substr(sublime.Region(0, view.size()))

		#parse the contents
		m = re.findall("(.*)"+mark+"(\\S+)\\s+(.*)", lines)
		for match in m:
			sort_store(match[1], match[0]+match[2])

		for key in mItems:
			output = output + key + ":\n"+ mItems[key] + "\n"

		# output the contents
		set_code(tab, output, "Packages/MarkdownHighlighting/Markdown.sublime-syntax")

def sort_store(key, value):
	global mItems
	if key in mItems:
		mItems[key] = mItems[key] + "\n" + "\t" + value
	else:
		mItems[key] = "\t" + value
	print (mItems)

def creat_tab(view, title, type):
	win = view.window()
	tab = win.new_file()
	tab.set_name(title+"."+type)
	return tab

def set_code(tab, code, syntax):
	# tab.set_name('untitled.' + self.type)
	# insert codes
	tab.run_command('insert_snippet', {'contents': code})
	tab.set_syntax_file(syntax)
