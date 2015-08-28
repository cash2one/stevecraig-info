from mysql import DatabaseManager

class UserManager:

    def 

    def get_user_by_id(self, id):
        query = """
            SELECT id, username, email, phone FROM User WHERE
            id = %(id)s
        """
        return DatabaseManager().fetchone_query_and_close(query, {'id': id})

    def get_user_phone_by_id(self, id):
        query = """
            SELECT phone FROM User WHERE
            id = %(id)s
        """
        result = DatabaseManager().fetchone_query_and_close(query, {'id': id})
        if result is not None:
            return result[0]
        else:
            return None

    def get_user_id_by_phone(self, phone):
        if phone.startswith('+1'):
            phone = phone[2:]
        phone = phone.replace('-', '').replace(' ', '')
        query = """
            SELECT id FROM User WHERE
            phone = %(phone)s
        """
        result = DatabaseManager().fetchone_query_and_close(query, {'phone': phone})
        if result is not None:
            return result[0]
        else:
            return None