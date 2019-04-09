from os import environ
from Components.Language import language
from gettext import bindtextdomain, dgettext, gettext
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

def localeInit():
	environ["LANGUAGE"] = language.getLanguage()[:2]
	bindtextdomain("ImageManager", resolveFilename(SCOPE_PLUGINS, "Extensions/ImageManager/locale"))

def _(txt):
	t = dgettext("ImageManager", txt)
	if t == txt:
		t = gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)
