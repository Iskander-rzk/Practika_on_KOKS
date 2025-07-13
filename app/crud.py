from sqlite3 import Error
import logging
from app.models.models import IPAddressDB
from app.core.database import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_ip_address(ip_address: str) -> bool:
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ip_addresses (ip_address) VALUES (?)",
            (ip_address,)
        )
        conn.commit()
        return True
    except Error as e:
        logger.error(f"Error creating IP address: {e}")
        return False
    finally:
        conn.close()

def get_all_ip_addresses() -> list[IPAddressDB]:
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, ip_address FROM ip_addresses")
        return [IPAddressDB(id=row[0], ip_address=row[1]) for row in cursor.fetchall()]
    except Error as e:
        logger.error(f"Error fetching IP addresses: {e}")
        return []
    finally:
        conn.close()

def delete_ip_address(ip_address: str) -> bool:
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM ip_addresses WHERE ip_address = ?",
            (ip_address,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        logger.error(f"Error deleting IP address: {e}")
        return False
    finally:
        conn.close()

def search_ip_addresses(search_term: str) -> list[IPAddressDB]:
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, ip_address FROM ip_addresses WHERE ip_address LIKE ?",
            (f"%{search_term}%",)
        )
        return [IPAddressDB(id=row[0], ip_address=row[1]) for row in cursor.fetchall()]
    except Error as e:
        logger.error(f"Error searching IP addresses: {e}")
        return []
    finally:
        conn.close()

def select(ip_address: str) -> IPAddressDB | None:
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, ip_address FROM ip_addresses WHERE ip_address = ?",
            (ip_address,)
        )
        row = cursor.fetchone()
        return IPAddressDB(id=row[0], ip_address=row[1]) if row else None
    except Error as e:
        logger.error(f"Error selecting IP address: {e}")
        return None
    finally:
        conn.close()