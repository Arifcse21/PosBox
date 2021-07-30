from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import re


class OperatorsWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cart = []
        self.qty = []
        self.total = 0.00

    def update_purchases(self):
        pcode = self.ids.code_inp.text
        products_container = self.ids.products
        if pcode == "1234" or pcode == "2345":
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={"top": 1})
            products_container.add_widget(details)
            pname = "Product One"
            if pcode == "2345":
                pname = "Product Two"

            code = Label(text=pcode, size_hint_x=0.3, color=(0.06, 0.45, 0.45, 1))
            name = Label(text=pname, size_hint_x=0.3, color=(0.06, 0.45, 0.45, 1))
            qty = Label(text="1", size_hint_x=0.1, color=(0.06, 0.45, 0.45, 1))
            price = Label(text="0.00", size_hint_x=0.2, color=(0.06, 0.45, 0.45, 1))
            total = Label(text="0.00", size_hint_x=0.2, color=(0.06, 0.45, 0.45, 1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(price)
            details.add_widget(total)

            # Update Preview
            pprice = 1.00
            pqty = str(1)
            self.total += pprice
            purchase_total = "`\n\nTotal\t\t\t\t\t\t\t\t\t\t\t\t" + str(self.total)
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find("`")
            if _prev > 0:
                prev_text = prev_text[: _prev]

            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i
            if ptarget >= 0:
                pqty = self.qty[ptarget] + 1
                self.qty[ptarget] = pqty
                expr = "%s\t\t\t\tx\\d\t" % pname
                rexpr = pname + "\t\t\t\tx" + str(pqty) + "\t"
                new_text = re.sub(expr, rexpr, prev_text)
                preview.text = new_text + purchase_total
                print(pqty, type(pqty))

            else:
                self.cart.append(pcode)
                self.qty.append(1)
                new_preview = "\n".join([prev_text, pname + "\t\t\t\tx" +
                pqty + "\t\t\t\t" +
                str(pprice), purchase_total])
                preview.text = new_preview


class OperatorsApp(App):
    def build(self):
        return OperatorsWindow()


if __name__ == '__main__':
    op = OperatorsApp()
    op.run()
