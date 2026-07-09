import requests
import json

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

print("\n📋 اختر الكرت:\n")
for i, (name, _) in enumerate(ALL_PRODUCTS, 1):
    print(f"[{i}] {name}")

while True:
    try:
        choice = int(input("\nاختار رقم الكرت: "))
        if 1 <= choice <= len(ALL_PRODUCTS):
            product_name, product_id = ALL_PRODUCTS[choice - 1]
            break
        else:
            print("اختيار غير صحيح")
    except:
        print("ادخل رقم صحيح")

receiver = input("\n📱 ادخل الرقم اللي عايز تشحن له: ").strip()

if not (receiver.startswith("01") and len(receiver) == 11):
    print("رقم غير صحيح")
    exit()

pin = input("🔒 ادخل الرقم السري للمحفظة: ").strip()

# الحصول على seamless token و msisdn
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
    'digitalId': "24S0M31T0I9RK"
}

response_seamless = requests.get(url_seamless, headers=headers_seamless)
seamless_data = response_seamless.json()
seamless_token = seamless_data.get('seamlessToken')
sender_msisdn = seamless_data.get('msisdn')

if seamless_token:
    print('✅ تم تسجيل الدخول بنجاح إلى الكاش')

# الحصول على access token
url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"

payload_token = {
    'grant_type': "password",
    'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3",
    'client_id': "cash-app"
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
    'digitalId': "24S0M31T0I9RK"
}

response_token = requests.post(url_token, data=payload_token, headers=headers_token)
access_token = response_token.json()['access_token']

# تنفيذ طلب الشحن
url_order = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"

payload_order = {
    "channel": {
        "name": "MobileApp"
    },
    "orderItem": [
        {
            "action": "insert",
            "id": product_id,
            "product": {
                "characteristic": [
                    {
                        "name": "PaymentMethod",
                        "value": "VFCash"
                    },
                    {
                        "name": "USE_EMONEY",
                        "value": "False"
                    },
                    {
                        "name": "MerchantCode",
                        "value": ""
                    }
                ],
                "id": product_id,
                "relatedParty": [
                    {
                        "id": sender_msisdn,
                        "name": "MSISDN",
                        "role": "Subscriber"
                    },
                    {
                        "id": receiver,
                        "name": "Receiver",
                        "role": "Receiver"
                    }
                ]
            },
            "@type": product_id,
            "eCode": 0
        }
    ],
    "relatedParty": [
        {
            "id": pin,
            "name": "pin",
            "role": "Requestor"
        }
    ],
    "@type": "CashFakkaAndMared"
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
    'msisdn': f'0{sender_msisdn}' if sender_msisdn and not str(sender_msisdn).startswith('0') else sender_msisdn,
    'Authorization': f"Bearer {access_token}",
    'Accept-Language': "ar",
    'x-agent-operatingsystem': "13",
    'clientId': "AnaVodafoneAndroid",
    'x-agent-device': "OPPO CPH2235",
    'x-agent-version': "2024.7.2.1",
    'x-agent-build': "1050",
    'digitalId': "24S0M31T0I9RK"
}

response_order = requests.post(url_order, data=json.dumps(payload_order), headers=headers_order)

try:
    result = response_order.json()
    if result.get('state') == 'Completed' or result.get('complete'):
        print('✅ تم الشحن بنجاح!')
    else:
        print('❌ فشل: رصيدك غير كافي أو خطأ آخر')
        print(f'الرد: {result}')
except:
    print(f'❌ خطأ: {response_order.text}')