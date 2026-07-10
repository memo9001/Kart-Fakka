import json
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.text import LabelBase
from kivy.core.window import Window
import arabic_reshaper
from bidi.algorithm import get_display
LabelBase.register(
    name="Arabic",
    fn_regular="Cairo.ttf"
)

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

Window.clearcolor = (0.08, 0.08, 0.10, 1)

# قوائم المنتجات الخاصة بك بدون أي تعديل
FAKKA_PRODUCTS = [
    ("فكة  2.5  جنيه", "Fakka_2.5_Unite"),
    ("فكة  4.25 جنيه", "Fakka_4.25_Unite"),
    ("فكة  5    جنيه", "Fakka_5_Unite"),
    ("فكة  6    جنيه", "Fakka_6_NewUnite"),
    ("فكة  7    جنيه", "Fakka_7_Unite"),
    ("فكة  9    جنيه", "Fakka_9_Unite"),
    ("فكة  10   جنيه", "Fakka_10_Unite"),
    ("فكة  10   جنيه (new)", "Fakka_10_NewUnite"),
    ("فكة  10.5 جنيه", "Fakka_10.5_Unite"),
    ("فكة  11.5 جنيه", "Fakka_11.5_Unite"),
    ("فكة  12   جنيه", "Fakka_12_Unite"),
    ("فكة  12.5 جنيه", "Fakka_12.5_Unite"),
    ("فكة  13   جنيه", "Fakka_13_Unite"),
    ("فكة  13.5 جنيه", "Fakka_13.5_Unite"),
    ("فكة  15   جنيه", "Fakka_15_Unite"),
    ("فكة  15   جنيه (new)", "Fakka_15_NewUnite"),
    ("فكة  15.5 جنيه", "Fakka_15.5_Unite"),
    ("فكة  16.5 جنيه", "Fakka_16.5_Unite"),
    ("فكة  17.5 جنيه", "Fakka_17.5_Unite"),
    ("فكة  19.5 جنيه", "Fakka_19.5_NewUnite"),
    ("فكة  20   جنيه", "Fakka_20_Unite"),
    ("فكة  26   جنيه", "Fakka_26_Unite"),
]

MARED_PRODUCTS = [
    ("مارد 10 دقايق", "Mared_10_Minuts"),
    ("مارد 10 فليكس", "Mared_10_Flexs"),
    ("مارد 10 سوشيال", "Mared_10_Social"),
]

ALL_PRODUCTS = FAKKA_PRODUCTS + MARED_PRODUCTS
PRODUCT_NAMES = [ar(item[0]) for item in ALL_PRODUCTS]


