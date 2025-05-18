import frappe
from frappe.model.document import Document

class BankDeposit(Document):
    def validate(self):
        self.total_amount = sum([row.amount for row in self.payments])

    def on_submit(self):
        self.make_journal_entry()

    def make_journal_entry(self):
        if not self.payments:
            frappe.throw("Please select at least one payment to deposit.")

        je = frappe.new_doc("Journal Entry")
        je.posting_date = self.posting_date
        je.voucher_type = "Bank Entry"
        je.company = frappe.defaults.get_user_default("Company")
        total = 0

        for row in self.payments:
            je.append("accounts", {
                "account": "Undeposited funds - SD",
                "party_type": "Customer",
                "party": row.customer,
                "credit_in_account_currency": row.amount,
                "reference_no": row.reference_no,
                "reference_date": row.payment_date
            })
            total += row.amount

        je.append("accounts", {
            "account": self.deposit_to,
            "debit_in_account_currency": total
        })
        je.bank_account = self.deposit_to
        je.user_remark = f"Bank Deposit - {self.name}"

        je.insert()
        je.submit()
        self.journal_entry = je.name

        # Mark Payment Entries as Deposited
        for row in self.payments:
            frappe.db.set_value("Payment Entry", row.payment_entry, {
                "bank_deposit": self.name,
                "is_deposited": 1
            })

    def on_cancel(self):
        if self.journal_entry:
            je = frappe.get_doc("Journal Entry", self.journal_entry)
            je.cancel()
        # Unmark Payment Entries as deposited
        for row in self.payments:
            frappe.db.set_value("Payment Entry", row.payment_entry, {
                "is_deposited": 0,
                "bank_deposit": ""
            })

@frappe.whitelist()
def get_undeposited_payments():
    payments = frappe.db.get_all("Payment Entry",
        filters={
            "paid_to": "Undeposited funds - SD",
            "docstatus": 1,
            "is_deposited": 0
        },
        fields=["name", "party", "paid_amount", "mode_of_payment", "reference_no", "posting_date"]
    )
    return payments
