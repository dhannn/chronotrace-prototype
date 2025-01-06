from datetime import datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

from uuid import UUID

class DatabaseConnection:
    def __init__(self):

        # Use a service account.
        cred = credentials.Certificate('comet-chronotrace-firebase-adminsdk-66usr-bbb31d66bb.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        

    def is_valid_user(self, student_id):
        doc_ref = self.db.collection('users').document(student_id)
        return doc_ref.get().exists

    def add_entry(self, student_id, session_id):
        user_ref = self.db.collection('users').document(student_id)
        has_entered = user_ref.get(['entered']).to_dict()['entered']
        
        if has_entered:
            recent = user_ref.get(['recent_session']).to_dict()['recent_session']
            log_ref = self.db.collection('logs').document(recent)
            log_ref.update(
                {'time_out': firestore.SERVER_TIMESTAMP}
            )
            timestamp = log_ref.get(['time_out']).to_dict()['time_out']
            
            user_ref.update({'entered': not has_entered})
            updated_user_info = user_ref.get(['first_name', 'entered']).to_dict()
        else: 
            data = {
                'student_id': user_ref,
                'time_in': firestore.SERVER_TIMESTAMP
            }
            
            log_ref = self.db.collection('logs').document(str(session_id))
            log_ref.set(data)
            user_ref.update({'entered': not has_entered, 'recent_session': str(session_id)})

            timestamp = log_ref.get(['time_in']).to_dict()['time_in']
        
            updated_user_info = user_ref.get(['first_name', 'entered']).to_dict()

        return {
            'timestamp': timestamp,
            'entered': updated_user_info['entered'],
            'name': updated_user_info['first_name']
        }
        
