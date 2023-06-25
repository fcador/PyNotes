from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QPushButton, QWidget, QInputDialog, QListWidgetItem, QMessageBox, QHBoxLayout, QLabel
from database import Database
from PyQt5.QtCore import QTimer, Qt

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle('Note App')
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()

        # Logique de création du projet et de l'enregistrement au clic
        self.add_project_button.clicked.connect(self.add_project)
        self.save_note_button.clicked.connect(self.save_note)

        # Logique de chargement d'une note à la sélection d'un projet.
        self.project_list.currentItemChanged.connect(self.load_note)
        
        # Sélectionne par défaut le dernier projet de la liste
        self.load_projects_from_db()

        # Sauvegarde auto ttes les 10sec
        self.timer = QTimer()
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.save_note)
        self.timer.start()


    def setup_ui(self):
        # Création du widget central qui contiendra nos autres widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Création un layout vertical pour le widget central
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Création du bouton d'ajout de projet
        self.add_project_button = QPushButton('Ajouter un projet')
        self.main_layout.addWidget(self.add_project_button)

        # Création de la liste de projets
        self.project_list = QListWidget()
        self.main_layout.addWidget(self.project_list)

        # Création de la zone d'édition de texte pour les notes
        self.note_editor = QTextEdit()
        self.main_layout.addWidget(self.note_editor)

        # Message user pour save
        self.save_label = QLabel('')
        self.save_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.save_label)

        # Bouton de sauvegarde en dehors des saves auto
        self.save_note_button = QPushButton('Sauvegarder les notes')
        self.main_layout.addWidget(self.save_note_button)

    def load_projects_from_db(self):
        for project_id, project_name in self.db.load_projects():
            self.add_project_to_list(project_id, project_name)

        last_item_index = self.project_list.count() - 1
        if last_item_index >= 0:  
            self.project_list.setCurrentRow(last_item_index)

    def add_project_to_list(self, project_id, project_name):
        widget = QWidget()
        layout = QHBoxLayout()
        label = QLabel(project_name)
        delete_button = QPushButton('Supprimer')
        layout.addWidget(label)
        layout.addWidget(delete_button)
        widget.setLayout(layout)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, project_id)
        item.setSizeHint(widget.sizeHint())
        self.project_list.addItem(item)
        self.project_list.setItemWidget(item, widget)

        delete_button.clicked.connect(lambda checked, pid=project_id: self.delete_project(pid))

    # Logique de création d'un projet. On récupère l'id généré par l'insertion
    def add_project(self):
        project_name, ok = QInputDialog.getText(self, 'Nouveau projet', 'Entrez le nom du projet :')
        if ok and project_name:
            project_id = self.db.add_project(project_name)
            item = QListWidgetItem(project_name)
            item.setData(Qt.UserRole, project_id)
            self.project_list.addItem(item)

    # Logique d'enregistrement des notes dans la bdd basée sur l'id du projet
    def save_note(self):
        current_item = self.project_list.currentItem()
        if current_item is not None:
            project_id = current_item.data(Qt.UserRole)
            note_content = self.note_editor.toPlainText()
            self.db.add_note(project_id, note_content)

        self.save_label.setText('Note sauvegardée')
        QTimer.singleShot(1000, self.hide_save_message)


    # On charge la note attachée au projet. Même si non utilisé, nécessité d'avoir previous_item en argument car dans tous les cas renvoyé par currentItemChanged
    def load_note(self, current_item, previous_item):
        if current_item is not None:
            project_id = current_item.data(Qt.UserRole)
            note_content = self.db.get_note(project_id)
            self.note_editor.setPlainText(note_content)

    def delete_project(self, project_id):
        confirm = QMessageBox.question(self, 'Confirmation', 'Voulez-vous vraiment supprimer ce projet ?')
        if confirm == QMessageBox.Yes:
            self.db.delete_project(project_id)
            for i in range(self.project_list.count()):
                item = self.project_list.item(i)
                if item.data(Qt.UserRole) == project_id:
                    self.project_list.takeItem(i)
                    break

    def hide_save_message(self):
        self.save_label.setText('')


    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)


def main():
    app = QApplication([])
    window = NoteApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
