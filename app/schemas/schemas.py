from app.core.database import get_db_connection
from app.models.models import IPAddressDB


def create_ip_address(ip_address: str, description: str = ""):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO ip_addresses (ip_address, description) VALUES (%s, %s)"
            cursor.execute(query, (ip_address, description))
            conn.commit()
            return True
        except Error as e:
            print(f"Error creating IP address: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return False


def get_all_ip_addresses():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM ip_addresses"
            cursor.execute(query)
            result = cursor.fetchall()
            return [IPAddressDB(**row) for row in result]
        except Error as e:
            print(f"Error fetching IP addresses: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return []


def delete_ip_address(ip_address: str):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM ip_addresses WHERE ip_address = %s"
            cursor.execute(query, (ip_address,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting IP address: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return False


def search_ip_addresses(search_term: str):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM ip_addresses WHERE ip_address LIKE %s OR description LIKE %s"
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            result = cursor.fetchall()
            return [IPAddressDB(**row) for row in result]
        except Error as e:
            print(f"Error searching IP addresses: {e}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return []


def import_from_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            ip_addresses = [line.strip() for line in file if line.strip()]

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE ip_addresses")

                for ip in ip_addresses:
                    cursor.execute(
                        "INSERT INTO ip_addresses (ip_address) VALUES (%s)",
                        (ip,)
                    )
                conn.commit()
                return True
            except Error as e:
                print(f"Error importing IP addresses: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


def export_to_file(file_path: str):
    ip_addresses = get_all_ip_addresses()
    try:
        with open(file_path, 'w') as file:
            for ip in ip_addresses:
                file.write(f"{ip.ip_address}\n")
        return True
    except Exception as e:
        print(f"Error exporting to file: {e}")
        return False