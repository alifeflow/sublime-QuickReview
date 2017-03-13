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
		# lines = view.substr(sublime.Region(0, view.size()))

		#Staging related
		stagingKey = ""
		stagingValue = ""
		stagingLevel = -1

		#The variables for tabbed contents parsing
		levelTitle = dict()
		currentLevel = 0

		#Get contents line by line
		regions = view.lines(sublime.Region(0, view.size()))
		for region in regions:
			line = view.substr(region)

			#Get level
			currentLevel = len(line)
			line = line.lstrip("\t")
			newLen = len(line)
			if newLen == 0:
				continue
			currentLevel -= newLen
			levelTitle[currentLevel] = line

			for i in range(currentLevel):
				line = levelTitle[i] + " " + line

			#parse the contents
			m = re.findall("(.*)"+mark+"(\\S+)\\s+(.*)", line)
			for match in m:
				if currentLevel <= stagingLevel:
					sort_store(stagingKey, stagingValue)
				stagingLevel = currentLevel
				stagingValue = match[0]+match[2]
				stagingKey = match[1]
		#Add the last line
		sort_store(stagingKey, stagingValue)

		#Print the result dict
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
