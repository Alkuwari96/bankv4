frappe.ui.form.on('Bank Deposit', {
    refresh: function(frm) {
        frm.add_custom_button(__('Get Undeposited Payments'), function() {
            frappe.call({
                method: "bank_deposit.bank_deposit.doctype.bank_deposit.bank_deposit.get_undeposited_payments",
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table('payments');
                        (r.message).forEach(function(row) {
                            let child = frm.add_child('payments');
                            child.payment_entry = row.name;
                            child.customer = row.party;
                            child.amount = row.paid_amount;
                            child.payment_method = row.mode_of_payment;
                            child.reference_no = row.reference_no;
                            child.payment_date = row.posting_date;
                        });
                        frm.refresh_field('payments');
                    }
                }
            });
        });
    }
});
