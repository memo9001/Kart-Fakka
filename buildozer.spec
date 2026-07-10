[app]

title = Vodafone Cash Fakka

package.name = vfcashfakka
package.domain = org.memo9001

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf

version = 1.0

requirements = python3,kivy,requests,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 21
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

android.allow_backup = True

log_level = 2

warn_on_root = 0
