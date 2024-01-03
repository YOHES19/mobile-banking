from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys
from datetime import datetime

class HomePage(QtWidgets.QWidget):
    def __init__(self, username, user_id, cursor, connection):
        super().__init__()
        self.setWindowTitle("Mobile Banking")
        self.setGeometry(100, 100, 400, 300)
        self.username = username
        self.user_id = user_id
        self.cursor = cursor
        self.transactions = [] 
        self.connection = connection
        layout = QtWidgets.QVBoxLayout(self)

        # Add widgets to the layout
        image_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("bank.png")  # Change with the path to your image
        scaled_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(image_label)

        welcome_label = QtWidgets.QLabel(f"Selamat datang di Mobile Banking, {username}!", self)
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(welcome_label)

        saldo_menu_button = QtWidgets.QPushButton("Saldo", self)
        saldo_menu_button.clicked.connect(self.show_saldo)
        layout.addWidget(saldo_menu_button)

        transfer_menu_button = QtWidgets.QPushButton("Transfer", self)
        transfer_menu_button.clicked.connect(self.show_transfer_menu)
        layout.addWidget(transfer_menu_button)

        deposit_menu_button = QtWidgets.QPushButton("Deposit", self)
        deposit_menu_button.clicked.connect(self.show_deposit_menu)
        layout.addWidget(deposit_menu_button)

        pulsa_menu_button = QtWidgets.QPushButton("Pulsa", self)
        pulsa_menu_button.clicked.connect(self.show_pulsa_menu)
        layout.addWidget(pulsa_menu_button)

        digital_wallet_button = QtWidgets.QPushButton("Dompet Digital", self)
        digital_wallet_button.clicked.connect(self.show_digital_wallet_menu)
        layout.addWidget(digital_wallet_button)

        history_menu_button = QtWidgets.QPushButton("Riwayat", self)
        history_menu_button.clicked.connect(self.show_history_menu)
        layout.addWidget(history_menu_button)

    def show_history_menu(self):
        # Fetch the latest transactions every time the history menu is shown
        transactions = self.fetch_latest_transactions()

        history_menu = QtWidgets.QDialog(self)
        history_menu.setWindowTitle("Riwayat Transaksi")
        history_menu.setGeometry(200, 200, 600, 400)

        table = QtWidgets.QTableWidget(history_menu)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Jumlah"])

        for row, transaction in enumerate(transactions):
            table.insertRow(row)
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(transaction["date"]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(transaction["type"]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(transaction["amount"])))

        keluar_button = QtWidgets.QPushButton("Kembali", history_menu)
        keluar_button.clicked.connect(history_menu.reject)

        grid_layout = QtWidgets.QGridLayout(history_menu)
        grid_layout.addWidget(table, 0, 0, 1, 2)
        grid_layout.addWidget(keluar_button, 1, 0, 1, 2)

        history_menu.exec_()

    def fetch_latest_transactions(self):
        try:
            query = "SELECT date, type, amount FROM transactions_history WHERE user_id = %s ORDER BY date DESC"
            self.cursor.execute(query, (self.user_id,))
            latest_transactions = self.cursor.fetchall()

            # Print for debugging
            print("Latest Transactions:", latest_transactions)

            transactions_list = []
            for transaction in latest_transactions:
                # Convert date to a human-readable format
                formatted_date = datetime.strftime(transaction[0], "%Y-%m-%d")
                
                transactions_list.append({
                    "date": formatted_date,
                    "type": transaction[1],
                    "amount": transaction[2]
                })

            return transactions_list
        except Exception as e:
            print(f"Error fetching transactions_history: {e}")
            return []
    
     
    def show_pulsa_menu(self):
        pulsa_menu = QtWidgets.QDialog(self)
        pulsa_menu.setWindowTitle("Pulsa Menu")
        pulsa_menu.setGeometry(200, 200, 400, 300)

        # Tambahkan QLabel untuk ikon pulsa
        pulsa_icon_label = QtWidgets.QLabel(pulsa_menu)
        pulsa_icon_pixmap = QtGui.QPixmap("pulsa.png")  # Ganti dengan path ke ikon pulsa Anda
        scaled_pulsa_icon_pixmap = pulsa_icon_pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        pulsa_icon_label.setPixmap(scaled_pulsa_icon_pixmap)
        pulsa_icon_label.setAlignment(QtCore.Qt.AlignCenter)

        nomor_hp_label = QtWidgets.QLabel("Nomor HP:", pulsa_menu)
        pembelian_label = QtWidgets.QLabel("Pilihan Pembelian:", pulsa_menu)

        self.nomor_hp_entry = QtWidgets.QLineEdit(pulsa_menu)

        # Create buttons for each pembelian option with uniform labels
        button_5000 = QtWidgets.QPushButton("Rp. 5,000", pulsa_menu)
        button_10000 = QtWidgets.QPushButton("Rp. 10,000", pulsa_menu)
        button_15000 = QtWidgets.QPushButton("Rp. 15,000", pulsa_menu)
        button_20000 = QtWidgets.QPushButton("Rp. 20,000", pulsa_menu)
        button_25000 = QtWidgets.QPushButton("Rp. 25,000", pulsa_menu)
        button_30000 = QtWidgets.QPushButton("Rp. 30,000", pulsa_menu)

        # Connect each button to the buy_pulsa function with the corresponding amount
        button_5000.clicked.connect(lambda: self.buy_pulsa(5000))
        button_10000.clicked.connect(lambda: self.buy_pulsa(10000))
        button_15000.clicked.connect(lambda: self.buy_pulsa(15000))
        button_20000.clicked.connect(lambda: self.buy_pulsa(20000))
        button_25000.clicked.connect(lambda: self.buy_pulsa(25000))
        button_30000.clicked.connect(lambda: self.buy_pulsa(30000))

        keluar_button = QtWidgets.QPushButton("Kembali", pulsa_menu)
        keluar_button.clicked.connect(pulsa_menu.reject)

        grid_layout = QtWidgets.QGridLayout(pulsa_menu)
        grid_layout.addWidget(nomor_hp_label, 0, 0)
        grid_layout.addWidget(self.nomor_hp_entry, 0, 1)
        grid_layout.addWidget(pembelian_label, 1, 0)

        # Add buttons to the layout
        grid_layout.addWidget(button_5000, 1, 1)
        grid_layout.addWidget(button_10000, 1, 2)
        grid_layout.addWidget(button_15000, 2, 1)
        grid_layout.addWidget(button_20000, 2, 2)
        grid_layout.addWidget(button_25000, 3, 1)
        grid_layout.addWidget(button_30000, 3, 2)

        # Add QLabel for pulsa icon
        grid_layout.addWidget(pulsa_icon_label, 0, 3, 4, 1)

        grid_layout.addWidget(keluar_button, 4, 0, 1, 4)

        pulsa_menu.exec_()

    def buy_pulsa(self, jumlah_beli):
        try:
            # Get pulsa information from the input fields
            nomor_hp = self.nomor_hp_entry.text()

            # Perform validation and buy pulsa operation
            if nomor_hp and jumlah_beli > 0:
                # Call the function to handle pulsa purchase
                self.purchase_pulsa(nomor_hp, jumlah_beli)

                QtWidgets.QMessageBox.information(
                    self,
                    "Pulsa Purchase Successful",
                    f"Pulsa purchase of {jumlah_beli} for {nomor_hp} successful."
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Invalid Input",
                    "Please enter valid information for pulsa purchase."
                )
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a valid numerical amount for pulsa purchase."
            )
    def purchase_pulsa(self, nomor_hp, jumlah_beli):
     try:
        # Debugging output to print provided Nomor HP
        print(f"Provided Nomor HP: {nomor_hp}")

        # Get user_id based on the provided nomor_hp
        query_user_id = "SELECT id FROM users WHERE LOWER(TRIM(nomor_hp)) = LOWER(TRIM(%s))"
        self.cursor.execute(query_user_id, (nomor_hp,))
        user_id_result = self.cursor.fetchone()

        if user_id_result is not None:
            user_id = user_id_result[0]

            # Perform logic to handle pulsa purchase, for example, deducting balance
            # For simplicity, let's assume pulsa purchase just deducts the balance
            query_saldo = "SELECT saldo FROM users WHERE id = %s"
            self.cursor.execute(query_saldo, (user_id,))
            saldo_result = self.cursor.fetchone()

            if saldo_result is not None:
                current_balance = saldo_result[0]

                # Deduct the amount from the current balance
                new_balance = current_balance - jumlah_beli

                # Update the balance in the database
                update_query = "UPDATE users SET saldo = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_balance, user_id))
                self.connection.commit()

                # Insert pulsa purchase information into pulsa_purchases table
                insert_pulsa_purchase_query = "INSERT INTO pulsa_purchases (user_id, nomor_hp, jumlah_beli) VALUES (%s, %s, %s)"
                self.cursor.execute(insert_pulsa_purchase_query, (user_id, nomor_hp, jumlah_beli))
                self.connection.commit()

                print(f"Pulsa purchase successful for user {user_id}. New balance: {new_balance}")
            else:
                print("User not found.")
        else:
            print("Nomor HP not found.")
     except Exception as e:
        print(f"Error in purchase_pulsa: {e}")
        
    def show_digital_wallet_menu(self):
        digital_wallet_menu = QtWidgets.QDialog(self)
        digital_wallet_menu.setWindowTitle("Dompet Digital")
        digital_wallet_menu.setGeometry(200, 200, 400, 300)

        # Add QLabel for digital wallet image
        digital_wallet_image_label = QtWidgets.QLabel(digital_wallet_menu)
        digital_wallet_image_pixmap = QtGui.QPixmap("wallet.png")  # Change with the path to your digital wallet image
        scaled_digital_wallet_image_pixmap = digital_wallet_image_pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        digital_wallet_image_label.setPixmap(scaled_digital_wallet_image_pixmap)
        digital_wallet_image_label.setAlignment(QtCore.Qt.AlignCenter)

        nomor_label = QtWidgets.QLabel("Nomor:", digital_wallet_menu)
        jumlah_label = QtWidgets.QLabel("Jumlah:", digital_wallet_menu)
        jenis_dompet_label = QtWidgets.QLabel("Jenis Dompet:", digital_wallet_menu)

        # Use the instance attributes here
        self.nomor_entry = QtWidgets.QLineEdit(digital_wallet_menu)
        self.jumlah_entry = QtWidgets.QLineEdit(digital_wallet_menu)
        self.jenis_dompet_combo = QtWidgets.QComboBox(digital_wallet_menu)
        self.jenis_dompet_combo.addItems(["OVO", "Shopee", "Dana"])

        top_up_button = QtWidgets.QPushButton("Top Up", digital_wallet_menu)
        top_up_button.clicked.connect(self.top_up_amount)

        back_button = QtWidgets.QPushButton("Kembali", digital_wallet_menu)
        back_button.clicked.connect(digital_wallet_menu.reject)

        grid_layout = QtWidgets.QGridLayout(digital_wallet_menu)
        grid_layout.addWidget(digital_wallet_image_label, 0, 0, 1, 2)  # Add the image label
        grid_layout.addWidget(nomor_label, 1, 0)
        grid_layout.addWidget(self.nomor_entry, 1, 1)
        grid_layout.addWidget(jumlah_label, 2, 0)
        grid_layout.addWidget(self.jumlah_entry, 2, 1)
        grid_layout.addWidget(jenis_dompet_label, 3, 0)
        grid_layout.addWidget(self.jenis_dompet_combo, 3, 1)
        grid_layout.addWidget(top_up_button, 4, 0, 1, 2)
        grid_layout.addWidget(back_button, 5, 0, 1, 2)

        digital_wallet_menu.exec_()

    def top_up_amount(self):
     try:
        # Get top-up information from the input fields
        nomor = self.nomor_entry.text()
        jumlah = float(self.jumlah_entry.text())
        jenis_dompet = self.jenis_dompet_combo.currentText()

        # Perform validation and top-up operation
        if nomor and jumlah > 0:
            # Top-up the balance (call the correct function)
            self.top_up_balance(jumlah)

            # Connect the digital wallet to the user's account
            self.connect_digital_wallet(nomor, jenis_dompet)

            QtWidgets.QMessageBox.information(
                self,
                "Top Up Successful",
                f"Top Up of {jumlah} to {jenis_dompet} with Nomor {nomor} successful."
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter valid information for top-up."
            )
     except ValueError:
        QtWidgets.QMessageBox.warning(
            self,
            "Invalid Input",
            "Please enter a valid numerical amount for top-up."
        )



    def connect_digital_wallet(self, wallet_number, wallet_type):
     try:
        # Check if the user already has a digital wallet
        check_query = "SELECT * FROM digital_wallets WHERE user_id = %s"
        self.cursor.execute(check_query, (self.user_id,))
        existing_wallet = self.cursor.fetchone()

        if existing_wallet:
            # Update existing wallet
            update_query = "UPDATE digital_wallets SET wallet_number = %s, wallet_type = %s WHERE user_id = %s"
            self.cursor.execute(update_query, (wallet_number, wallet_type, self.user_id))
        else:
            # Insert a new wallet entry
            insert_query = "INSERT INTO digital_wallets (user_id, wallet_number, wallet_type) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_query, (self.user_id, wallet_number, wallet_type))

        self.connection.commit()

        print(f"Digital wallet connected successfully. Wallet Number: {wallet_number}, Wallet Type: {wallet_type}")
     except Exception as e:
        print(f"Error in connect_digital_wallet: {e}")
        
    def top_up_balance(self, amount):
        try:
            # Query the current balance from the database
            query_saldo = "SELECT saldo FROM users WHERE id = %s"
            self.cursor.execute(query_saldo, (self.user_id,))
            saldo_result = self.cursor.fetchone()

            if saldo_result is not None:
                current_balance = saldo_result[0]

                # Top-up the amount to the current balance
                new_balance = current_balance - amount

                # Update the balance in the database
                update_query = "UPDATE users SET saldo = %s WHERE id = %s"
                self.cursor.execute(update_query, (new_balance, self.user_id))
                self.connection.commit()

                print(f"Top-up successful. New balance: {new_balance}")
            else:
                print("User not found.")
        except Exception as e:
            print(f"Error in top_up_balance: {e}")

    def show_saldo(self):
        saldo_dialog = QtWidgets.QDialog(self)
        saldo_dialog.setWindowTitle("Saldo Anda")
        saldo_dialog.setGeometry(200, 200, 400, 250)

        query_saldo = "SELECT saldo FROM users WHERE id = %s"
        self.cursor.execute(query_saldo, (self.user_id,))
        saldo_result = self.cursor.fetchone()

        if saldo_result is not None:
            saldo_amount = saldo_result[0]
            formatted_saldo = "{:,}".format(saldo_amount)
            saldo_label = QtWidgets.QLabel(f"Saldo Anda: Rp {formatted_saldo}", saldo_dialog)
            saldo_label.setAlignment(QtCore.Qt.AlignCenter)

            # Adding an image of an ATM
            image_label = QtWidgets.QLabel(saldo_dialog)
            pixmap = QtGui.QPixmap("kartu.png")  # Change with the path to your image
            scaled_pixmap = pixmap.scaledToWidth(200)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(QtCore.Qt.AlignCenter)

            ok_button = QtWidgets.QPushButton("OK", saldo_dialog)
            ok_button.clicked.connect(saldo_dialog.accept)

            grid_layout = QtWidgets.QGridLayout(saldo_dialog)
            grid_layout.addWidget(image_label, 0, 0, 1, 2)  # Add the ATM image
            grid_layout.addWidget(saldo_label, 1, 0, 1, 2)
            grid_layout.addWidget(ok_button, 2, 0, 1, 2)

            saldo_dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "Gagal mendapatkan informasi saldo. Silakan coba lagi."
            )
    def show_transfer_menu(self):
        transfer_menu = QtWidgets.QDialog(self)
        transfer_menu.setWindowTitle("Menu Transfer")
        transfer_menu.setGeometry(200, 200, 400, 300)

        # Tambahkan widget untuk gambar transfer
        transfer_image_label = QtWidgets.QLabel(transfer_menu)
        transfer_image_pixmap = QtGui.QPixmap("transfer.jpg")
        scaled_transfer_image_pixmap = transfer_image_pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        transfer_image_label.setPixmap(scaled_transfer_image_pixmap)
        transfer_image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Tambahkan widget untuk detail transfer
        sender_label = QtWidgets.QLabel(f"Pengirim: {self.username}", transfer_menu)
        receiver_label = QtWidgets.QLabel("Penerima:", transfer_menu)
        amount_label = QtWidgets.QLabel("Jumlah:", transfer_menu)

        receiver_entry = QtWidgets.QLineEdit(transfer_menu)
        amount_entry = QtWidgets.QLineEdit(transfer_menu)

        transfer_button = QtWidgets.QPushButton("Transfer", transfer_menu)
        transfer_button.clicked.connect(lambda: self.transfer_amount(receiver_entry.text(), amount_entry.text()))

        back_button = QtWidgets.QPushButton("Kembali", transfer_menu)
        back_button.clicked.connect(transfer_menu.reject)

        # Atur tata letak untuk menu transfer
        grid_layout = QtWidgets.QGridLayout(transfer_menu)
        grid_layout.addWidget(transfer_image_label, 0, 0, 1, 2)
        grid_layout.addWidget(sender_label, 1, 0, 1, 2)
        grid_layout.addWidget(receiver_label, 2, 0)
        grid_layout.addWidget(receiver_entry, 2, 1)
        grid_layout.addWidget(amount_label, 3, 0)
        grid_layout.addWidget(amount_entry, 3, 1)
        grid_layout.addWidget(transfer_button, 4, 0, 1, 2)
        grid_layout.addWidget(back_button, 5, 0, 1, 2)

        transfer_menu.exec_()

    def transfer_amount(self, receiver_username, amount_str):
        try:
            # Get ID of the sender
            query_sender_id = "SELECT id FROM users WHERE username = %s"
            self.cursor.execute(query_sender_id, (self.username,))
            sender_result = self.cursor.fetchone()

            if sender_result:
                sender_id = sender_result[0]

                # Get ID of the receiver
                query_receiver_id = "SELECT id FROM users WHERE username = %s"
                self.cursor.execute(query_receiver_id, (receiver_username,))
                receiver_result = self.cursor.fetchone()

                if receiver_result:
                    receiver_id = receiver_result[0]

                    # Convert amount to an integer
                    amount = int(amount_str)

                    # Check if the sender has sufficient balance
                    if amount > 0:
                        # Update sender's balance
                        update_sender_saldo_query = "UPDATE users SET saldo = saldo - %s WHERE id = %s"
                        self.cursor.execute(update_sender_saldo_query, (amount, sender_id))

                        # Update receiver's balance
                        update_receiver_saldo_query = "UPDATE users SET saldo = saldo + %s WHERE id = %s"
                        self.cursor.execute(update_receiver_saldo_query, (amount, receiver_id))

                        # Insert transfer record
                        insert_transfer_query = "INSERT INTO transfers (sender_id, receiver_id, amount) VALUES (%s, %s, %s)"
                        self.cursor.execute(insert_transfer_query, (sender_id, receiver_id, amount))

                        # Commit changes to the database
                        self.connection.commit()

                        # Display success message (customize as needed)
                        QtWidgets.QMessageBox.information(
                            self,
                            "Transfer Berhasil",
                            f"Berhasil mentransfer {amount} ke {receiver_username}."
                        )
                    else:
                        # Display invalid amount message (customize as needed)
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Transfer Gagal",
                            "Jumlah tidak valid. Silakan coba lagi."
                        )
                else:
                    # Display receiver not found message (customize as needed)
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Transfer Gagal",
                        f"Penerima dengan nama pengguna {receiver_username} tidak ditemukan."
                    )
            else:
                # Display sender not found message (customize as needed)
                QtWidgets.QMessageBox.warning(
                    self,
                    "Transfer Gagal",
                    f"Pengirim dengan nama pengguna {self.username} tidak ditemukan."
                )

        except mysql.connector.Error as err:
            print("Error MySQL: {}".format(err))
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Terjadi kesalahan saat melakukan transfer: {err}"
            )
            import traceback
            traceback.print_exc()

    def show_deposit_menu(self):
        deposit_menu = QtWidgets.QDialog(self)
        deposit_menu.setWindowTitle("Menu Deposit")
        deposit_menu.setGeometry(200, 200, 400, 300)

        # Tambahkan widget untuk detail deposit
        amount_label = QtWidgets.QLabel("Jumlah:", deposit_menu)
        amount_entry = QtWidgets.QLineEdit(deposit_menu)

        deposit_button = QtWidgets.QPushButton("Deposit", deposit_menu)
        deposit_button.clicked.connect(lambda: self.deposit_amount(amount_entry.text()))

        back_button = QtWidgets.QPushButton("Kembali", deposit_menu)
        back_button.clicked.connect(deposit_menu.reject)

        # Tambahkan widget untuk gambar deposito
        deposit_image_label = QtWidgets.QLabel(deposit_menu)
        pixmap = QtGui.QPixmap("deposito.png")  # Ganti dengan path gambar deposito Anda
        scaled_pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        deposit_image_label.setPixmap(scaled_pixmap)
        deposit_image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Atur tata letak untuk menu deposit
        grid_layout = QtWidgets.QGridLayout(deposit_menu)
        grid_layout.addWidget(deposit_image_label, 0, 0, 1, 2)
        grid_layout.addWidget(amount_label, 1, 0)
        grid_layout.addWidget(amount_entry, 1, 1)
        grid_layout.addWidget(deposit_button, 2, 0, 1, 2)
        grid_layout.addWidget(back_button, 3, 0, 1, 2)

        deposit_menu.exec_()

    def deposit_amount(self, amount_str):
        try:
            # Konversi jumlah menjadi integer
            amount = int(amount_str)

            # Periksa apakah jumlah deposit valid
            if amount > 0:
                # Perbarui saldo pengguna
                update_saldo_query = "UPDATE users SET saldo = saldo + %s WHERE id = %s"
                self.cursor.execute(update_saldo_query, (amount, self.user_id))

                # Masukkan catatan deposit
                insert_deposit_query = "INSERT INTO deposits (user_id, amount) VALUES (%s, %s)"
                self.cursor.execute(insert_deposit_query, (self.user_id, amount))

                # Komit perubahan ke database
                self.connection.commit()

                # Tampilkan pesan sukses (dapat disesuaikan)
                QtWidgets.QMessageBox.information(
                    self,
                    "Deposit Berhasil",
                    f"Berhasil melakukan deposit sejumlah {amount}."
                )

            else:
                # Tampilkan pesan jumlah deposit tidak valid (dapat disesuaikan)
                QtWidgets.QMessageBox.warning(
                    self,
                    "Deposit Gagal",
                    "Jumlah deposit tidak valid. Silakan coba lagi."
                )

        except mysql.connector.Error as err:
            print("Error MySQL: {}".format(err))
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Terjadi kesalahan saat melakukan deposit: {err}"
            )
            import traceback
            traceback.print_exc()
            
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(330, 442)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Form.setStyleSheet("QPushButton#pushButton{\n""background-color:rgba(2, 65, 118, 255);\n""color:rgba(255, 255, 255, 200);\n""border-radius:5px;\n"
                           "}\n""QPushButton#pushButton:pressed{\n""padding-left:5px;\n""padding-top:5px;\n""background-color:rgba(2, 65, 118, 100);\n"
                           "background-position:calc(100% - 10px)center;\n""}\n""QPushButton#pushButton:hover{\n""background-color:rgba(2, 65, 118, 200);\n""}")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 290, 410))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.label.setStyleSheet("background-color:rgba(16, 30, 41, 240);\n""border-radius:10px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 210, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n""border:1px solid rgba(0, 0, 0, 0);\n""border-bottom-color:rgba(46, 82, 101, 255);\n"
                                   "color:rgb(255, 255, 255);\n""padding-bottom:7px")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 260, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n" "border:1px solid rgba(0, 0, 0, 0);\n""border-bottom-color:rgba(46, 82, 101, 255);\n"
                                     "color:rgb(255, 255, 255);\n""padding-bottom:7px")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(20, 320, 250, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(60, 30, 180, 150))
        original_pixmap = QtGui.QPixmap("icon orang.png")  # Ganti dengan path logo Anda
        scaled_pixmap = original_pixmap.scaled(180, 150, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(scaled_pixmap)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(50, 365, 211, 16))
        self.label_3.setStyleSheet("color:rgba(255, 255, 255, 150);")
        self.label_3.setObjectName("label_3")
        # Menu setup
        self.menuBar = QtWidgets.QMenuBar(Form)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 330, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setStyleSheet("background-color: rgba(16, 30, 41, 240); color: white;")
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 330, 25))
        Form.setMenuBar(self.menuBar)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit.setPlaceholderText(_translate("Form", "  Nama Pengguna"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  Kata Sandi"))
        self.pushButton.setText(_translate("Form", "L o g   I n"))
        self.label_3.setText(_translate("Form", "Lupa Nama Pengguna atau Kata Sandi?"))

    def show_home_page(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bankpbo")

            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND user_password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                self.home_page = HomePage(username, user_id, cursor, connection)
                self.home_page.show()
            else:
                QtWidgets.QMessageBox.warning(
                    self.widget,
                    "Login Gagal",
                    "Nama pengguna atau kata sandi tidak valid. Silakan coba lagi.")

        except mysql.connector.Error as err:
            print("Error MySQL: {}".format(err))
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.pushButton.clicked.connect(ui.show_home_page)
    Form.setCentralWidget(ui.widget)
    Form.show()
    sys.exit(app.exec_())
