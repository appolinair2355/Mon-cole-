import os, yaml, datetime as dt

class Database:
    def __init__(self, filename='data/ecoles.yaml'):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not os.path.exists(filename):
            self.save_data({'ecoliers': [], 'eleves': [], 'notes': [], 'payments': [], 'moyennes': [], 'admin': []})

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {'ecoliers': [], 'eleves': [], 'notes': [], 'payments': [], 'moyennes': [], 'admin': []}
        except:
            return {'ecoliers': [], 'eleves': [], 'notes': [], 'payments': [], 'moyennes': [], 'admin': []}

    def save_data(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _id(self, collection):
        data = self.load_data()
        return max([c['id'] for c in data[collection]] or [0]) + 1

    def add_ecolier(self, fields):
        data = self.load_data()
        fields['id'] = self._id('ecoliers')
        data['ecoliers'].append(fields)
        self.save_data(data)

    def add_eleve(self, fields):
        data = self.load_data()
        fields['id'] = self._id('eleves')
        data['eleves'].append(fields)
        self.save_data(data)

    def get_ecoliers(self): return self.load_data()['ecoliers']
    def get_eleves(self):   return self.load_data()['eleves']
    def get_all(self):      d = self.load_data(); return d['eleves'] + d['ecoliers']

    def add_payment(self, student_id, student_type, amount):
        data = self.load_data()
        data['payments'].append({'student_id': student_id, 'student_type': student_type, 'amount': int(amount), 'date': dt.datetime.now().strftime('%d/%m/%Y %H:%M')})
        self.save_data(data)
        return True

    def get_total_paid(self, student):
        data = self.load_data()
        return sum(p['amount'] for p in data['payments']
                   if p['student_id'] == student['id'] and p['student_type'] == ('ecolier' if student in data['ecoliers'] else 'eleve'))

    def add_note(self, student_id, student_type, classe, matiere, note):
        data = self.load_data()
        data['notes'].append({'student_id': student_id, 'student_type': student_type, 'classe': classe, 'matiere': matiere, 'note': float(note), 'date': dt.datetime.now().strftime('%d/%m/%Y %H:%M')})
        self.save_data(data)

    def get_notes(self, classe=None, matiere=None):
        data = self.load_data()['notes']
        if classe: data = [n for n in data if n['classe'] == classe]
        if matiere: data = [n for n in data if n['matiere'] == matiere]
        return data

    def get_student_notes(self, student_id, student_type):
        return [n for n in self.load_data()['notes'] if n['student_id'] == student_id and n['student_type'] == student_type]

    def save_moyennes(self, resultats, classe, pp_nom, diviseur):
        data = self.load_data()
        data['moyennes'].append({'classe': classe, 'pp_nom': pp_nom, 'diviseur': diviseur, 'resultats': resultats, 'date': dt.datetime.now().strftime('%d/%m/%Y %H:%M')})
        self.save_data(data)

    def save_admin(self, resultat, enseignants, frais_divers, scolarite_paye):
        data = self.load_data()
        data['admin'].append({'resultat': resultat, 'enseignants': enseignants, 'frais_divers': frais_divers, 'scolarite_paye': scolarite_paye, 'date': dt.datetime.now().strftime('%d/%m/%Y %H:%M')})
        self.save_data(data)

    def get_total_scolarite_due(self):
        data = self.load_data()
        return sum(int(str(e.get('montant_scolarite', '0')).strip() or 0) for e in data['eleves'] + data['ecoliers'])
                      
