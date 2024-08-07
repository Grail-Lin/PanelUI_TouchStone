import win32gui
from ctypes import HRESULT
from ctypes.wintypes import HWND
from comtypes import IUnknown, GUID, COMMETHOD
import comtypes.client
import os


def popup_keyboard(a):
	toggle_tabtip()
	
class ITipInvocation(IUnknown):
	_iid_ = GUID("{37c994e7-432b-4834-a2f7-dce1f13b834b}")
	_methods_ = [COMMETHOD([], HRESULT, "Toggle", (['in'], HWND, "hwndDesktop"))]


def toggle_tabtip():
	try:
		comtypes.CoInitialize()
		ctsdk = comtypes.client.CreateObject("{4ce576fa-83dc-4F88-951c-9d0782b4e376}", interface=ITipInvocation)
		ctsdk.Toggle(win32gui.GetDesktopWindow())
		comtypes.CoUninitialize()
	except OSError as e:
		os.system(r'"C:\Program Files\Common Files\microsoft shared\ink\tabtip.exe"')


def popup_tabtip():
	try:
		comtypes.CoInitialize()
		ctsdk = comtypes.client.CreateObject("{4ce576fa-83dc-4F88-951c-9d0782b4e376}", interface=ITipInvocation)
		ctsdk.Toggle(win32gui.GetDesktopWindow())
		
		comtypes.CoUninitialize()
	except OSError as e:
		os.system(r'"C:\Program Files\Common Files\microsoft shared\ink\tabtip.exe"')