class VodafoneCashApp(App):

    def build(self):
        # واجهة التطبيق - ترتيب عمودي وبادئ مريح للعين
        self.main_layout = BoxLayout(
            orientation='vertical', padding=15, spacing=12
        )

        # 1. القائمة المنسدلة لاختيار نوع الكارت
        self.main_layout.add_widget(
            Label(
    text=ar("اختر نوع الكارت المعين:"),
    font_name="Arabic",
color=(1,1,1,1),
font_size=16,
                size_hint_y=None,
                height=30,
            )
        )
        self.card_spinner = Spinner(
            text=ar("اضغط هنا لاختيار الكارت"),
            font_name="Arabic",
            option_cls=Spinner.option_cls,
            values=PRODUCT_NAMES,
            size_hint_y=None,
            height=50,
            font_size=16,
        )
        self.main_layout.add_widget(self.card_spinner)
         self.card_spinner.option_cls.font_name = "Arabic"

        # 2. خانة إدخال رقم المستلم
        self.receiver_input = TextInput(
            hint_text="📱 ادخل الرقم اللي عايز تشحن له (11 رقم)",
            foreground_color=(1,1,1,1),
background_color=(0.13,0.13,0.13,1),
cursor_color=(0.89,0.04,0.16,1),
            font_name="Arabic",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size=16,
            input_filter="int",
        )
        self.main_layout.add_widget(self.receiver_input)

        # 3. خانة إدخال الرقم السري للمحفظة
        self.pin_input = TextInput(
            hint_text="🔒 ادخل الرقم السري للمحفظة",
            foreground_color=(1,1,1,1),
background_color=(0.13,0.13,0.13,1),
cursor_color=(0.89,0.04,0.16,1),
            font_name="Arabic",
            multiline=False,
            password=True,  # يخفي الباسورد على شكل نجوم للأمان
            size_hint_y=None,
            height=50,
            font_size=16,
            input_filter="int",
        )
        self.main_layout.add_widget(self.pin_input)

        # 4. زر تشغيل العملية
        self.btn_submit = Button(
            text="🚀 بدء عملية الشحن التلقائي",
            font_name="Arabic",
            size_hint_y=None,
            height=55,
            background_color=(0.89, 0.04, 0.16, 1),
            font_size=18,
        )
        self.btn_submit.bind(on_press=self.start_thread)
        self.main_layout.add_widget(self.btn_submit)

        # 5. شاشة السجل وعرض تفاصيل الـ print السابقة
        scroll = ScrollView()
        self.log_label = Label(
            text="حالة العمليات ستظهر هنا خطوة بخطوة...\n",
            font_name="Arabic",
            color=(1,1,1,1),
            markup=True,
            size_hint_y=None,
            halign="center",
            valign="top",
            font_size=15,
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        self.main_layout.add_widget(scroll)

        return self.main_layout

    def write_log(self, text):
        # تحديث النص في واجهة التطبيق
        self.log_label.text += f"{text}\n"
        
    def start_thread(self, instance):
        # تشغيل الكود في الخلفية لكي لا يتوقف التطبيق عن الاستجابة أثناء طلبات الويب
        threading.Thread(target=self.process_billing).start()

    def process_billing(self):
        # تفريغ الشاشة القديمة أولاً
        self.log_label.text = "⏳ جاري بدء العملية...\n"

        # أخذ المدخلات من الواجهة
        selected_card = self.card_spinner.text
        receiver = self.receiver_input.text.strip()
        pin = self.pin_input.text.strip()

        # التحقق من صحة الاختيارات
        if selected_card == "اضغط هنا لاختيار الكارت":
            self.write_log("❌ خطأ: يرجى اختيار نوع الكارت أولاً!")
            return

        if not (receiver.startswith("01") and len(receiver) == 11):
            self.write_log("❌ خطأ: رقم الهاتف غير صحيح (يجب أن يبدأ بـ 01 ومكون من 11 رقم).")
            return

        if not pin:
            self.write_log("❌ خطأ: يرجى كتابة الرقم السري للمحفظة.")
            return

        # معرفة الـ product_id بناءً على الاسم المختار
        product_id = None
        for name, p_id in ALL_PRODUCTS:
            if name == selected_card:
                product_id = p_id
                break

        # -------------------------------------------------------------
        # كود الـ Requests الفعلي الخاص بك بدون أي تعديل في المنطق والبيانات
        # -------------------------------------------------------------
        self.write_log("🔄 جاري الحصول على الـ Seamless Token...")

        url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
        headers_seamless = {
            'User-Agent': "okhttp/4.11.0",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'x-dynatrace': "MT_3_5_2386790616_1-0_a556db1b-4506-43f3-854a-1d2527767923_0_21317_157",
            'x-agent-operatingsystem': "13",
            'clientId': "AnaVodafoneAndroid",
            'Accept-Language': "ar",
            'x-agent-device': "OPPO CPH2235",
            'x-agent-version': "2024.7.2.1",
            'x-agent-build': "1050",
            'digitalId': "24S0M31T0I9RK",
        }

        try:
            response_seamless = requests.get(
                url_seamless, headers=headers_seamless
            )
            seamless_data = response_seamless.json()
            seamless_token = seamless_data.get('seamlessToken')
            sender_msisdn = seamless_data.get('msisdn')

            if seamless_token:
                self.write_log("✅ تم تسجيل الدخول بنجاح إلى الكاش.")
            else:
                self.write_log("❌ فشل الحصول على Seamless Token.")
                return

            # الحصول على access token
            self.write_log("🔄 جاري طلب الـ Access Token...")
            url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
            payload_token = {
                'grant_type': "password",
                'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3",
                'client_id': "cash-app",
            }
            headers_token = {
                'User-Agent': "okhttp/4.11.0",
                'Accept': "application/json, text/plain, */*",
                'Accept-Encoding': "gzip",
                'silentLogin': "true",
                'seamlessToken': seamless_token,
                'firstTimeLogin': "true",
                'x-dynatrace': "MT_3_5_2386790616_1-0_a556db1b-4506-43f3-854a-1d2527767923_0_21520_165",
                'x-agent-operatingsystem': "13",
                'clientId': "AnaVodafoneAndroid",
                'Accept-Language': "ar",
                'x-agent-device': "OPPO CPH2235",
                'x-agent-version': "2024.7.2.1",
                'x-agent-build': "1050",
                'digitalId': "24S0M31T0I9RK",
            }

            response_token = requests.post(
                url_token, data=payload_token, headers=headers_token
            )
            access_token = response_token.json()['access_token']

            # تنفيذ طلب الشحن
            self.write_log("🔄 جاري تنفيذ أمر شحن الكارت الآن...")
            url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"

            payload_order = {
                "channel": {"name": "MobileApp"},
                "orderItem": [
                    {
                        "action": "insert",
                        "id": product_id,
                        "product": {
                            "characteristic": [
                                {"name": "PaymentMethod", "value": "VFCash"},
                                {"name": "USE_EMONEY", "value": "False"},
                                {"name": "MerchantCode", "value": ""},
                            ],
                            "id": product_id,
                            "relatedParty": [
                                {
                                    "id": sender_msisdn,
                                    "name": "MSISDN",
                                    "role": "Subscriber",
                                },
                                {
                                    "id": receiver,
                                    "name": "Receiver",
                                    "role": "Receiver",
                                },
                            ],
                        },
                        "@type": product_id,
                        "eCode": 0,
                    }
                ],
                "relatedParty": [
                    {"id": pin, "name": "pin", "role": "Requestor"}
                ],
                "@type": "CashFakkaAndMared",
            }

            headers_order = {
                'User-Agent': "okhttp/4.11.0",
                'Connection': "Keep-Alive",
                'Accept': "application/json",
                'Accept-Encoding': "gzip",
                'Content-Type': "application/json",
                'api-host': "ProductOrderingManagement",
                'useCase': "CashFakkaAndMared",
                'x-dynatrace': "MT_3_5_2386790616_1-0_a556db1b-4506-43f3-854a-1d2527767923_0_2_160",
                'api-version': "v2",
                'msisdn': (
                    f'0{sender_msisdn}'
                    if sender_msisdn and not str(sender_msisdn).startswith('0')
                    else sender_msisdn
                ),
                'Authorization': f"Bearer {access_token}",
                'Accept-Language': "ar",
                'x-agent-operatingsystem': "13",
                'clientId': "AnaVodafoneAndroid",
                'x-agent-device': "OPPO CPH2235",
                'x-agent-version': "2024.7.2.1",
                'x-agent-build': "1050",
                'digitalId': "24S0M31T0I9RK",
            }

            response_order = requests.post(
                url_order,
                data=json.dumps(payload_order),
                headers=headers_order,
            )

            result = response_order.json()
            if result.get('state') == 'Completed' or result.get('complete'):
                self.write_log("🎉 ✅ تم الشحن بنجاح واكتملت العملية!")
            else:
                self.write_log("❌ فشل: رصيدك غير كافي أو هناك خطأ في المحفظة.")
                self.write_log(f"الرد من فودافون: {result}")

        except Exception as e:
            self.write_log(f"❌ حدث خطأ غير متوقع أثناء الاتصال:\n{str(e)}")


if __name__ == '__main__':
    VodafoneCashApp().run()
