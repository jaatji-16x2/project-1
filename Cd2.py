import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

kivy.require('2.0.0')

# Dummy data for demonstration
customers = {
    'customer1': {'password': 'pass1', 'milk_records': []},
    'customer2': {'password': 'pass2', 'milk_records': []},
}

class OwnerInterface(Screen):
    def __init__(self, **kwargs):
        super(OwnerInterface, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.bill_input = TextInput(hint_text='Enter Customer Code', multiline=False)
        layout.add_widget(self.bill_input)

        check_bill_btn = Button(text='Check Bill')
        check_bill_btn.bind(on_press=self.check_bill)
        layout.add_widget(check_bill_btn)

        milk_entry_btn = Button(text='Enter Milk Purchase')
        milk_entry_btn.bind(on_press=self.enter_milk)
        layout.add_widget(milk_entry_btn)

        self.milk_type_input = TextInput(hint_text='Enter Milk Type (cow/buffalo)', multiline=False)
        layout.add_widget(self.milk_type_input)

        self.amount_input = TextInput(hint_text='Enter Amount in Litres', multiline=False)
        layout.add_widget(self.amount_input)

        self.date_input = TextInput(hint_text='Enter Date (YYYY-MM-DD)', multiline=False)
        layout.add_widget(self.date_input)

        submit_btn = Button(text='Submit Milk Entry')
        submit_btn.bind(on_press=self.submit_milk_entry)
        layout.add_widget(submit_btn)

        self.add_widget(layout)

    def check_bill(self, instance):
        code = self.bill_input.text
        if code in customers:
            total = sum(record['cost'] for record in customers[code]['milk_records'])
            self.show_popup('Total Bill', f'Total Bill for {code}: ₹{total}')
        else:
            self.show_popup('Error', 'Customer not found.')

    def submit_milk_entry(self, instance):
        code = self.bill_input.text
        milk_type = self.milk_type_input.text.lower()
        amount = self.amount_input.text
        date = self.date_input.text

        if code in customers and milk_type in ['cow', 'buffalo'] and amount.isdigit():
            price_per_litre = 55 if milk_type == 'cow' else 70
            total_cost = price_per_litre * int(amount)
            customers[code]['milk_records'].append({'date': date, 'amount': int(amount), 'cost': total_cost})
            self.show_popup('Success', f'Milk entry added for {code}. Total cost: ₹{total_cost}')
        else:
            self.show_popup('Error', 'Invalid input. Please check the details.')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class CustomerInterface(Screen):
    def __init__(self, **kwargs):
        super(CustomerInterface, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.code_input = TextInput(hint_text='Enter Code', multiline=False)
        layout.add_widget(self.code_input)

        self.password_input = TextInput(hint_text='Enter Password', multiline=False, password=True)
        layout.add_widget(self.password_input)

        login_btn = Button(text='Login')
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        self.add_widget(layout)

    def login(self, instance):
        code = self.code_input.text
        password = self.password_input.text
        if code in customers and customers[code]['password'] == password:
            self.show_records(code)
        else:
            self.show_popup('Error', 'Invalid credentials.')

    def show_records(self, code):
        records = customers[code]['milk_records']
        record_text = '\n'.join([f"{record['date']}: {record['amount']}L, Cost: ₹{record['cost']}" for record in records]) or 'No records found.'
        self.show_popup('Milk Records', record_text)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size _hint=(None, None), size=(400, 200))
        popup.open()

class DairyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(OwnerInterface(name='owner'))
        sm.add_widget(CustomerInterface(name='customer'))
        return sm

if __name__ == '__main__':
    DairyApp().run()